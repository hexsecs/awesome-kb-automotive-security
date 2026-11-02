---
title: "Beneath the Bonnet: A Breakdown of Diagnostic Security"
summary: "Van den Herrewegen and Garcia, ESORICS 2018. Reverse engineers the seed-key ciphers of four manufacturers from ECU firmware and achieves remote code…"
type: entity
category: "Research Papers"
url: "https://pure-oai.bham.ac.uk/ws/portalfiles/portal/50643148/Beneath_the_Bonnet.pdf"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Van den Herrewegen and Garcia, ESORICS 2018. Reverse engineers the seed-key ciphers of four manufacturers from ECU firmware and achieves remote code execution over CAN through diagnostics alone."
sources:
  - url: "https://pure-oai.bham.ac.uk/ws/portalfiles/portal/50643148/Beneath_the_Bonnet.pdf"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1007/978-3-319-99073-6_15"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - uds-seed-key
  - lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems
  - diagnostic-service-abuse
  - calibration-plane
  - shared-and-default-secrets
---

Van den Herrewegen and Garcia, ESORICS 2018. Reverse engineers the seed-key ciphers of four manufacturers from ECU firmware and achieves remote code execution over CAN through diagnostics alone.

## What it is

Jan Van den Herrewegen and Flavio D. Garcia, University of Birmingham, UK. *23rd European Symposium on Research in Computer Security (ESORICS 2018)*, Barcelona, Springer LNCS 11098, pp. 305–324. The paper attacks the two things between a CAN-bus adversary and full control of an ECU: the **seed/key challenge–response** (UDS SecurityAccess) and the **diagnostic download mechanism** behind it. Firmware from **13 ECUs across 8 car models** was extracted via JTAG/BDM debug interfaces, the seed/key implementations located in IDA Pro and cryptanalysed; the manufacturers' own code-download path then becomes a generic remote-code-execution channel. Targets: instrument clusters, body control modules (immobiliser secrets), a gateway, a telematics unit. The paper names the manufacturers — Ford, Volvo, Fiat, and Volkswagen/Audi — and this page follows the paper's naming.

## What it showed

**Three ciphers, four manufacturers — proprietary, small-state, not diversified:** the same secret serves every ECU of a type, often every car, so each break is break-once.

*Ford cipher (also found in Volvo units).* 3-byte challenge and response. A modified Galois LFSR — 24-bit state, initialised from a firmware constant (0xC541A9) — absorbs the 24-bit challenge and then a 40-bit secret over 64 rounds; the response is a nibble permutation of the final state. Only the first 24 secret bits add entropy (same start state and taps in every ECU studied): one valid challenge/response pair recovers 24 secret bits, and a pure over-CAN attack (no valid pair needed) drops from 2^40 to **2^24 attempts**. Demonstrated over CAN on a 2012 Ford Focus BCM and a 2015 Volvo V50 Telematics Unit — neither has a failed-attempt delay (delays elsewhere fall to an ECUReset reset) — at four frames per attempt on a 500 kbit/s bus: ≈5 hours theoretical, **approximately 15 hours** implemented. Found across Focus MK2/MK3 and Fiesta MK6/MK7 clusters and BCMs (2008–2017).

*Fiat cipher (Body System Interface, pre- and post-2012).* 32-bit challenge and response; two 16-bit LFSRs, 24 rounds. A naive search is 2^48, but the paper prints two Fiat ECUs' constants side by side (Table 2) and almost everything is shared: the BSIs differ only in taps (0x8408 vs 0x3423) and in secret bytes S[0]/S[2] (0x12/0x34 vs 0x21/0x43 — nibble-reversals of each other); S[1], S[3], and the 0xFFFF start state are identical. The search collapses to **2^16 = 65,536 attempts**. Demonstrated on a Fiat Grande Punto BSI: its 10-second delay after two failed attempts is bypassed by session cycling (default → programming resets the timers); 106 seconds theoretical, **just over an hour** implemented.

