---
title: "SoK: Kicking CAN Down the Road. Systematizing CAN Security Knowledge"
summary: "Serag et al., 2025. Systematization of two decades of CAN security, with a unified taxonomy and assessment model for attackers, attacks, and defences."
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/2510.02960"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Serag et al., 2025. Systematization of two decades of CAN security, with a unified taxonomy and assessment model for attackers, attacks, and defences."
sources:
  - url: "https://arxiv.org/abs/2510.02960"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - error-handling-of-in-vehicle-networks-makes-them-vulnerable
  - canvas-fast-and-inexpensive-automotive-network-mapping
  - fingerprinting-electronic-control-units-for-vehicle-intrusion-detection
  - evading-voltage-based-intrusion-detection-on-automotive-can
  - can-injection
  - can-availability
---

Serag et al., 2025. Systematization of two decades of CAN security, with a unified taxonomy and assessment model for attackers, attacks, and defences.

## What it is

A defender-oriented systematization of knowledge (SoK) for CAN 2.0 security — not a new attack or defence, but a framework for comparing the existing ones. The corpus was built by a keyword search of eight major security venues (1983 to 1 June 2025) followed by unrestricted citation-graph traversal, retaining only papers introducing a *distinct* attack or defence idea (same bin, purpose, and assessment = a variant; the earliest is kept): 150 papers — 43 attack-only, 100 defence-only, 7 both, 17 defence papers also counted as dual-use — 67 contributing attacks, 107 defences. Its framework: a three-layer CAN stack model (transwire ≈ physical, controller ≈ data-link, "higher layer" for UDS/J1939-class protocols running on CAN); a multi-dimensional attacker model; attack and defence taxonomies with assessment models, juxtaposed to expose gaps; and a root-cause analysis (is each cause *inherent* to CAN? *unique* to CAN?) feeding a transferability check against CAN FD, CAN XL, and 10BASE-T1S. The authors are the CANOX error-handling group and collaborators (Serag et al.), writing explicitly from the defender's seat.

## What it showed

**Three archetypes are enough.** Attackers are modelled on bus access, equipment, and deepest stack layer controlled; because control is cumulative, twelve nominal combinations collapse into three archetypes: the **by-the-rules** attacker (higher-layer control only; frame sniffing, full-frame injection on an idle bus, and simultaneous transmission against a victim's frame); the **bit-banger** (controller-layer control: bit/pulse injection and sniffing, dynamic bit-width manipulation — traditionally physical, but shown remotely attainable on generic ECUs, the KB's CANflict page being one route); and the **down-to-earth** attacker (full transwire control, physical access and special equipment).

**The attack map.** Attacks are binned by CIA property × stack layer into 22 categories — confidentiality C1–C5, integrity I1–I10 (fake-data fabrication through physical-fingerprint distortion), availability A1–A7 — each scored on restrictiveness, difficulty, and weakest attacker model. An attack is **highly replicable** if it exploits a standard vulnerability, is easy-to-moderate, and is remotely launchable. The asymmetries are the finding: integrity is most targeted (28 of 50 pure attack papers), most diverse (10 categories), and most replicable (6 of 10 highly replicable); the controller layer dominates (32 of 50 papers, 11 categories, 9 of 11 highly replicable, none resting on restricted flaws); availability is second in targeting (22 of 50, 4 of 7 highly replicable); higher-layer attacks are numerous (29 of 50) but least replicable (2 of 7) and most dependent on restricted implementation flaws; confidentiality is least targeted in pure attack papers (17 of 50) but most targeted once dual-use defence papers count (33 of 67) — fingerprinting research that doubles as reconnaissance.

**The defence map, and the gaps.** Defences are taxonomised on the same grid into 19 categories (DC1–DC3, DI1–DI11, DA1–DA5) and assessed per attack on six axes. A defence is *effective* only if it prevents, covers widely, is at least analysed for CAN, and is moderate-or-better on all three cost axes; a **defence gap** is a highly replicable attack with no effective defence. Integrity is the only element with effective defences for highly replicable attacks (7 of 10 categories defended, including 4 of 6 highly replicable) — and the most defended (88 of 107 defence papers). Availability is the exposed element: second-most targeted, least defended (5 of 107 papers), *all* its highly replicable bit-banger attacks without effective defence, and all four controller-layer availability attacks highly replicable with no effective defence. Confidentiality has no effective defence for any highly replicable attack. Two cheap defences recur as disproportionately valuable: one-shot mode (DA4, disabling automatic retransmission) against the retransmission-dependent error-state attacks, and frame destruction (DI5), which is what keeps impersonation from being a gap at all.

