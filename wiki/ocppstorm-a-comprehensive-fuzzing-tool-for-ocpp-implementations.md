---
uid: 01a19d3c-afb3-7611-b994-2c3a90ad7c8d
title: "OCPPStorm: A Comprehensive Fuzzing Tool for OCPP Implementations"
summary: "Coppoletta et al., VehicleSec 2024. Black-box fuzzer for the OCPP charging-station protocol that tests implementations regardless of platform or language…"
type: entity
category: "Research Papers"
url: "https://www.ndss-symposium.org/ndss-paper/auto-draft-457/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Coppoletta et al., VehicleSec 2024. Black-box fuzzer for the OCPP charging-station protocol that tests implementations regardless of platform or language, and found five confirmed CVEs in two open-source OCPP systems."
related: [checkocpp, emuocpp, ocpp-charging-attacks, everest]
sources:
  - url: "https://www.ndss-symposium.org/ndss-paper/auto-draft-457/"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.14722/vehiclesec.2024.23069"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
---

Coppoletta et al., VehicleSec 2024. Black-box fuzzer for the OCPP charging-station protocol that tests implementations regardless of platform or language, and found five confirmed CVEs in two open-source OCPP systems.

## What it is

Gaetano Coppoletta (University of Illinois Chicago), Amanjot Kaur, Nima Valizadeh, and Omer Rana (Cardiff University), and Rigel Gjomemo and V. N. Venkatakrishnan (Discovery Partners Institute, University of Illinois). *2nd Symposium on Vehicle Security and Privacy (VehicleSec 2024)*, co-located with NDSS, San Diego, CA. OCPPStorm is a **black-box fuzzer for implementations of the Open Charge Point Protocol** — the protocol between a charging station and its central management system (CMS, also called a CSMS). Where the attacks on the [OCPP concept page](concepts/ocpp-charging-attacks.md) are mostly design-level (transport profiles, identity handling, duplicate connections), this paper asks the implementation-level question: do real CMS codebases actually validate the OCPP messages they receive? The threat model assumes an attacker who can send messages to a CMS — realistically, via a compromised or rogue charging station — and who can authenticate and start a session, so that post-authentication message handling is in scope. Because implementations differ in language, platform, and deployment, the tool knows nothing about the target's internals: it speaks OCPP over WebSocket, generates messages from the protocol's JSON schemas and a protocol description, and judges the target purely by its responses. In place of code coverage, which a black-box tool cannot see, it uses **protocol coverage**: reaching behaviour deep in the protocol requires inputs that satisfy the protocol's constraints up to that point.

## What it showed

**The tool.** OCPPStorm (~1,900 lines of Python) combines three independent fuzzers. The **Random Fuzzer** generates messages with randomised types, fields, and violations at two levels — datatype/length violations inside fields, and missing or extra fields at message level. The **State Machine Fuzzer** first walks user-defined sequences of valid messages (boot, authorise, start transaction…) to drive the target into a chosen protocol state, and only then starts fuzzing — this is what reaches transaction-handling code that random messages from a cold start never touch. The **Isla Fuzzer** generates grammar- and constraint-based inputs via the ISLA library, either violating chosen constraints deliberately (e.g., an `idTag` longer than its 20-character maximum) or ignoring constraints for coverage. Around the fuzzers sit a Message Validator (JSON-schema compliance, RFC 3339 timestamps) and an Error Detector, which predicts the error the specification prescribes for each malformed message and classifies what actually comes back — correct error, wrong error, a valid request wrongly rejected, a malformed request silently accepted, or a response that itself violates the response schema. Every run produces a battery of logs, including a mismatched-error log for manual vulnerability triage.

**The evaluation.** Two open-source CMS implementations were the targets, chosen as the most developed available: **SteVe** (Java, ~31,400 lines) and **OCPP.Core** (.NET, ~21,700 lines), each seeded with fictitious users and stations. OCPPStorm exercised every OCPP 1.6 message addressed to the CMS, at scale: 500,000 random-fuzzer iterations and 1,114,800 state-machine iterations per target, plus 100,000 unconstrained and 19,950 constrained Isla iterations. Headline behaviour: both implementations deviate from the protocol substantially. Correct-response rates ranged from ~22% to ~58% depending on fuzzer and target, and **wrong-error rates reached 75%** — the servers usually do *something*, but rarely the thing the specification prescribes. The two targets fail differently. SteVe is lenient: it accepts over-length fields, missing required properties, and wrong datatypes across most message types. OCPP.Core enforces the schema more strictly (its silent-acceptance rate is far lower) but, as below, its transaction logic is unsound. Throughput differs just as sharply: the random and state-machine fuzzers sustain ~520–595 messages/second against SteVe but only ~21/second against OCPP.Core, and the Isla fuzzer is one to two orders of magnitude slower than both (1.4–4 messages/second) because constraint solving dominates generation.