*Volkswagen Group cipher (2009 Audi Gateway; 2010 VW Passat Instrument Cluster).* Not a fixed cipher but a **bytecode interpreter**: firmware-stored bytes are opcodes (rotate, add/subtract, XOR constants) over a 32-bit state initialised with the challenge itself. The Audi gateway's program is a 10-round rotate-left construction XORing 0x04C11DB7; since the state starts as the public challenge, that constant is the only secret — one challenge/response pair plus a 2^32 search recovers it. The same gateway also contains a **hardcoded backdoor**: a tester sending the response **0xCAFFE012** is authenticated whatever the challenge.

**From authentication bypass to code execution.** The ECUs lack the XCP calibration protocol; instead, diagnostic services download the XCP stack into RAM — a generic path. Once authenticated (§3 is the only lock): programming session → RequestDownload / TransferData / RequestTransferExit → RoutineControl jumps into the downloaded **"secondary bootloader"**, with read/write access to memory, firmware, and peripherals. Worked cases: a **2016 Ford Focus Instrument Cluster** (RoutineControl 0x301, explicit jump address; odometer rewritten in the external ST M95320 EEPROM — Miller & Valasek's variant used a predefined address, routine 0x304); the **Fiat BSIs** (write DIDs 0xF184/0xF185, EraseMemory 0xFF00 over exactly the download range, jump to a firmware-fixed RAM address, watchdog in reset mode to service). The authors build a **firmware extraction/modification framework** on this primitive for their Table 3 ECUs (the Volvo telematics unit's extraction *failed* — no CAN driver). Two force-multipliers: only the level-1 secret is ever needed (extracted firmware holds all other levels' secrets — the multi-level scheme collapses), and the download-address search is unauthenticated and unlimited, error codes 0x13 vs 0x31 leaking which guesses are well-formed (128 KiB of RAM = at most 8,192 probes).

**Mitigations proposed:** sound challenge-response with per-car/per-ECU diversified keys; a public-key design (128-bit challenge, ECDSA P-256); signed downloadable code; authenticated CAN (LeiA).

## Where it fits

This is the evidence anchor for the KB's [UDS seed/key](concepts/uds-seed-key.md) concept page: the concept's general claims (proprietary transforms, small seeds, cross-model secret reuse, firmware-extraction recovery) are this paper's §3. It is also the diagnostic-security counterpart to the same programme's RKE work ([Lock It and Still Lose It](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md)): those papers break the keys that *open and start* the car, this one breaks the gate that *reprograms* it — and the paper connects the two: bootloader firmware dumps recover PKE/immobiliser keys. Against Miller & Valasek's earlier Ford work it generalises both halves — the cipher falls over CAN with no valid pair, and RAM-download execution is cross-manufacturer — with the "automotive worm" implication stated by the authors. Its mitigation section is the bridge to [LeiA](leia-a-lightweight-authentication-protocol-for-can.md).

## Limits and safety notes

From the paper itself:

- **Bench sample, physical first step.** Ciphers were recovered from firmware extracted via debug interfaces — one physical unit per ECU type is needed before the over-CAN attacks exist. 13 ECUs / 8 models, no fleet-wide prevalence claimed; findings are generation-specific (≈2008–2017).
- **Uneven strength inside one manufacturer.** The Volkswagen Group result is explicitly variable: the broken program is the Audi gateway's; several VW clusters use more rounds and multiple constants ("more secure", per the authors). Ford timings likewise assume no delay timer on the studied units.
- **The chain needs a CAN foothold.** Everything after §3 presupposes an attacker who can already send/receive on the target bus (OBD-II or a compromised ECU); the paper's point is escalation from that foothold, not initial access.
- Responsible disclosure: manufacturers informed in **April 2018**, five months before publication.

## Status and sources

Status: **published** (finished 2018 publication; no living artefact). Bibliographic verification: LNCS vol. 11098 (portal record), pp. 305–324 (Crossref); DOI 10.1007/978-3-319-99073-6_15 is printed on the manuscript itself and Crossref-verified. Full text read: the **peer-reviewed author manuscript** (post-peer-review, pre-copyedit) from the University of Birmingham portal; wording may differ minutely from the final LNCS version.

## Related

- [UDS seed/key](concepts/uds-seed-key.md)
- [Lock It and Still Lose It](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md)
