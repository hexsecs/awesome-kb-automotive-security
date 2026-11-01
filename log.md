# Log

Append-only activity log for this KB (OpenShelf convention).

## [2026-10-31] init | KB created, bulk ingest of the source list

Created the KB and ingested hexsecs/awesome-automotive-security@b7b92a7:
228 entity stubs plus generated indexes, under a home-grown pilot spec.

## [2026-10-31] ingest | Retrofit to OpenShelf v0.1

Converged the pilot onto the OpenShelf standard (hexsecs/openkb): kb.yaml
manifest, wiki/ layout, OpenShelf page frontmatter (summary ≤160, verbatim
list text in body + list_summary), generated index.md + per-category
sub-indexes, AGENTS.md maintainer schema. Removed the parallel inventions
(sources.yaml, index.json, llms.txt, SPEC.md-as-format) — the format lives
in OpenShelf; local rules live in AGENTS.md. Verified with openshelf lint.

## [2026-10-31] deepen | CAN Bus Analysis depth slice + four concept pages

Deepened all 28 CAN Bus Analysis entity pages from stub to full (what it
is / how it works / where it fits / limits, `related` links, primary
sources checked 2026-10-31). Status calls from that check: CANalyse and
Kayak are `archived` (their repositories are archived); CANter stays
`unknown` (paper proof-of-concept, no released artefact). Added four
concept pages under `wiki/concepts/`: CAN injection, UDS seed/key
(SecurityAccess), key-fob relay attacks, and OCPP/charging attacks —
defensive, architecture-level synthesis cross-linked to the entity and
paper pages. Ingester updated to preserve unmanaged frontmatter and full
bodies across syncs and to list concept pages in the L1 index; verified
idempotent (0 created / 0 updated / 0 tombstoned) and `openshelf lint
--strict` clean. Landed by PR per the depth rule in AGENTS.md.

## [2026-10-31] deepen | Diagnostic Tools depth slice (issue #2)

Deepened all 19 Diagnostic Tools entity pages from stub to full (what
it is / how it works / where it fits / limits, `related` links, primary
sources checked 2026-10-31). Status calls from that check: most tools
are active; ford-ecu-bruteforcer, pq-flasher, uds-server, and udsim are
`maintenance` (dated or sparse recent activity); conescan and
uds-firmware-extraction stay `unknown` — conescan's README is empty and
its docs unreachable, so its page records source-tree evidence only and
says so, and uds-firmware-extraction has two commits from its creation
day. Gallia's research-only damage warning, Atlas's brick warning, and
pq-flasher's steering warnings are quoted on their pages. Landed by PR
per the depth rule in AGENTS.md.

## [2026-11-01] ingest | Sync to list 61ba124 + ingester identity fix

The list's 2026-10-31 merges (EVerest URL move, two VehicleSec 2026
papers) exposed two ingester flaws: identity was URL-only, so the EVerest
move tombstoned the page and created a duplicate, and every page was
rewritten whenever the source commit changed (last_checked re-stamped
without any verification). The ingester now matches by slug when a URL
moves, rewrites only pages whose own entry data changed, never moves
last_checked, and keeps tombstoned pages listed in their sub-index so
they stay reachable. This sync: 2 created (the VehicleSec papers),
1 updated (everest URL, in place), 0 tombstoned; re-run is 0/0/0.
## [2026-11-01] deepen | EV Charging Security depth slice (issue #3)

