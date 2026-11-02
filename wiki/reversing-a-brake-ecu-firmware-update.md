---
title: "Reversing a Brake ECU Firmware Update"
summary: "Gardiner, USENIX VehicleSec 2026. Reverse engineers the Bendix EC80 brake ECU's J2497 power-line updater, diffs the firmware to show a safety recall also…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/vehiclesec26/presentation/gardiner"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Gardiner, USENIX VehicleSec 2026. Reverse engineers the Bendix EC80 brake ECU's J2497 power-line updater, diffs the firmware to show a safety recall also patched security bugs, and demonstrates a write-where primitive and DoS on a bench and in a moving truck."
sources:
  - url: "https://www.usenix.org/conference/vehiclesec26/presentation/gardiner"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - secure-firmware-updates
  - uds-seed-key
  - uds-firmware-extraction
  - vw-flash
  - expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol
  - firmware-acquisition
---

Gardiner, USENIX VehicleSec 2026. Reverse engineers the Bendix EC80 brake ECU's J2497 power-line updater, diffs the firmware to show a safety recall also patched security bugs, and demonstrates a write-where primitive and DoS on a bench and in a moving truck.

## What it is

Ben Gardiner (NMFTA). *4th USENIX Symposium on Vehicle Security and Privacy* (VehicleSec '26), Baltimore, MD, August 2026, pp. 389–408; an expanded whitepaper ("Reversing a Recall," v0.1) accompanies the author's Black Hat USA 2026 presentation; this page draws its detail from that full text. The subject is the Bendix EC80, the Class 8 tractor brake ECU for anti-lock braking, traction control, and electronic stability — built on two NXP MC9S12XEQ512 (S12X) microcontrollers. In late 2024 the three OEMs that integrate the EC80 recalled an estimated 450,000 ESP/ATC-equipped units: Bendix described memory corruption from electrical noise on J2497 (PLC4TRUCKS), the tractor–trailer power-line databus, and shipped a fix via a Windows updater, "ID9363." The anomaly that motivated the work: noise crashing the ECU implied the brake controller was *processing* J2497 traffic far beyond the trailer lamp messages (MIDs 0x0A/0x0B, active-ABS event) a tractor unit should receive — on an interface already known to be wirelessly injectable (the author's CVE-2022-26131) and reachable from compromised trailer telematics. The paper reverse-engineers the ID9363 update process, differentially analyses the firmware before and after across three EC80 variants (one per OEM), and asks what the patch changed. Its scope is strict: only functionality the patch *removed* is analysed, so no unpatched vulnerability is disclosed.

## What it showed

**Getting both firmwares.** The update runs UDS over J1939 (ISO-TP, unicast, adapter to brake controller): seed/key SecurityAccess, a fingerprint write, two RequestDownload/TransferData blocks writing the PFLASH ranges, a checksum routine check, reset, then a dataset/calibration block and verification reads. Capturing that traffic yields the *new* firmware in cleartext — but only the written extents: the updater skips the bootloader/vector region. The *old* firmware could not be obtained the same way: the author reconstructed the seed/key exchange in closed form and confirmed the EC80 offers no UDS upload service. So the pre-update images were dumped over the BDM debug interface (XPROG / PROGS12Z) — S12X read-out protection exists but was not enabled. Only the larger ("right") MCU's code changed. Making the images analysable took paged memory modelling in IDA Pro, live BDM RAM polling for the real interrupt-vector base, and manual resolution of indirect calls and jump tables — reaching 60–80% function coverage of the changed regions per variant. QBinDiff then showed over 98% of functions unchanged: 104–127 *deleted*, only 11–13 modified per variant, 87 deletions common to all three.

**What the patch did.** The deletions fall into three buckets: (1) *all* J1587 PID processing received over J2497, except lamp and active-ABS-event handling — the pre-update firmware parsed a full table of J1587 parameter IDs (diagnostic codes, VIN, wheel speeds, traction control) on the power-line interface and silently consumed them; (2) the SCI2 UART edge-interrupt handling in the J2497 receive path; (3) secondary J1587 machinery (diagnostic-code manager, transport-protocol connection management, timeouts). Two modified functions make the change: each simply loses its call into the deleted machinery. The remediation was not a repair of the parsing code but its *removal* — the tractor ECU stopped listening to everything on J2497 except the lamp messages the standard intends for it.

**What was in the removed code.** Four findings, each classified by verification status. (i) A J1587 PID handler (0xC2, transmitter diagnostic-code table) copied a length-prefixed payload into a small fixed stack buffer with no length check: **denial of service and remote code execution, both verified on the bench** on two variants — the S12X's memory-protection unit was not configured to prevent execution from data/stack memory, and the receive FIFO could stage the payload despite the 21-byte frame limit. (ii) A second PID handler (0xED, vehicle identification) made an unbounded copy into a static buffer, overwriting pointers a later handler dereferences: **DoS verified; the resulting write-where primitive and RCE are theoretical.** (iii) The deleted edge-interrupt code reset the receive buffer inconsistently — a write offset left un-reset plus a write-before-bounds-check append — giving a steerable out-of-bounds write (**write-where primitive, theoretical**). (iv) A third PID handler (0xC7) gated the J1587 traction-control-disable function behind a **hardcoded manufacturer access code** — an authentication bypass **verified on the bench** (the code is withheld here). Pointedly, a simple J1587 fuzzing script found the two crashing handlers — no reverse engineering needed.

**In a moving truck.** The DoS findings were validated in-motion on closed tracks, twice over. A host tractor's EC80 was back-flashed to vulnerable firmware via BDM and recalibrated with OEM tools; signals were injected with a software-defined radio through the in-cab diagnostic port, simulating the wireless path (the port's J2497 filtering is inadequate). Below 5 mph and at ~9 mph, both crashing handlers took the ECU offline: CAN traffic ceased, recovery always required a battery disconnect, and the first truck lost speedometer, steering assist, and shifting, with ABS pulsing disabled at 9 mph. On a second, fleet-owned truck from a different OEM, the same crashes produced cluster faults and loss of ABS pulsing without those losses, and the hardcoded-credential message put that truck into a persistent "Dyno Mode" needing both OEM and Bendix tools to clear — impact is integration-dependent.

## Where it fits

For this KB's [secure firmware updates](concepts/secure-firmware-updates.md) concept, the paper is the mirror-image case: the concept is about making update *delivery* trustworthy; here delivery worked conventionally (seed/key-gated UDS download, fingerprint, checksum check — the paper describes no signature verification of the images) and the failure sits one layer up, in *transparency*: a correctly delivered update silently doubled as a security patch. The fixed flaws received no CVEs and no security advisory, so operators scoring the recall as safety-only could not price their unpatched trucks' risk — the author cites ISO/IEC 29147 and CISA guidance that patched vulnerabilities should be communicated; updated firmware had reached ≈310,000 of ≈450,000 units when he wrote. His positive conclusion is architectural: ATA TMC's position paper, CISA advisory ICSA-25-021-03, and the balloted SAE J2497 revision all say tractor-side J2497 reception should be lamp messages only; the EC80 patch is the worked example of deletion as the fix. Methodologically it is a firmware-acquisition and binary-diffing study: reconstructing the [UDS seed/key](concepts/uds-seed-key.md) exchange in closed form is what proved no upload service exists, and its update capture is the heavy-vehicle instance of [UDS firmware extraction](uds-firmware-extraction.md)'s captured-session channel — with the twist that the capture alone was insufficient.

## Limits and safety notes

Detail here is from the expanded whitepaper (v0.1) — the VehicleSec paper is a 20-page condensation — whose appendices publish disassembly of the deleted functions only, a boundary the author states and this page keeps: **no trigger messages, exploit code, or the hardcoded access code are reproduced here**, and the findings are safe to describe because every one is removed by the recall firmware (absent in all three post-update versions). Scope limits: analysis covers the "right" MCU's code only; RCE through the second handler and the edge-interrupt write-where are labelled theoretical, and exploit layout depends on each "Z" version's memory layout (the DoS and credential findings worked on all three tested versions; all 13 Z versions are expected affected). In-motion testing was low-speed (≈9 mph maximum), closed-track, OEM-supported, on trucks back-flashed to vulnerable firmware. The manufacturer was contacted before the analysis and again before publication; two OEMs and NHTSA were briefed. One caution the paper supplies: random noise is *unlikely* to generate the checksum-valid frames these flaws need — "fixed noise crashes" and "fixed remotely triggerable flaws" are not the same claim.

## Status and sources

Status: **published** — *Proceedings of the 4th USENIX Symposium on Vehicle Security and Privacy (VehicleSec '26)*, USENIX Association, August 2026, pp. 389–408, ISBN 978-1-939133-56-4. **DOI: none** — USENIX assigns no DOIs to its proceedings papers, and Crossref queries (2026-11-01) returned no record; no aggregator identifier is substituted. Sources read in full 2026-11-01: the USENIX presentation page and abstract, and the expanded primary text — Gardiner, "Reversing a Recall," Black Hat USA 2026 whitepaper v0.1 (179 pp.; Appendix B's disassembly listings sampled, not read line-by-line).

## Related

- [Secure firmware updates](concepts/secure-firmware-updates.md) — the concept this paper mirrors: delivery worked; disclosure of the fixes failed
- [UDS seed/key](concepts/uds-seed-key.md) — the exchange reconstructed in closed form to prove no upload service exists
- [UDS firmware extraction](uds-firmware-extraction.md) — the captured-session channel this work's updater capture instantiates
- [VW_Flash](vw-flash.md) — update packages as an acquisition source, passenger-car side
- [Expanding the Attack Scenarios of SAE J1939](expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol.md) — J1939 protocol context for the updater