**Root causes: CAN is more securable than perceived.** Nine attack root causes (R1 attacker access; R2 shared-media properties; R3 the exploitable priority system; R4 error-handling properties; R5 physical signalling; R6 bit sampling; R7 vulnerable higher-layer protocols/implementations; R8 layer-II rule violation; R9 layer-I rule bypass) and three gap root causes (DR1 cryptography challenges — performance, 64-bit length, and above all the shared-media key-management dilemma: group keys expose traffic to any compromised member, pairwise keys do not fit a broadcast bus; DR2 the cost of filtering or disabling one attacker's signals; DR3 the difficulty of understanding the cyber-physical environment well enough to call a message malicious). Only **two causes are unique to the CAN family — R4 (error handling) and R6 (bit sampling)** — and **no defence-gap root cause is unique to CAN**. Of 22 attacks, 9 are inherent, 8 unique, only 5 both; no gap is both inherent and unique.

**Transferability: replacing CAN does not fix it.** Judged by root-cause presence in the successor standards (by-the-rules attackers only): CAN FD shares every compared root cause — all considered attacks and gaps likely transfer. CAN XL, error handling on: 14 attacks and 2 gaps likely transfer, 1 more attack exposed as a gap; off: error-state manipulation likely dies but node suspension (DA2) dies with it, likely exposing bus-access denial as a gap. 10BASE-T1S: 10 attacks likely transfer, both gaps transfer, 3 further attacks likely exposed as gaps. Even a hypothetical *ideal* bus leaves 6 of 14 compared attacks standing, because attacker access (R1), higher-layer flaws (R7), and environment understanding (DR3) live in the system around the bus. Optional link-layer security (CANsec, MACsec) closes none of the open gaps. Four research directions follow: insider-aware IVB cryptography, low-cost shared-media filtering, cyber-physical state consistency checking, and securing emerging IVBs before deployment hardens their own flaws.

## Where it fits

This is the KB's first systematization *of the CAN literature itself*, and it largely confirms the framings the KB's CAN cluster already uses — with two sharpenings. The error-handling line (bus-off page, CANOX page, CANvas) is exactly the SoK's R4, graded **inherent and unique**: the sender/receiver validity mismatch, the distinct error states, and the uncovered non-conformity cases are CAN-family properties, not generic bus properties. CANvas's clock-skew correction sits inside the SoK's C3 (network reconnaissance), which treats clock-skew and voltage profiling symmetrically as attack *and* defence (also C4; defence-side DI7), and the SoK carries the DUET warning in its own terms: profiles updated online can be poisoned (I10) — fingerprinting defence and evasion attack are one literature, not two. Where the SoK pushes past the KB's framing is availability: the filed CAN-availability concept issue treats bus-off and error manipulation as an under-defended class, and the SoK generalises that verdict — availability is the *most exposed* element bus-wide, and its gap root cause (DR2) is not CAN-specific. For the CAN message-authentication concept ([issue #45](https://github.com/hexsecs/awesome-kb-automotive-security/issues/45)), DI4 is the design space stated abstractly — authentication channel (payload, spare fields, out-of-band), immediacy (immediate vs delayed/TESLA-style), responsibility (per-ECU vs central monitor): the axes on which vatiCAN and LeiA make opposite choices — and DR1 names the concept's two limits in stronger form: a compromised legitimate sender is not an edge case but *the* key-management dilemma of a broadcast bus, and authentication says nothing about availability.

## Limits and safety notes

A systematization is an assessment of other people's evidence, not new evidence: every grade is the authors' judgement on published claims. Three scope choices shape the conclusions: variants collapse to their earliest publication, so later, stronger versions do not raise an attack's grade; the corpus closes 1 June 2025; and transferability is, in the authors' own word, *indicative* — inferred from root-cause presence in the successor standards, not validated on those buses. Nothing here reproduces an attack procedure; the taxonomy's value is defensive triage.

## Status and sources

Status: **published**. Version read: arXiv:2510.02960v5 (25 Sep 2026), the NDSS 2027 proceedings version (Symposium 22–26 March 2027, Seoul; ISBN 978-1-970672-09-1) — the stub's "2025" is the arXiv first version's date. The paper prints DOI 10.14722/ndss.2027.230993 in its footer; **no Crossref record for that DOI existed when checked for this page** (the symposium is in the future), so the DOI is reported as printed-in-paper, not Crossref-verified — the deliberate opposite of this KB's usual rule, stated rather than silent. (Artefact spreadsheet: DOI 10.5281/zenodo.22555092.)

## Related

- [Error Handling of In-Vehicle Networks Makes Them Vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) — the CANOX line: the SoK's R4 at full depth
- [CANvas](canvas-fast-and-inexpensive-automotive-network-mapping.md) — clock-skew mapping, inside the SoK's C3
- [Fingerprinting Electronic Control Units for Vehicle Intrusion Detection](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md) — CIDS; fingerprinting as attack and defence
- [DUET](evading-voltage-based-intrusion-detection-on-automotive-can.md) — the profile-poisoning instance of the SoK's I10
- [CAN injection](concepts/can-injection.md) — the access-path pattern the archetypes organise