Deepened all 11 EV Charging Security pages from stub to full, with
what-it-is / how-it-works / where-it-fits / limits sections and primary
sources checked 2026-11-01. Documentation links are pinned to the checked
upstream commits. Added reciprocal sibling links, links back to the OCPP
charging-attacks concept, and reciprocal related metadata on the existing
OCPPStorm paper stub (its research depth remains for issue #12).

Status calls: 10 active (unarchived with observed 2026 default-branch
updates); OpenV2G maintenance (unarchived, latest checked commit is the
2025-11-12 import of 0.9.6, whose README records incremental fixes).
Maintenance is an editorial classification, not an upstream retirement
claim. No checked repository is archived. Each page records its evidence.

Limits retained explicitly: AcCCS's conflicting DIN-only versus newer
ISO/TLS/Plug & Charge instructions; dsV2Gshark's preliminary -20 support
and test-secret requirement; EmuOCPP's missing 1.6 transactions and stale
setup paths; OpenV2G's version-specific decoder fixes; WWCP's opt-in trust
roots, absent revocation checks and parent-checkout dependency; EVerest's
EvseV2G deprecation and configuration-dependent TLS/protocol behaviour.
No physical charging or security tools were executed.

Validation: full-tree ingest against the canon snapshot 61ba124 is
idempotent (0 created / 0 updated / 0 tombstoned); OpenShelf lint --strict
is clean; related links and pinned source endpoints were checked. The
shell proxy was unavailable, so repository and primary-source reads used
the GitHub connection; lint used the unmodified OpenShelf implementation
retrieved from hexsecs/openkb. One PR for this depth slice, per AGENTS.md.

## [2026-11-01] deepen | RF and Key Fob Analysis depth slice (issue #4)

Deepened all 6 RF and Key Fob Analysis pages from stub to full, with
what-it-is / how-it-works / where-it-fits / limits sections and primary
sources checked 2026-11-01. Added reciprocal sibling links and links to
the key-fob relay concept page from every page, keeping relay distinct
from cloning and from replay throughout, as the concept page does.

Status calls: Flipper Zero active (firmware 1.5.1, 2026-10-15; push
2026-10-30); Flipper-ARF active (dev builds only, latest push
2026-10-30); Proxmark3 active (Iceman fork canonical — the old
repository's README declares itself unmaintained; release v4.23346,
push 2026-10-30); rtl_433 active (release 25.12; commit 2026-10-27);
KAT maintenance (eight releases to v1.3.0 on 2026-06-24, no commits
since); URH archived (repository archived by its owner 2026-03-29;
final release v2.10.0). Each page records its evidence.

Corrections and limits retained explicitly: KAT's list summary
overstates its hardware support — Flipper Zero is an import/export file
format for KAT, not capture/transmit hardware, and its demodulator is
AM/OOK only (no FM/2FSK); KAT's licence is BSD-3-Clause with a
no-military/no-government rider. Proxmark3's primary sources document
Hitag and EM4x70 (ID48/Megamos) chip support but do not themselves use
the word immobilizer, and document no relay function. Flipper Zero
official firmware decodes dynamic (rolling-code) protocols but disables
saving them. URH's linked user guide (v1.1, for v2.0) predates its
final release. No RF hardware was executed.

## [2026-11-01] deepen | Firmware and ECU Reverse Engineering depth slice (issue #5)

Deepened all 7 Firmware and ECU Reverse Engineering pages from stub to
full, with what-it-is / how-it-works / where-it-fits / limits sections
and primary sources checked 2026-11-01. Added reciprocal sibling links,
plus links to the UDS seed/key concept from pyXCP and Simos18_SBOOT.

Status calls: pyA2L active (release v0.15.2, 2026-10-21) and pyXCP
active (release v0.26.3, 2026-10-23), both by the same author;
ghidra_v850 maintenance (packaged releases ended at v0.0.9 in 2023,
occasional P-code fixes since, latest commit 2025-04-27); ghidra-tc1797
unknown (two commits, 2020 snapshot); medc17-checksum-tool unknown
(single commit, 2025-08-12, no licence file); Simos18_SBOOT unknown
(finished research artefact, content-complete 2021-07-16);
TC1791_CAN_BSL unknown (single commit, 2020-12-06).

Corrections and limits retained explicitly: the medc17 list summary
claims RSA signature regeneration; the README states the opposite (the
private keys are not public) and the page follows the README. The
TC1791_CAN_BSL list summary's "arbitrary flash and RAM read/write"
end-state is the SBOOT workflow's outcome, not a claim in that
repository's README; the SBOOT README also names its companion
"TC1767_CAN_BSL" where the listed repository is TC1791_CAN_BSL — both
flagged in-page as unverified from primary sources. pyXCP documents no
dedicated flash-programming routine (flashing rests on generic memory
programming), and pyA2L upstream describes A2L import into a database
rather than parsing per se.

Uptane assessment (per issue #5): a concept page on secure firmware
updates IS warranted — Uptane has an entity page and a paper page in
different sections, and this slice adds the failure side of the same
problem (signed-boot chain failure in Simos18_SBOOT, the signature
boundary in medc17-checksum-tool). Filed as its own issue rather than
growing this one, per the issue's instruction. No ECU was connected and
no firmware was processed.

## [2026-11-01] deepen | Hardware Interfaces depth slice (issue #6)

Deepened all 8 Hardware Interfaces pages from stub to full, with
what-it-is / how-it-works / where-it-fits / limits sections and primary
sources checked 2026-11-01. Added reciprocal sibling links across the
section.

Status calls: panda active (commits to 2026-10-30) and RAMN active
(release v2.3, 2026-07-31); candleLight_fw maintenance (latest release
2021, occasional fixes since); SuperCAN maintenance (release v1.2.3,
last push 2025-01-14); CFUC maintenance (irregular commits to
2026-05-17, no releases or licence file in the firmware repo); CANtact
maintenance on a split record — the listed cantact-app repository was
archived by its owner 2025-04-06 with development moved to a successor
Rust application, and cantact-fw is unarchived but quiet since
2024-05-24; CAN-DAQ unknown (repository created 2025-05, latest commit
2025-05-25, no releases; design fixed by a HardwareX paper); OWASP
Automotive EMB 60 unknown (incubator stage, project page last updated
2022-03-12, founding repository quiet since 2022-08, never marked
archived).

Corrections and limits retained explicitly: CFUC's SocketCAN story is
gs_usb kernel driver on Linux plus a socketcand-style bridge daemon for
its Python path, not a native SocketCAN driver of its own; SuperCAN's
firmware does not support CANtact/candleLight-class hardware despite an
older same-name Windows driver for that hardware; EMB 60's SBC and CAN
board MCU are not pinned in its primary sources (the page says so
rather than repeating the summary's certainty); CAN-DAQ is classic CAN
only (ESP32-S3 TWAI) with no documented frame transmission. No hardware
was built, flashed, or run.

## [2026-11-01] correct | Slice 5/6 correction pass (15 pages)

The full primary-source research notes for the Firmware/ECU RE slice
(issue #5) and the Hardware Interfaces slice (issue #6) arrived after
PRs #17 and #19 had merged; the pages had been written from partial
notes. This pass rewrites the 15 affected pages from the full notes.
Slice #4 (RF and Key Fob) full notes match what landed — no changes.

Status changes: medc17-checksum-tool unknown -> active (repo created
2025-11-20, commits through 2026-08-27, MIT); TC1791_CAN_BSL unknown
-> maintenance (intermittently active, pushed 2026-08-02 after a
2022-2026 gap); candleLight_fw maintenance -> active (pushed
2026-10-02, commits through Sep 2026); CANtact maintenance -> unknown
(neither repo is archived — the earlier "archived 2025-04-06" claim was
wrong; original app/fw dormant since 2016/2017 HEAD commits, living
continuation in linklayer/cantact + candleLight_fw + CANtact Book);
SuperCAN maintenance -> active (commit 2026-10-27, release v1.0.28).

Major factual corrections: ghidra-tc1797 is a pspec + ldefs add-on to
Ghidra's built-in TriCore support (not a SLEIGH spec, no licence,
created 2024-04-20); ghidra_v850 is MIT, source-only distribution, no
releases ever, language defs v0.1; medc17 README does carry the
"Bleichenbacher signatures" bullet (mechanism undocumented) and the
tool also corrects CVN; pya2l's PyPI package is pya2ldb at 1.0.355,
licence record conflicts (GPL-2.0 metadata vs LGPL v3+ badge); pyxcp is
LGPL-3.0 at v0.28.0 and its README does document programming building
blocks; Simos18_SBOOT's CRC flaw pays off in boot-password recovery
(not a direct flash-read primitive), last commit 2022-03-18, and the
TC1767 naming wrinkle was wrong; CAN-DAQ is CC-BY-4.0, USB-UART wired
(no WiFi), transmits, MCP2561, HardwareX e00743 (2026); candleLight
licences are MIT/BSD/SLA0044, only release v2.0, F103 impossible,
G0B1/G431 unsupported; CFUC hardware+firmware share one repo under
LGPL-3.0 with two exclusive firmware flavours (CDC + cfuc plugin, or
the gs_usb budgetcan port); EMB 60's documented board is an
ATSAME70N21B design with 2x MCP2562FD and a documented secure
bootloader, but no source repository exists; panda's safety policies
live in opendbc, default mode is silent, no releases ever (the 0.0.10
header claim dropped as uncorroborated); RAMN ECUs are STM32L5 with
A=gateway/B=chassis/C=powertrain/D=body roles, releases v1.0.x (no
"Marlow"), terminated bus must not connect to a real car; SuperCAN's
Linux SocketCAN is a separate DKMS driver, its python-can plugin is
Windows-only. No hardware was built, flashed, or run.
