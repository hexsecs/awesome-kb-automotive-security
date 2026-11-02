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

## [2026-11-01] deepen | Concept page: misbehavior detection in V2X (#27) + F2MD page correction pass

New concept page `wiki/concepts/misbehavior-detection.md`: the three-layer split (message security / plausibility detection / reporting-and-authority) with the insider argument sourced to TS 103 759's own definition (misbehavior = false content *using valid certificates*, faulty stations included) and TR 103 460 ("PKI based security would not be able to prevent such data semantic level attacks"); the framing correction that TS 103 759 standardizes the *reporting* service while detection mechanisms live in the TR 103 460 study; F2MD as the chain's one full implementation; the authority in both credential systems (ETSI MDM with its MA-unlinkability rule; US SCMS with split Linkage Authorities); and the source-named open problems (structural false positives, the privacy/revocation tension, store-and-forward latency, pseudonymity starving count-based detection). Research notes: kb-work/joyride-27-misbehavior-notes-{a,b}.md. The same pass corrected `wiki/f2md.md` against the F2MD code and the anchoring paper's full text (HAL hal-02527873): paper title/citation fixed (TVT 69(6), 6631–6643, DOI 10.1109/TVT.2020.2984878); the "two generations / binary ETSI-format report" claim replaced (reports are JSON on the authority path; V1/V2 are parallel chain configurations; the four forms follow the VNC 2018 three-container protocol); the "pluggable ideal detector" authority replaced with the shipped count-threshold rule the paper itself calls "a simple non intelligent method", reaction levels 0–4, no resolution broadcast; "pseudonymous certificates" replaced (no PKI in the artefact; synthetic-integer pseudonyms under six change policies; PKI is paper future work); attack naming aligned to the paper's 9 faulty behaviours + 6 attacks (19 local code types + MA Stress). `related` reciprocated on f2md, vanetza, v2verifier, artery, veins, van3twin.

## [2026-11-01] deepen | Concept page: V2X credential management (#28)

