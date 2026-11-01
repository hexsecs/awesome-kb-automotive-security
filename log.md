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

## [2026-11-01] deepen | Secure firmware updates concept page (issue #18)

New concept page wiki/concepts/secure-firmware-updates.md synthesising
how automobiles are supposed to receive software securely, built around
Uptane: the Standard's threat model (either-repository compromise,
rollback, freeze, mix-and-match, partial bundle installation), the
Director/Image two-repository design with TUF roles, per-ECU signed
vehicle version manifests, full vs partial verification with the
no-verification-no-OTA floor, and the paper's compromise ladder
(reported as the design team's own analysis).

Corrections to the framing the issue inherited: IEEE-ISTO 6100.1.0.0
is the 2019 v1.0.0 edition only; the current Standard is v2.1.0
(2023) under the Linux Foundation's Joint Development Foundation.
Deployment record stated thin, as the project's own Adoptions page
leaves it: AGL/aktualizr, HERE OTA Connect, Airbiquity OTAmatic,
Foundries.io (partial), Torizon — no automaker, model, or production
deployment named, and none claimed here. The UNECE R156 relationship
is recorded as an engineering fit for the delivery-protection layer
only; no source states Uptane is required or endorsed under R156.

Reciprocal related links: uptane and the Uptane paper page
(frontmatter), Simos18_SBOOT, TC1791_CAN_BSL, and
medc17-checksum-tool (frontmatter + Related sections). Primary
sources only, retrieved 2026-11-01.

## [2026-11-01] deepen | Penetration Testing depth slice (issue #7)

All 11 Penetration Testing pages to full: AutoFuze,
automotive-security-research, CANHack, Car Toolkit, DongleScope,
NullSec CarFuzz, PiCCANTE, pwnobd, SecOC Key Extractor, tesla-opener,
TruckDevil. Written from full primary-source research notes gathered
before any page was drafted, with every status call re-verified
firsthand against the GitHub API at write time.

Status calls (checked 2026-11-01): PiCCANTE active (latest commit
2026-01-26, releases incl. v0.0.1 and rolling dev-latest); TruckDevil
active (latest commit 2026-09-05); AutoFuze maintenance (2024-01-18);
CANHack maintenance (2024-04-01); NullSec CarFuzz maintenance (created
2026-01-25, six commits, latest 2026-04-04); pwnobd maintenance
(latest commit 2025-09-23, release 0.1.0 of 2024-08-28); SecOC Key
Extractor maintenance (latest commit 2025-03-04); automotive-security-
research unknown (commits end 2019-05-26); Car Toolkit unknown (all
25 commits in a two-day burst ending 2023-10-30); DongleScope unknown
(NOT archived — archived flag verified false despite the 2020-07-27
last commit; finished USENIX Security 2020 artefact); tesla-opener
unknown (latest commit 2023-03-14).

Precision points kept in-page rather than smoothed over: AutoFuze's
SPI support is aspirational in its own README matrix; CarFuzz's README
and USAGE.md document two different CLIs and its deeper claims rest on
a three-file codebase; DongleScope's fuzzing-test danger warning is
quoted from its README; the SecOC extractor's confirmed vehicle scope
is only the two models its README lists.

## [2026-11-01] deepen | Automotive Ethernet depth slice (issue #8)

All 6 Automotive Ethernet pages to full: eth-ws-someip, ICS CAP,
ProtoCrawler, Scapy, someip-protocol-fuzzer, vsomeip. Written from
full primary-source research notes gathered before any page was
drafted, with every status call re-verified firsthand at write time
(GitHub API for the four repositories; the vendor download index
re-read for ICS CAP; CyTAL site liveness re-checked for ProtoCrawler).

Status calls (checked 2026-11-01): Scapy active (release v2.8.0,
2026-10-02; head commit on the check date); vsomeip active (five
releases in six months, latest 3.7.6 on 2026-09-17); ICS CAP active
(vendor download index, latest 26.2.1 dated 2026-05-08); ProtoCrawler
active (vendor site live, posts dated May 2026); eth-ws-someip
maintenance (releases ended 2019, but a dissector fix landed on master
2025-06-22 after a ~5.5-year gap); someip-protocol-fuzzer unknown (no
commit, release or tag since 2022-04-20; finished proof-of-concept).

Precision points kept in-page: Scapy's list-claimed FlexRay support is
not corroborated as a dedicated automotive layer (only an IEEE 1722
AVTP encapsulation header), so the page states the narrower fact;
ProtoCrawler's SOME/IP/DoIP/UDS/AVB coverage rests on the vendor's
vertical blog post and is absent from its formal supported-protocols
library page, and the page says so; icscap standalone is capture +
Lua only, with SOME/IP analysis and fuzzing credited to the
icscap + Vehicle Spy pairing as the vendor's own split draws it;
eth-ws-someip's AUTOSAR generation wording differs between the repo
description (4.2) and README (CP & AP, Foundation 1.5.0) and both are
preserved; vsomeip's "reference implementation" and production-ECU
framings are the list's wording, not upstream's, and the page flags
that. The slice's concept-page assessment: SOME/IP is warranted as a
concept page (touched by 5 of 6 section entries plus AutoFuze, with
shared SD/method/event vocabulary no page defines) — filed as its own
issue per the slice instructions rather than built here.

## [2026-11-01] deepen | Infotainment and IVI depth slice (issue #9)

All 6 Infotainment and IVI pages to full: byd-dolphin-hacking,
Chimaera, gen5fw, ic1101, MMI3G-Toolkit, Q50 Reverse Engineering.
Written from full primary-source research notes gathered before any
page was drafted, with every status call re-verified firsthand
against the GitHub API at write time (Chimaera is a journal paper;
its bibliographic facts were verified against Springer + Crossref).

Status calls (checked 2026-11-01): MMI3G-Toolkit active (360 commits
since 2026-04-14, latest 2026-09-24, three releases); byd-dolphin-
hacking active (174 commits since 2026-05-07, latest 2026-10-07);
Q50 Reverse Engineering active (created 2026-09-15, latest commit
2026-10-24); ic1101 maintenance (2023 burst, near-quiet stretch, then
a 22-commit burst Jan-Jun 2026, latest 2026-06-13); gen5fw
maintenance (latest 2025-01-08, maintainer merging community PRs);
Chimaera unknown (finished peer-reviewed publication, May 2024, no
public code repository).

Precision points kept in-page: Chimaera's tools are described in its
paper, not downloadable, and the page says so; gen5fw's fleet-wide
hardcoded AES key/IV and CRC32-only manifest are stated as the
finding; ic1101's trusted key is the public AOSP test key; the MMI
FSC bypass is a 2-byte patch to the user's own unit binary, not key
recovery; Q50's EPK signature/verification boundary is explicitly
unmapped in its source and stays unmapped on the page; BYD's
CVE-2025-24132 identification is attributed to the repo. Concept
assessment from this slice: all six entries defeat or probe an IVI
update/package trust anchor by a different mechanism — filed as its
own concept-page issue rather than built here.

## [2026-11-01] deepen | V2X Security depth slice (issue #10)

All 6 V2X Security pages to full: Artery, F2MD, V2Verifier, VaN3Twin,
Vanetza, Veins. Written from full primary-source research notes
gathered before any page was drafted, with every status call
re-verified firsthand against the GitHub API at write time.

Status calls (checked 2026-11-01): Vanetza active (head commit dated
the check day itself; v26.09 2026-09-08); Veins active (veins-5.4
2026-10-29); VaN3Twin active (head 2026-10-06); Artery active (latest
2026-07-30, no releases ever); F2MD maintenance (substantive code
ends Sept 2022, README-only after); V2Verifier maintenance (v3.0.1
2023-08-15, commits end 2024-11-04).

Precision points kept in-page: F2MD and Artery have no code
dependency in either direction; V2Verifier's C-V2X support is removed
in the current line and its master is mid-redesign per its own
README, so the list description is historical there; VaN3Twin's
security is signing-only with encryption unimplemented and no
TS 103 097 conformance claim; Vanetza's 1609.2 ASN.1 presence is not
a 1609.2 implementation, and its self-declared gaps (no CRL checks,
no enrolment) are stated; Veins core verifiably has no 1609.2/103 097
security implementation. Concept assessment: misbehavior detection
and the V2X PKI/trust model both recur undefined — filed as their own
concept-page issues rather than built here.

## [2026-11-01] deepen | Security Analysis depth slice (issue #11)

All 6 Security Analysis pages to full: Automotive Threat Matrix,
Automotive Threat Modeling Template, AutoTARA, AVCDL, Security
AutoDesigner, Uptane (entity). Written from full primary-source
research notes gathered before any page was drafted, with every
status call re-verified firsthand at write time.

Status calls (checked 2026-11-01): Automotive Threat Matrix active
(live site, Feb 2025 white paper, Vultara maintenance); AutoTARA
active (commits 2026-10-24, alpha release Aug 2026) — both halves
stated: it is a self-described research prototype; Security
AutoDesigner active (commercial, vendor site current into 2026);
AVCDL maintenance (4.18.6, 2024-05-07, core declared complete);
Uptane maintenance (Standard v2.1.0 current, no release since
Jun 2023, implementation upkeep continues); NCC threat-modeling
template unknown (finished artefact, unchanged since v1.2,
Sept 2017).

Precision points kept in-page: AVCDL's TUV SUD assessments cover
ISO/SAE 21434 and UN R155 only — 24089/R156 were still in progress
at last repo state and are not upgraded; ATM's technique count is
not stated by Auto-ISAC and the third-party ~80 figure is not
imported; AutoTARA's two-TARAs distinction (MITRE TARA vs ISO 21434
TARA) is kept explicit; Security AutoDesigner's thin public
documentation is stated as the finding, with all quantitative claims
attributed to the vendor; the Uptane entity page carries the
artefact record (governance, versions, implementations — including
the archived pre-1.0 reference implementation named as a trap, and
the Scala services' automated-update pushes characterised as such)
and points to the secure-firmware-updates concept page for the
design rather than duplicating it.

## [2026-11-01] concept | SOME/IP and SOME/IP-SD concept page (issue #23)

New concept page wiki/concepts/someip.md at full depth, written from
two primary-source research lanes: protocol mechanics from the
AUTOSAR PRS texts (FO 1.5.0 bundled in eth-ws-someip, cross-checked
against R20-11 and R23-11 editions; E2E cited to R20-11) and
service discovery + security surface from the SD PRS, vsomeip's
configuration documentation and the SecOC SWS (R24-11).

Centrepieces kept precise: the SD specification's single security
requirement (PRS_SOMEIPSD_00656, a subnet-topology check on
advertised addresses) is quoted in full; the attack consequences
(rogue Offer with specified overwriting of preconfigured endpoints,
forged Stop Offer deleting subscriptions on both sides, Nack reasons
containing no authorisation decision) are each read off specified
mechanics; E2E is fenced as a safety CRC mechanism with no
authentication; the SecOC boundary is stated exactly (whole
SomeIpTp message as a PDU, nothing SOME/IP-native, nothing for SD);
vsomeip's opt-in security is local-IPC only and off by default.
Version traps recorded on the page: TP_RESPONSE/TP_ERROR are
0xA0/0xA1 (the FO 1.5.0 table's 0x23/0x24 contradicts its own flag
rule); ACK message types appear in no PRS table checked and are
flagged as implementation extensions; 30490 is SD's port, not
SOME/IP's. Related links reciprocated on all seven entity pages.

## [2026-11-01] concept | IVI update-path trust concept page (issue #25)

New concept page wiki/concepts/ivi-update-trust.md at full depth,
written from two research lanes over the KB's own verified pages:
(A) the six IVI platforms' trust anchors, (B) the wider KB evidence
and the defensive contrast. The taxonomy has seven classes — no
check at the gate; the trusted key is public; one key for the whole
fleet; integrity without authenticity; the check is patchable in
the trusted binary; the trusted binary leaks its own key; and the
open case, verification boundary unmapped (Q50). Precision kept:
BYD's package signature check is not claimed bypassed (its failure
is caller authorisation + a disengaged bootloader); MMI's two
anchors (FSC RSA patch, format CRC32) are kept distinct; gen5fw's
build.prop-derived zip password is recorded as adjacent, not a
class; Chimaera's CVEs are listed unitemised, as the paper leaves
them. The ECU-side evidence (Simos18 SBOOT/ASW, VW_Flash) is folded
in as reinforcement with the layering axis (present-and-holding /
present-but-patchable / absent-or-public), and the delivery split
is stated as the survey found it: removable media on the IVI side,
the diagnostic bus on the ECU side. Uptane is a pointer paragraph
only — the design detail stays on secure-firmware-updates — with
the deployment-reality caveat attached. Related links reciprocated
on the six IVI pages plus simos18-sboot and vw-flash; the page body
sits inside the OpenShelf L2 budget.
