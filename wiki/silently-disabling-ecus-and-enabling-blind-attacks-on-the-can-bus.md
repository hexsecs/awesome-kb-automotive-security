---
uid: 01a19d3c-afd6-76c5-8a71-45bd9bd6a8ab
title: "Silently Disabling ECUs and Enabling Blind Attacks on the CAN Bus"
summary: "Rogers and Rasmussen, arXiv 2022. Disables an ECU with a single frame and without generating bus errors, evading the error-counting that earlier bus-off…"
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/2201.06362"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Rogers and Rasmussen, arXiv 2022. Disables an ECU with a single frame and without generating bus errors, evading the error-counting that earlier bus-off detection relies on, and adds a synchronisation method letting an attacker who cannot read the bus strike reliably."
sources:
  - url: "https://arxiv.org/abs/2201.06362"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - error-handling-of-in-vehicle-networks-makes-them-vulnerable
  - exposing-new-vulnerabilities-of-error-handling-mechanism-in-can
  - canvas-fast-and-inexpensive-automotive-network-mapping
  - canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks
  - can-availability
---

Rogers and Rasmussen, arXiv 2022. Disables an ECU with a single frame and without generating bus errors, evading the error-counting that earlier bus-off detection relies on, and adds a synchronisation method letting an attacker who cannot read the bus strike reliably.

## What it is