New concept page `wiki/concepts/v2x-credential-management.md`: the shared design problem of both V2X credential systems (authenticatable yet unlinkable; revocable yet private; the authorities themselves inside the threat model — the SCMS design's "at least two of its components need to collude" rule) and the split-knowledge answer both converged on. ETSI side from TS 102 941 V2.1.1 read firsthand: enrolment credential vs nameless Authorization Ticket (EU Certificate Policy numbers — ≤1 week validity, ≤60 parallel as a Sybil bound — flagged as Release 1 policy values, two TBD in the document itself; the ETSI TSs set no lifetimes), the EA/AA knowledge split ("separation of duties", cl. 5), the authorization protocol's blinding mechanics (keyTag HMAC + EC signature sealed to the EA; "the EA is not able to draw conclusions on the keys requested"), the two CTLs (TLM/ECTL for Root CAs vs RCA lists for its own authorities), and the three-tier revocation asymmetry (tickets never revoked — passive eviction by non-reissuance; ECs on the EA's never-published internal blacklist; published CRLs for CA certificates only). US side from Brecht et al. (IEEE T-ITS 2018, DOI verified): RA/PCA knowledge split with shuffled requests, butterfly key expansion and the PCA's blinding step, linkage values (lv = plv1 ⊕ plv2) making CRL revocation forward-only with backward privacy preserved, design parameters (1 week / ≥20 simultaneous / 1–3 years) labelled as design values against today's IEEE 1609.2.1-2022 operation. Closing section: across the KB's V2X entries the machinery exists only as an assumption (Vanetza fabricates but never enrols or requests; V2Verifier verifies only; VaN3Twin models containers without authorities; F2MD abstracts the PKI away entirely). Research notes: kb-work/joyride-28-pki-notes-{a,b}.md. `related` reciprocated on vanetza, v2verifier, van3twin, f2md and the misbehavior-detection concept page.

## [2026-11-01] deepen | #12 batch 1: seven landmark papers to full (2004–2011)

Wolf 2004 (bus systems), Raya & Hubaux 2007 (VANET security), Papadimitratos et al. 2008 (SeVeCom), Koscher et al. 2010, Rouf et al. 2010 (TPMS), Checkoway et al. 2011, Francillon et al. 2011 (PKES relay) taken from stub to full depth from the papers' full texts. All status unknown (finished publications). DOIs recorded where they exist (Raya & Hubaux, SeVeCom, Koscher — Crossref-verified); the USENIX/NDSS papers carry none and say so on the page. Anonymized vehicles and sensor systems are never named. Related links reciprocated on the can-injection, v2x-credential-management, misbehavior-detection, and uds-seed-key concept pages and on vanetza.

## [2026-11-01] deepen | #12 batch 2: immobilizer crypto + Miller & Valasek (2012–2015)

Four papers to full depth from their full texts: Hitag2 (Verdult, Garcia & Balasch, USENIX Security 2012 — an earlier draft attribution transposing the third authors of the two Radboud papers was caught in research and corrected against the title pages), Megamos Crypto (Verdult, Garcia & Ege, USENIX Security 2015; the injunction history is carried in a separately attributed passage resting on court reporting, not the paper), Miller & Valasek 2013 (named vehicles, released tools, the download-path execution result) and Miller & Valasek 2015 (the cellular-to-CAN Jeep chain; recall documented from the paper's own disclosure timeline). All status unknown; both white papers are identified as non-peer-reviewed, no DOIs anywhere in the batch. Related reciprocated on the can-injection concept page; the IVI update-trust link from the 2015 paper is one-directional by design, with the scoping stated on the page.

## [2026-11-01] deepen | #12 batch 3: six 2016 papers to full (CAN cluster + RKE + Uptane design)

Six papers to full depth from their full texts: Cho & Shin CIDS (USENIX Security 2016 — clock-skew ECU fingerprinting; no DOI, USENIX practice), Cho & Shin bus-off (ACM CCS 2016, DOI 10.1145/2976749.2978302 — error handling as a protocol-layer DoS that operates below checksums/MACs and content IDSs), vatiCAN (Nürnberger & Rossow, CHES 2016, DOI 10.1007/978-3-662-53140-2_6 — second-frame HMAC retrofit; its AUTOSAR comparison is carried as the paper's 2016 characterization, not present fact), Lock It and Still Lose It (Garcia, Oswald, Kasper & Pavlidès, USENIX Security 2016 — author list verified against the title page; the research brief's "Schmitt & Wollinger" attribution was wrong and is not used; VW global keys + the Hitag2 RKE correlation attack, a cloning break, not relay), LeiA (Radu & Garcia, ESORICS 2016, DOI 10.1007/978-3-319-45741-3_15 — per-ID keys, design-and-proof only, no implementation or measurements in the paper), and the Uptane design paper (Kuppusamy et al., escar Europe 2016 — kept consistent with the Uptane entity page and the secure-firmware-updates concept: the paper's "release" role is the standard's Snapshot, IEEE-ISTO 6100.1.0.0 belongs to the 2019 v1.0.0 edition only, and DOI 10.1109/MVT.2017.2778751 is a different 2018 publication and is not attached). All status unknown. Related links reciprocated on the Hitag2 and Megamos pages, the Uptane entity page, and the CAN injection concept page. Research notes: kb-work/joyride-12-batch3-notes-{a,b}.md.

## [2026-11-01] maintain | Populate `created` across all pages + ingester support

Every page in the KB now carries `created` (OpenShelf SPEC §4.2 — the date the page first entered the KB, set once, never changes). Backfilled from each file's first commit in this repo: 232 pages at 2026-10-31 (the bulk ingest and the first depth slices) and 7 at 2026-11-01 (five concept pages — secure firmware updates, SOME/IP, IVI update-path trust, misbehavior detection, V2X credential management — plus the two VehicleSec 2026 papers added by that day's list sync). All 239 pages covered: 230 entity pages and 9 concept pages. The ingester now manages the field: stamped from the source commit date when a stub is first created, preserved verbatim on every later rewrite (it joined `MANAGED_KEYS` and the generated frontmatter, between `last_checked` and `updated`). AGENTS.md records the rule for hand-written concept pages (author sets `created` at authoring) and the depth enum is updated to the SPEC §4.5 ladder (stub | brief | full | deep).

## [2026-11-01] deepen | #12 batch 4: six papers to full (2017–2018 — IDS, sensor attacks, CAN auth, diagnostics)

Six papers to full depth from their full texts, all DOIs Crossref-verified firsthand by the page author as well as in research: VIDEN (Cho & Shin, ACM CCS 2017, DOI 10.1145/3133956.3134001 — voltage-profile attacker identification that closes CIDS's aperiodic-injection gap; detail rests on the arXiv extended version, flagged on the page), WALNUT (Trippel et al., IEEE EuroS&P 2017, DOI 10.1109/EuroSP.2017.42 — acoustic injection against MEMS accelerometers, 15/20 models biasing-vulnerable, 13/20 control-vulnerable; the paper's own MIS2DH/MIS2DSH spelling discrepancy noted on the page), VulCAN (Van Bulck, Mühlberg & Piessens, ACSAC 2017, DOI 10.1145/3134600.3134623 — vatiCAN + LeiA implemented on Sancus under a fully-compromised-ECU adversary model; its Appendix A replay attack on vatiCAN's nonce renewal — 99% reuse after 36,000 renewals at k=15, ~30 minutes of traffic — stated at the paper's own strength and cross-linked from the vatiCAN page; the ~3% congestion figure is vatiCAN's, cited not measured, and the page says so), Illusion and Dazzle (Shin et al., CHES 2017, DOI 10.1007/978-3-319-66787-4_22 — VLP-16 only experimentally; saturation sector-blindness and closer-than-spoofer relay dots), GIDS (Seo, Song & Kim, PST 2018, DOI 10.1109/PST.2018.8514157 — figures are the arXiv preprint's, the proceedings text being shorter and not openly readable, flagged on the page; the conclusion's "100% average accuracy" claim is not repeated — the paper's tables govern), and Beneath the Bonnet (Van den Herrewegen & Garcia, ESORICS 2018, DOI 10.1007/978-3-319-99073-6_15 — the paper is NOT anonymized: Ford, Volvo, Fiat, Volkswagen/Audi named as the paper names them; three ciphers across four manufacturers; the uds-seed-key concept page's frontmatter now links it, closing the reciprocity gap research flagged). All status unknown. Related reciprocated on the CIDS, vatiCAN, and LeiA pages and on the can-injection and uds-seed-key concept pages. Research notes: kb-work/joyride-12-batch4-notes-{a,b}.md.

## [2026-11-01] deepen | Deep pilot: Koscher 2010 to depth deep + concept evaluation

The KB's first `deep` page (OpenShelf SPEC §4.5, ≤6,000 tokens, on-demand tier): Koscher et al. 2010 expanded from the paper's full text re-read end-to-end — experiment design in full (two-car differential protocol, the three settings, "at speed" defined as wheels at 40 MPH, the runway/chase-car protocol and its yank-cord safety measure), the Table I ECU map and the two-bridge architecture, CARSHARK's three forced capabilities, the DeviceControl fuzzing mechanics (CPID enumeration → random arguments → bit correlation), per-ECU results with the tables' qualifier patterns (BCM: all 15 effects at speed, none key-gated; ECM: all six key-gated, plus the ungated Table V kill and the forged airbag-deployed bit; EBCM: the stuck brake that survived battery removal, and the jack-stand-vs-runway unlock nuance), the composites (105-line radar-verified speedometer, Lights Out, self-destruct), the five-item standards-deviation cluster carried as its own section, and subnet bridging (1,184 B / 291 instructions, runway-verified self-wipe). Vehicle remains anonymized, payloads remain withheld — the paper's own line, kept.

The pilot also ran the owner's concept-evaluation directive (deep pages evaluate for new concepts for addition or update; eight candidates evaluated against the full corpus — notes kb-work/joyride-deep-koscher-concepts-b.md). Outcomes: two UPDATEs landed in this same PR — uds-seed-key gains "The measured baseline" (Koscher's brute-force arithmetic the concept prescribed against but never cited, the telematics hardcoded seed, the PAM constant 11 22 33, ford-ecu-bruteforcer as field evidence), and can-injection gains an "Access paths" section (its theft-model framing was narrower than the KB's own evidence: diagnostic-port attachment, compromised/bridged ECU, and CANflict's unmodified-MCU crafting now scoped, with which mitigations bind which path). Four ADDs filed as discrete issues: #42 diagnostic-service abuse (85/100), #43 CAN availability and denial of service (80/100), #44 in-vehicle intrusion detection and ECU fingerprinting (85/100; its VIDEN+GIDS build gate cleared by PR #41), #45 CAN message authentication — the retrofit design space (75/100; VulCAN build gate likewise cleared). Three DECLINEs with reasons recorded in the evaluation: gateway bridging/subnet pivoting (synthesis already lives in the entity pages; revisit triggers named), standards deviation (one paper's findings — carried as a section of the deep page instead), attack persistence/anti-forensics (a single corpus instance).

**Ingester fix in the same PR:** the rewrite path preserved bodies only for `depth: full` — a `deep` (or `brief`) page whose list entry changed would have had its authored body replaced by the stub body on the next ingest. The condition is now "any authored depth keeps its body; stubs are regenerated." Verified by a forced-rewrite test on a scratch copy: the deep page's entry was made stale, ingest rewrote it (1 updated), and the deep body and `depth: deep` survived intact.

## [2026-11-01] deepen | #12 batch 5: five survey-cluster papers to full (one deferred)

Five of the six survey-cluster papers to full depth from their full texts: Studnia et al. 2013 (DSN-W, DOI 10.1109/DSNW.2013.6615528, Crossref-verified — the field's 2013 map: six attack goals including owner-as-attacker electronic tuning, CAN's five missing properties, and the three-family countermeasure classification of cryptography / anomaly detection / software integrity that the KB's later pages keep instantiating; read from the HAL author manuscript), Miller & Valasek's remote attack surfaces survey (Black Hat USA 2014, 94 pp., no DOI — Crossref-checked; the three-stage anatomy, surface as explicit proxy, 6 of 14 (42%) of 2014 vehicles with no separation between a cyber-physical ECU and a remote-surface ECU, segmentation rarely a security boundary, and the detection-first defence the CAN-IDS pages later build on; its relationship to Checkoway 2011 stated as the survey itself presents it), Foster et al. 2015 (USENIX WOOT, no DOI — the aftermarket C4E dongle: unauthenticated debug console, the fleet-wide shared root SSH key recovered from a NAND dump, ~1,500–3,000 Internet-visible devices, and the unsigned, server-unauthenticated, attacker-chosen-server SMS update chain as the core break; the vendor's production claims printed unresolved against the team's evidence), Petit et al. 2015 (Black Hat Europe, no DOI — MobilEye C2-270 blinding, 650 nm laser most effective and non-recovering, ibeo LUX 3 relay and spoofing with the paper's own 20 m/40 m closer-than-attacker floors stated at the paper's strength), and the pseudonym-schemes survey (Petit, Schaub, Feiri & Kargl, IEEE COMST 2015, DOI 10.1109/COMST.2014.2345420, Crossref-verified — the five-phase pseudonym lifecycle, the four scheme categories with the §IX verdict, TS 102 941's preliminary state, and the CAMP design the credential-management concept page's SCMS descends from). All status unknown. Related reciprocated on the Checkoway, Raya & Hubaux, and SeVeCom pages and on the v2x-credential-management, misbehavior-detection, and can-injection concept pages; Foster's page links the can-injection concept (its payload is arbitrary CAN from an attached device) and deliberately not ivi-update-trust (a dongle is not an IVI unit, whatever the update-chain resemblance). Research notes: kb-work/joyride-12-batch5-notes-{a,b}.md.

**Deferred, on the record:** the sixth cluster paper, Petit & Shladover's *Potential Cyberattacks on Automated Vehicles* (IEEE T-ITS 2015, DOI 10.1109/TITS.2014.2342271, Crossref-verified), stays at stub depth. Its full text is paywalled at IEEE and no open copy exists (checked: Berkeley ITS page carries abstract + citation only; Semantic Scholar and OpenAlex mark it closed; Unpaywall/CORE/BASE/OpenAIRE hold no full text). A full page is not written from an abstract plus secondary reproductions — the research lane's attributed draft is preserved in the batch-5 lane B notes for the day the text is obtained. This landing clears two concept build gates: #59 (physical-channel sensor attacks — Petit et al. sensor experiments now full) and #58 (pseudonym change strategies update — the survey now full).

## [2026-11-01] deepen | #12 batch 6: the 2019 cluster to full

Four 2019 papers to full depth from their full texts. **CANvas** (Kulandaivel, Goyal, Agrawal & Sekar, USENIX Security 2019, pp. 389–405, no DOI — Crossref-verified): the nmap for the vehicle, and its first result is a correction to this KB's CIDS page — the published clock-skew estimators are period-dependent and fail as a mapping primitive; CANvas tracks pairwise relative offsets at the hyper-period instead (30 min of traffic, 0% false positives, 59 Prius IDs → 9 transmitters), and rebuilds the bus-off attack below the CAN controller as a dependable isolation step because the message-level formula's 0.025 ms jitter assumption fails against ≥0.15 ms measured on real cars. Two findings: a previously unknown ninth ECU in the authors' own Prius (an aftermarket plug-in battery conversion), and zero controller-level receive filtering on either ground-truthed car — reception, the precondition for injection's follow-on attacks, measured as universal. The paper contradicts itself on the Fiesta year (2013 vs '15); flagged on the page, not resolved. **Losing the Car Keys** (Baker & Martinovic, USENIX Security 2019, pp. 407–424, no DOI — Crossref-verified): CCS's single-ended PLC wiring (an IEC 61851 backwards-compatibility consequence) makes the cable an antenna and the OFDM waveform radiates as a replica — 54 sessions, 14 UK sites, six charger manufacturers, all leaking; CRC32-valid recovery 91.8% from the adjacent parking bay; plaintext SLAC delivered the NMK in 31 sessions; zero TLS in any observed session; EV ID + MAC in 41/54; AutoCharge's MAC-only billing as the theft path; the non-existent-PKI lesson and the ECDH-in-SLAC countermeasure. Scope kept explicit against the OCPP concept: this is the vehicle↔charger link only. **Fast, Furious and Insecure** (Wouters et al., TCHES 2019(3), pp. 66–85): the Pektron PKES in the Tesla Model S runs DST40, not the expected DST80 — the cipher broken in 2005, fourteen years on, protecting entry and start with one per-fob key; undocumented SPI commands recovered by busy-line fuzzing; unblown JTAG fuse; no mutual authentication, no security partitioning, unauthenticated RKE action byte; the practical clone = two elicited pairs + a 5.4 TB TMTO table, key in <2 s, ~$600 backpack platform, demonstrated on two Model S with consent. Scope beyond Tesla (McLaren/Karma/Triumph) carried strictly as the authors' unverified inference. The paper's DOI (10.13154/tches.v2019.i3.66-85) is printed in the paper and registered with DataCite but has no Crossref record — the page prints it with that caveat stated, an exception to the Crossref-first habit recorded here deliberately: the identifier is real and verified through its own registry. **Adversarial Sensor Attack on LiDAR-based Perception** (Cao et al., ACM CCS 2019, pp. 2267–2281, DOI 10.1145/3319535.3339815, Crossref-verified): the perception layer — first the clean negative (an improved spoofing rig, ~60 reliable points, and no blind configuration produced a single perceived obstacle in Apollo), then Adv-LiDAR (capability modelled as spatial transformations of a real trace; loss built from the post-processing's objectness×positiveness) reaching ~75% at the measured 60-point capability, all fakes classified as vehicles, plus the Apollo 3.0 Sim-control case studies; the paper's internal 30%-vs-18.9% inconsistency is not reproduced (the §8.1 figures are used). Reciprocation: Lock It, Hitag2, and Megamos pages and the WALNUT page gain the new slugs; can-injection gains CANvas; ocpp-charging-attacks gains Losing the Car Keys. Research notes: kb-work/joyride-12-batch6-notes-{a,b}.md.

## [2026-11-01] deepen | #12 batch 7: CAN error-handling + IDS cluster to full — first pages at status: published

Six papers to full depth from their full texts, and the first pages written under the new OpenShelf status convention (SPEC §9.2, openkb PR #30): finished publications carry `status: published`, not `unknown`. **Serag et al. 2021** (USENIX Security, no DOI — the group's AutoSec demo DOI belongs to a different work and is not attached): CANOX's three further error-handling vulnerabilities — passive error regeneration (14 recessive bits needed, 11 available), Single Frame Bus Off (TEC 0→256 in ≈5 ms vs the original's ≈36× slower 19 rounds; clutter stopped early sets TEC arbitrarily in 135–255), deterministic-recovery Persistent Bus Off, and error-state outspokenness mapping (aperiodic messages included); STS on an anonymized 2011 car, suppression EBCM 97.5 / BCM 91.4 / TCM 85 / ECM 83 (the paper's §6.2 prose swaps TCM/ECM against its own tables — the page follows the tables and the discrepancy is recorded in the research notes). **CANflict** (de Faveri Tron et al., CCS 2022, DOI 10.1145/3548606.3560618, Crossref-verified): peripheral pin conflicts as a software route to data-link-layer crafting from an unmodified MCU — SPI/UART full frames at 1 Mbit/s on all three platforms; the §5.4 targeted bus-off (×32 → TEC >255) with no periodicity assumption; positioned exactly as the can-injection concept's fourth access path and as an enabler, not an error-handling vulnerability. **Rogers & Rasmussen 2022** (arXiv preprint, no DOI): the stealth bus-off — interrupted error frames (+8 each) drive a victim to bus-off inside one message (≈600 µs) before any error frame completes; 38% flip accuracy → >99% success; blind synchronization to 100%; the EREF fix. Flagged on the page as analysis, not demonstration. **ROAD guide** (Verma et al., PLOS ONE 2024, DOI 10.1371/journal.pone.0296879, Crossref-verified; read from arXiv v3): the five-family taxonomy and timing-transparent/opaque axis; per-dataset verdicts on all six pre-ROAD datasets (OTIDS's mislabelled "impersonation," Car Hacking's stand-by gaps and parked-car train/test mismatch, SynCAN synthetic-only, TU/e hand-edited timestamps, Infector byte-level limits); ROAD itself — 33 dynamometer-verified attack captures, flam delivery, the zero-injection Accelerator Attack, 13 simulated masquerades (labelled simulated, as the guide insists), and its own stated drawbacks including no physical-layer data. **DUET** (Bhatia et al., NDSS 2021, DOI 10.14722/ndss.2021.23013, Crossref-verified): two colluding ECUs corrupt the voltage measurement itself (superposition → bimodal samples, classifier-independent), poison retraining one PREP bit at a time, then impersonate — 100% aggregate against Viden, 76%/message against Scission with ~1,000 messages to alarm; both of the paper's qualifications carried wherever the "every published VIDS" claim appears (VoltageIDS/SIMPLE/EASI argued, not measured; SIMPLE un-evadable if it never retrains); RAID defence (2^-18, success → 0%). **Lazeski et al. 2026** (VehicleSec '26 WIP, no DOI): decision-tree audit of five datasets — DoS/spoofing rules are single constants (Challenge F1 = 0.000 on its own changed patterns), fuzzing trees split on absolute timestamps, replay F1 54.7–76.4%, OTIDS file-level labelling, Car Hacking's 11 fuzzing-only benign IDs; "the bottleneck is dataset realism, not model choice," with the paper's own limitations (DT proxy, per-frame/binary scope) kept at full strength. The lane-B notes also record the detector-class assumption ledger for concept #44 and the datasets feed for the mining pass's deferred datasets concept (its revisit trigger — this guide reaching full — is now met; the concept itself remains a human/editorial call, not filed here). Reciprocation on the bus-off, CIDS, GIDS, and CANflict tool pages. Research notes: kb-work/joyride-12-batch7-notes-{a,b}.md.

## [2026-11-01] maintain | status: published adopted for the Research Papers category

Owner's call (2026-11-01): `status: unknown` on finished publications reads as "unverified/dubious" — the wrong signal. OpenShelf gained `published` for finished works (hexsecs/openkb PR #30, SPEC §9.2 + schema); this change adopts it here. (1) `tools/ingest.py`: new stubs in the Research Papers category are created with `status: published`; all other categories keep the `unknown` default. Existing pages are untouched by the change (ingest preserves `status` on rewrites, as before). (2) Backfill: all 59 Research Papers pages still carrying `status: unknown` now carry `published` — frontmatter on every page, plus the authored "Status: **unknown**" line in the Status-and-sources section of the 32 already-deepened pages, so frontmatter and body agree. (Batch 7's six pages were written directly at `published`.) (3) AGENTS.md records the rule. No content, depth, or link changes. Gates: ingest 0/0/0 twice after the backfill (the backfilled value survives ingest, confirming the preservation path), lint --strict clean.

## [2026-11-01] deepen | #12 batch 8: sensor/AV spoofing cluster to full

Six papers to full depth. **Dirty Road** (Sato et al., USENIX Security 2021, no DOI): DRP patches bend real lane detection on OpenPilot — ≥97.5% scenario success in ≤0.903 s against the 2.5 s reaction budget; 10/10 real-Camry collisions via trace injection (AEB never fired); the paper's own gap carried — no physical patch ever steered a real car. **Too Good to Be Safe** (Jing et al., USENIX Security 2021, no DOI): the mirror image — fake lanes *created* black-box on a paper-named Tesla Model S (HW 2.5, SW 2018.6.1) via a reverse-engineered GPU-memory oracle into Autopilot's `vision` binary; narrow-but-long stickers (1–5 cm) followed into oncoming traffic at a crossroads (5.1 m in 0.918 s); Tesla confirmed, declined to fix. **Invisible for both Camera and LiDAR** (Cao et al., IEEE S&P 2021, DOI 10.1109/SP40001.2021.00076, Crossref-verified): MSF-ADV — shape is the one property both modalities read; ≥91% evasion across all four Apollo/Autoware fusion combinations, printed cube detected in 1/108 frames, 100% LGSVL collision; the sequel that retires Cao 2019's "fusion, discussed not evaluated" defence, with rule-based-late-fusion-only scope markers. **Does Physical Adversarial Example Really Matter** (Wang et al., ICCV 2023, DOI 10.1109/ICCV51070.2023.00407, Crossref-verified): the system-level reality check — strongest published STOP-sign attacks produce **zero** system-level violations in a closed-loop pipeline (weakest inside the braking envelope, so the tracker never loses the sign); two design limitations (EoT's uniform sampling vs the pinhole 1/s² distribution; no plant/system model) and the SysAdv fix lifting violations 0% → 100% in several cells. The paper refutes the literature's *evaluation practice*, not the threat — the page says so in both halves. **Trajectory Prediction Attack** (Lou et al., USENIX Security 2024, no DOI): the first physical-world attack on trajectory prediction, launched indirectly — two placed cardboards flip a parked car's perceived heading (~π), so the predictor forecasts it into the victim's path; 63% prediction-space collision rate on nuScenes, 4–5/5 physical testbed trials ending in emergency braking; "collision rate" is flagged as a prediction-space metric in the dataset experiments. **On the Realism of LiDAR Spoofing** (Sato et al., NDSS 2025, DOI 10.14722/ndss.2025.230628, Crossref-verified): the line's sceptical audit — its survey table grades all predecessors stationary/≤5 km/h/≤10 m, none against an AD stack; the MVS rig (IR detection of the LiDAR's own 905 nm emission, servo auto-aim, ~$2.3k) + A-HFR (weak synchronization defeats pulse fingerprinting: 100% AT128, 96% XT32) succeed at 60 km/h from 110 m, with the first end-to-end spoofing of a stack-driven vehicle (Autoware crash + ghost-wall stop) — and the paper's self-stated gap: the stack runs were 5/15 km/h, night, closed course. Research-lane note: the task brief glossed Too Good to Be Safe as a LiDAR follow-up; it is a camera-channel lane attack, and the page follows the paper. The lane-B notes also record the mining-pass feed: the deferred "AV perception attacks" concept's revisit trigger (Cao 2019 full + one system-level paper full) is now **met** (Wang 2023, with Lou 2024 as a second system-level leg) — the build/wait call stays editorial, and the concept must remain downstream of the filed physical-channel concept (#59). Reciprocation on the Cao 2019 and Illusion and Dazzle pages. Research notes: kb-work/joyride-12-batch8-notes-{a,b}.md.

## [2026-11-01] deepen | #12 batch 9: EV/charging cluster to full

Six papers to full depth. **Plug-N-Pwned** (Wen, Chen & Lin, USENIX Security 2020, no DOI): DongleScope tested all 77 wireless OBD-II dongles on Amazon US (Feb 2019) on a real car — five vulnerability classes, every dongle exposing at least two; 84% with neither connection- nor application-layer authentication; 52/77 relaying undefined control frames; results stated as a lower bound. **Brokenwire** (Köhler, Baker, Strohmeier & Martinovic, NDSS 2023, DOI 10.14722/ndss.2023.23251, Crossref-verified): preamble-only CSMA/CA starvation of HomePlug Green PHY — 10 mW disrupts at 10 m while 20 W of broadband noise does nothing; 8 anonymized vehicles × 20 chargers, success in every combination, 47 m at <700 mW; the active/availability mirror of Losing the Car Keys' passive attack on the same wiring; CVE-2022-0878. **OCPPStorm** (Coppoletta et al., VehicleSec 2024, DOI 10.14722/vehiclesec.2024.23069, Crossref-verified): black-box stateful OCPP fuzzing of SteVe and OCPP.Core — correct-response rates ~22–58%, wrong-error rates to 75%, and every confirmed vulnerability from the state-machine fuzzer (server-crashing BootNotification, negative transactions, unauthorized termination). The paper's CVE count is internally inconsistent (abstract "5 confirmed + 7 under review" vs §IV "6 + 6"); the page follows the abstract figure, which matches the stub and the OCPP concept page, and flags the discrepancy. **Current Affairs** (Szakály, Köhler & Martinovic, USENIX Security 2025, no DOI): the first charger-side census — a portable EV emulator against 325 chargers / 26 manufacturers / 4 countries; only 12% offer TLS, 6% standards-compliant, zero mutual TLS, zero ISO 15118-20; development certs, key-log leaks, 32-bit NMKs at anonymized makers; the design flaw that charger certificates are unverifiable as to *which* station they belong to, with GPS-bound certs and leaf OCSP stapling proposed. **Charge It to My Neighbor** (Löw et al., VehicleSec 2026, no DOI): the PnC signature covers the challenge alone — no station identity — so three relayed application-layer messages bill a victim for the attacker's charge; positioned precisely against EVExchange (network-layer, co-located, both charging) and Baker & Martinovic (passive, MAC-only, no cryptography): encryption does not repair a missing *binding*. Context-binding fix proposed (EVSE-ID bytes inside the 16-byte challenge, backwards-compatible); manufacturers acknowledged the CharIN disclosure, saw no urgency. **Race to Charge** (Lee & Lee, VehicleSec 2026 short, no DOI): a manual threading audit of everest-core 2025.12.1 — 11 CVE-assigned flaws in three patterns (inconsistent locking 8/11 incl. an ASan-confirmed heap-use-after-free; non-atomic transitions; missing state validation — a delayed authorization response resurrecting `authorized` after RemoteStop, reproduced on a Raspberry Pi at 30/50/70 ms with the paper's own caveat that the trigger needs the MQTT/API plane, not CSMS alone). Both lanes' #54 feeds agree: the trust-chain concept now has a measured deployment baseline (the first hop mostly absent), its strongest structural claim (station identity unverifiable by design) confirmed from both directions, the encryption≠binding distinction, and a new endpoint layer (authorization finality as an implementation invariant). Lane A also flags that Plug-N-Pwned's landing meets the mining pass's separate declined "OBD-II dongle bridge" candidate's revisit trigger (load-bearing paper at full) — a parent-level call, recorded here and in the batch report, not filed. Reciprocation on the Losing the Car Keys, OCPP concept, and can-injection pages. Research notes: kb-work/joyride-12-batch9-notes-{a,b}.md.

## [2026-11-01] deepen | #12 batch 10: SoK/systematization cluster to full

Six papers to full depth. **Kicking CAN** (Serag et al.; read from arXiv:2510.02960v5, the NDSS 2027 proceedings version — the stub's "2025" is the arXiv v1 date): 150 papers systematized; three attacker archetypes; only two root causes unique to the CAN family (R4 error handling, R6 bit sampling) and no defence-gap cause unique to CAN; availability is the most exposed element bus-wide; replacing CAN does not fix it (CAN FD inherits everything; even an ideal bus leaves 6/14 attacks standing). Its printed DOI (10.14722/ndss.2027.230993) has **no Crossref record yet** — re-verified firsthand for this batch (HTTP 404); the page reports it as printed-in-paper, explicitly not Crossref-verified. **Stealing Cars** (Bianchi et al., VehicleSec 2025, no DOI): 35+ attacks, 13 defences, five classes; the bleakest finding is A3 — **none of the thirteen published defences is deployed in a real system** (an inference from public information, carried as such). One divergence is flagged on the page, not harmonized: the SoK calls Wouters et al.'s Model S break "DST80", while the KB's own Fast, Furious and Insecure page (from the TCHES full text) records DST40 — the page follows the primary paper. Its §5.3 supplies #55's family with a primary-sourced taxonomy (RollJam / RollingPwn / RollBack counter-state mechanics; Garcia's counter-window attack; the designed-in tolerance window as attack surface), and its landing formally meets the mining pass's immobilizer-crypto DECLINE revisit trigger — the lane's recommendation, recorded here: re-decide; if it converts to an ADD, scope it to the cross-cipher *technique* taxonomy and sequence it after #55 and #61. **SecV** (Kayondo et al., NDSS 2026, DOI 10.14722/ndss.2026.240106 Crossref-verified): TEE+HSM runtime provenance for EVN→IVN control traffic — "Uptane secures delivery; SecV secures provenance of live control traffic" — 6.5% geomean overhead on S32G3 hardware; the Ethernet path is a *proposed* redesign, not measured, and the page says so. **Zhang sensor SoK** (arXiv:2509.11120, no DOI — verified absent): SEPG error-propagation graphs over 121 papers; only 4/59 detection/localization attacks evaluated under fusion; 12 overlooked vectors, PoCs dataset-level only. Its §VII "38 categories" vs Table IV's 34 inconsistency is preserved on the page. **Khan Next Frontier** (EuroS&P 2026, pp. 281–300, DOI 10.1109/EuroSP68448.2026.00028 Crossref-verified — the stub undersold it as arXiv-only): 48 studies; input-level 41/48, fusion-stage 6/48, ~75% no/narrow defence; its PoC (phantom pedestrian 0.74 vs 0.43) is a simulation of sensor *outputs* and the page carries the paper's own physical-limitations list so the figure cannot be quoted beside physical results. With both SoKs full, the deferred AV-perception concept's systematizing base is complete (lane B's mapping: layer model from Zhang, prevalence counts from Khan; the concept stays downstream of #59). **DefenseWeaver / Automating Function-Level TARA** (Yang et al., NDSS 2026, DOI 10.14722/ndss.2026.231408 verified two ways): LLM function-level TARA — OpenXSAM++ atoms, three agents, LoRA-for-generation/RAG-for-scoring split with a stated failure case; 11 pen-test-confirmed paths in four anonymized projects. Its feed revises #56's scope at build time: add the vehicle-vs-function granularity axis (the BCM A/B pair) and make automation a three-pole spectrum. Reciprocation on the autotara, avcdl, CANOX, CANvas, key-fob-relay, and IVI-update-trust pages. Research notes: kb-work/joyride-12-batch10-notes-{a,b}.md.

## [2026-11-01] deepen | #12 batch 11: keyless-entry + localization clusters to full

Four papers to full depth. **My Other Car Is Your Car** (Wouters, Gierlichs & Preneel, TCHES 2021(4), DOI 10.46586/tches.v2021.i4.149-172 Crossref-verified): the Model X break — the cryptography (EAL5+ Secure Element) is never attacked; the CC2541 asked the SE to verify the fob firmware signature and **ignored the SE's error status words**, so arbitrary firmware ran, the APDU blocklist was patched out, and unlock tokens were spent at will; the pairing protocol's second flaw is structural (provisioning certificates are never sent to the car, so provisioning is skippable — a simulated-SE fob pairs to any car). Classed on the page as *enrolment abuse*, a third outcome beside relay and cloning. Tesla's 2020.48 fix works by honouring the check that existed all along; the pairing and wake-up flaws were not fixed in that update. The stub's "firmware downgrade" wording is imprecise vs the paper's unauthenticated-update mechanism — summary preserved verbatim per house rule, body follows the paper. **RollBack** (Csikor et al., Black Hat USA 2022 / ACM TCPS 2024, DOI 10.1145/3627827 Crossref-verified; page follows the arXiv text, journal version paywalled): the resync state machine exactly as documented (single window <16; double window storing counter l, resync only on l+1; blocked beyond), the variant space (#SIGNALS 2/3/5, strict/loose, 5 s/8 s/unbounded), the full Table 2 record including the negatives (TI-based Toyotas uniformly immune; two NXP systems immune — a receiver-implementation property, not a rolling-code universal), ~100-day-old signals validated, instruction-agnostic with re-locking, and the KeeLoq learning-process root-cause hypothesis carried **with the paper's own five objections** — NXP PSIRT confirmed receiver-side vulnerability, mechanism unproven. This removes #55's caveat: its resync-abuse member now rests on the primary paper, not tool pages and secondary accounts. **Drift with Devil** (Shen et al., USENIX Security 2020, no DOI): MSF localization under GPS spoofing — the baseline is genuinely reassuring (71% of upper-bound windows under 50 cm) until the **take-over effect**: in unconfident periods the state migrates until truthful LiDAR measurements are the rejected outliers and spoofed GPS is the only source; FusionRipper ≥97% off-road at a 2-minute window; offline profiling recovers mid-80s at half a day's cost. **All Your GPS** (Zeng et al., USENIX Security 2018, no DOI): stealth via route-shape matching — a ghost location whose route reproduces the victim's turn pattern, so every instruction is physically executable; wrong-way routes for 599/600 trips; 38/40 study participants fooled through all rounds, the two detectors catching exactly the inconsistencies the paper's §8 names as the promising defence channel (vision cross-checks). The paper's intro (1,547 routes/trip) vs §6.2 (335/3,507) discrepancy is flagged, §6.2 used. Lane B's #59 feed qualifies the concept's "defences are physical" framing: GNSS has no conditioning-chain fix (the flaw is the unauthenticated civilian signal design), and Shen shows the deployed estimator-level defence *becoming* the attack mechanism — the feed proposes a third axis for the build (where the defence sits: conditioning chain / estimator / human operator). Reciprocation on the Stealing Cars, Zhang SoK, and key-fob-relay pages. Research notes: kb-work/joyride-12-batch11-notes-{a,b}.md.