**The vulnerabilities.** All confirmed vulnerabilities were triggered by the State Machine fuzzer — the stateful approach was not a refinement but the difference between finding them and not. In **OCPP.Core**: an unvalidated `chargePointVendor` length in BootNotification lets an oversized payload **crash the server** (denial of service); StopTransaction is accepted with `meterStop` below the transaction's `meterStart`, producing **negative charging transactions** and billing errors; transactions can be **terminated with random transaction IDs**, with no ownership or existence validation; multiple concurrent transactions are accepted on the same connector with the same idTag; StartTransaction messages with extraneous or duplicate properties are processed (with the last duplicate silently winning); and message IDs can be reused for different calls on one WebSocket connection, breaking traceability. In **SteVe**: invalid timestamps in StartTransaction propagate into database errors; multiple StopTransaction messages are accepted for a single transaction; resent StartTransaction messages are reprocessed, duplicating transactions; **predictable transaction IDs** allow unauthorised termination of other sessions; the same negative-`meterStop` billing flaw appears; and message-ID reuse is likewise accepted. The paper's abstract counts **five confirmed CVEs with seven further reports under review at MITRE** at submission (the results section phrases the count slightly differently — the paper is internally inconsistent on the numbers, and the abstract's is the figure this page uses); the developers of both systems were contacted and the systems patched.

## Where it fits

This is the **charger↔backend link** — the OCPP side of the KB's charging coverage, disjoint from the vehicle↔charger link that [Losing the Car Keys](losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging.md) and Brokenwire cover. Within that link it is the implementation-robustness complement to the design-level attack model on the [OCPP charging attacks](concepts/ocpp-charging-attacks.md) concept page, which already cites its CVE haul as the reason fuzz-testing belongs in the mitigation list. Its sibling tools in this KB attack the same link from other angles: [CheckOCPP(checkocpp.md) is a passive Wireshark dissector that flags schema violations in observed traffic, and [EmuOCPP(emuocpp.md) emulates endpoints to demonstrate MitM and downgrade attacks — OCPPStorm is the active, stateful testing counterpart aimed at the server. (The mirror-image direction also exists in the literature the paper cites: Gebauer et al.'s "Evil SteVe" is a malicious *server* for penetration-testing charge points; OCPPStorm tests servers from the station side.) A methodological point transfers beyond OCPP: for stateful protocols, stateless random fuzzing plateaued at schema-level findings, and every logic vulnerability — billing, transaction ownership, session termination — required driving the target into a live transaction state first.

## Limits and safety notes

As the paper states them: **Black-box by design.** With no execution feedback, coverage cannot be measured and some code paths will be missed; the authors name white-box integration and static analysis as future work. **Server side only.** Only CMS implementations were tested — charge-point implementations could not be found to test, though the authors note the tool extends to station-bound messages. **Two targets, one protocol version:** the evaluation covers SteVe and OCPP.Core speaking OCPP 1.6; nothing here measures OCPP 2.0.1 implementations, and the leniency findings are properties of these two codebases, not of the protocol. The error-type predictions the Error Detector grades against are derived from the specification documents, so grading inherits any ambiguity in the spec's error taxonomy. This version of the paper omits the CVE numbers themselves (an anonymity footnote promises them for the final version). Testing ran against local installations seeded with fictitious data — no production systems were fuzzed.

## Status and sources

Status: **published** — a finished 2024 conference publication. DOI [10.14722/vehiclesec.2024.23069](https://doi.org/10.14722/vehiclesec.2024.23069), verified against Crossref (record's title, all six authors, VehicleSec 2024 event, and publisher match the paper), 2026-11-01. Full text read end-to-end from the NDSS-site PDF, 2026-11-01. The paper states the OCPPStorm code base will be released as open source.

## Related

- [OCPP and charging attacks](concepts/ocpp-charging-attacks.md) — the concept page for this link; cites this paper's CVE findings under mitigations
- [CheckOCPP(checkocpp.md) — passive schema-violation dissector for the same protocol
- [EmuOCPP(emuocpp.md) — OCPP network emulator with MitM and downgrade demonstrations
- [EVerest(everest.md) — the open-source charging stack whose concurrency flaws are the timing counterpart (Race to Charge)