Matthew Rogers and Kasper Rasmussen, University of Oxford. arXiv:2201.06362, January 2022 — a preprint; no peer-reviewed venue version exists. Where the earlier bus-off literature assumes an attacker who transmits frames (a compromised ECU or an attached device), this paper studies a weaker and stranger capability: an attacker who can only **flip individual bits on the bus**. Flipping a recessive 1 to a dominant 0 is free — dominant always wins on a wired-AND bus. Flipping a 0 to a 1 is physically hard (the attacker must negate another node's dominant signal; electromagnetic-induction attacks are the motivating example) and is modelled as succeeding only with some probability p. The system model is a single CAN bus of fully protocol-compliant ECUs watched by a basic whitelist IDS that alerts on previously unseen arbitration IDs. Three questions structure the paper: can a bit-flipper force a victim into bus-off **without anything anomalous ever appearing on the bus**; can an attacker who **cannot read the bus at all** still deliver an attack reliably; and what change to the error process would make silent disabling impossible in principle.

## What it showed

**The stealthy bus-off attack.** The lever is a rule every CAN node lives by: an error frame that is itself interrupted constitutes a further error. In Cho & Shin's attack each +8 of victim TEC costs one whole message, and every error frame completes on the bus, plainly visible — 32 messages of evidence. Here the attacker flips a bit in the victim's message to start an error, then **keeps interrupting the victim's error frames** — each interruption is another error, another +8 — so the victim's TEC climbs past 255 and it enters bus-off *inside a single message* (≈600 µs), **before any error frame has ever completed**. Nothing anomalous reaches the bus: no completed error frame, no extra message, no timing shift. Two obligations remain. The hijacked message must not raise errors in *receivers* (their error frames would be visible to the IDS), so the attacker recomputes its CRC after flipping and ensures the frame still ends with the required recessive run (the paper counts 11 recessive bits). And the victim's receiver stays online in bus-off — only its transmitter is disabled — so the attacker can immediately transmit in the victim's name into a vehicle that otherwise behaves normally.

**How bad a flipper can be — the probabilistic analysis.** Success decomposes into three requirements: interrupt every error frame (at least one successful 0→1 flip in each 6-bit window); finish the frame (11 consecutive recessive bits at the end — the binding constraint: an attacker below ~94% flip accuracy does this worse than a coin flip *unless* the victim is already error passive or in bus-off, in which case its own recessive signalling does the work, which is why the attack first pushes the victim passive); and present an arbitration ID the whitelist already knows. Combined, an attacker who flips bits with only **38% accuracy silently bus-offs a single victim within one message with over 99% success probability** (the abstract rounds this to 40% accuracy succeeding 100% of the time).

**Blind synchronization.** Every prior CAN attack quietly assumes the attacker can read the bus and time its move. A write-only "blind" attacker — a fixed payload fired by a limited exploit, or an induction attacker who cannot observe a flip's effect — succeeds only when its transmission lands in dead bus time: the paper's worked example gives 30% at 70% bus utilization (collisions otherwise leave at best an accidental DoS). The proposed methodology forces the bus into a known state from **any** of its four possible states (mid-message; arbitration over a 0; arbitration over a 1; dead bus) with a fixed recipe: flip a bit to provoke an error; where the attacker has won arbitration or the bus was idle, stay silent for 6 bits so a stuff error forms instead; flip a second bit at bit 8 to align the cases. After the resulting error frame and delimiter, the attacker knows exactly where the next frame boundary is — success rises to **100%** regardless of bus state. The method is not itself stealthy: it deliberately lets one error frame (possibly two) complete; it is a synchronization primitive for other attacks, not a silent one.

**The proposed fix — Error Resistant Error Frames (EREFs).** Change one rule: an interrupted error frame increments nothing; a node's TEC rises by 8 only when an error frame **completes**, and only once per error. The stealthy attack's engine — +8 per interruption — is removed. An attacker must now either let error frames complete (visible, and attributable) or interrupt forever and cascade errors into every receiving ECU, stopping the bus rather than silently owning one node. Even a 99%-accurate flipper then ends a clean frame only ~80% of the time (0.99¹¹), and the arbitration stage becomes infeasible in principle: flipping bits during arbitration inevitably errors into third-party ECUs, which cannot clear the error without producing the indicator the attacker exists to avoid. Two supporting mechanisms assume a defender-side controller that, unlike production parts, does not drop errored messages: the IDS keeps its **own per-ECU error counters** and narrows the transmitter from the arbitration prefix alone (demonstrated on a dataset of over 10 million packets from 17 ECUs), which catches even the slow, spread-out version of the original bus-off attack; and **canary transmissions** — the IDS periodically (every 1–5 s) sends an unused ID whose first three bits are dominant, so an attacker who is continuously "driving the bus" by flipping dominant bits to recessive will inevitably flip one, error the IDS's own frame, and expose itself.

## Where it fits

The third point on this KB's bus-off line, and the one that changes the detection question. [Cho & Shin](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) produce one completed, visible error frame per step and propose detection keyed to bursty error frames. [Serag et al.](exposing-new-vulnerabilities-of-error-handling-mechanism-in-can.md) regenerate errors *inside the victim's controller* — the victim's own passive signalling, interrupted by ordinary bus traffic, does the counting — fast, but the opening still collides sixteen times in the open. Rogers and Rasmussen move the interruption *outside* the victim: an external bit-flipper interrupts the error frames themselves, so the observable the other two attacks leave behind — a completed error frame — never occurs. The arithmetic is shared (+8 per interrupted error) and worth keeping distinct for the CAN availability/DoS concept (issue #43): Serag's is a victim-side regeneration primitive measured on real controllers; this paper's is a weaponization analysis against an assumed external capability. [CANvas](canvas-fast-and-inexpensive-automotive-network-mapping.md) is the concrete relative: its below-controller tap drives dominant bits into a victim's frame at chosen positions — bit-level bus access of the kind this paper abstracts into a flip probability — although CANvas injects dominant bits only, and this attack also needs the hard, recessive direction. Honesty about kind: unlike its two predecessors, this paper is **analysis, not demonstration** — probability computations over an explicit attacker model plus dataset-based detection checks; no hardware attack is built.

## Limits and safety notes

As the paper states them: **The bit-flip capability is assumed, not demonstrated.** No device is built; 0→1 flips at any accuracy rest on cited prior work (electromagnetic induction), and the model prices the hard direction as a bare probability. **The stealth claim is scoped to bus-visible indicators** — no completed error frames, no new IDs, no timing change; physical-layer detection (voltage fingerprinting) is argued around via its retraining windows, not measured. **EREFs are a protocol change, not a patch:** they require controllers to behave differently from the current standard, so nothing here deploys on existing vehicles; the per-ECU error counting likewise requires a non-standard controller that retains errored messages. **Model assumptions:** a single bus, all ECUs protocol-compliant, no man-in-the-middle position, and the attacker's access is never the victim ECU itself. **The blind method trades stealth for certainty:** it guarantees delivery at the price of one or two completed error frames — a visible trace the stealthy attack exists to avoid.

## Status and sources

Status: **published** — an arXiv preprint (arXiv:2201.06362, submitted 17 January 2022); no living artefact. **DOI: none** — no Crossref record matches this title (bibliographic query, 2026-11-01); no venue version was found, and no identifier from the authors' other papers is substituted. Full text read in full from the arXiv PDF, 2026-11-01.

## Related

- [Error Handling of In-Vehicle Networks Makes Them Vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) — the original bus-off attack this paper makes invisible
- [Exposing New Vulnerabilities of Error Handling Mechanism in CAN](exposing-new-vulnerabilities-of-error-handling-mechanism-in-can.md) — Serag et al.; the victim-side counterpart to the same +8 arithmetic
- [CANvas: Fast and Inexpensive Automotive Network Mapping](canvas-fast-and-inexpensive-automotive-network-mapping.md) — a concrete route to the bit-level bus access assumed here
- [CANflict](canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks.md) — bit-level access from inside an unmodified MCU
