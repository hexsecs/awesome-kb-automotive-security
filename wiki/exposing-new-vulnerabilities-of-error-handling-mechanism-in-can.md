---
uid: 01a19d3c-af8a-76c5-a965-4f8b37d1da1d
title: "Exposing New Vulnerabilities of Error Handling Mechanism in CAN"
summary: "Serag et al., USENIX Security 2021. Systematically tests CAN node behaviour under error conditions with CANOX and finds three further vulnerabilities in the…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity21/presentation/serag"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Serag et al., USENIX Security 2021. Systematically tests CAN node behaviour under error conditions with CANOX and finds three further vulnerabilities in the standard beyond the bus-off attack."
sources:
  - url: "https://www.usenix.org/system/files/sec21-serag.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - error-handling-of-in-vehicle-networks-makes-them-vulnerable
  - canvas-fast-and-inexpensive-automotive-network-mapping
  - canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks
  - silently-disabling-ecus-and-enabling-blind-attacks-on-the-can-bus
  - fingerprinting-electronic-control-units-for-vehicle-intrusion-detection
  - can-availability
---

Serag et al., USENIX Security 2021. Systematically tests CAN node behaviour under error conditions with CANOX and finds three further vulnerabilities in the standard beyond the bus-off attack.

## What it is

Khaled Serag and Rohit Bhatia (Purdue University), Vireshwar Kumar (Indian Institute of Technology Delhi), and Z. Berkay Celik and Dongyan Xu (Purdue). *30th USENIX Security Symposium*, August 11–13, 2021, pp. 4241–4258. The bus-off attack (Cho & Shin, 2016) weaponized CAN error handling from the default **error active** state. This paper asks what the rest of the state machine hides: nodes were not expected to leave error active except under genuine faults, so **error passive** — and the transitions back — went largely unexamined. The tool is **CANOX** (CAN Operation eXplorer), an automated tester that places a fully programmable node under test in a chosen error state, varies bus load, traffic priority, and scenario, and flags deviations in standby delay (SD) and TEC value change (TECC). TEC is the observable because a passive error frame is fourteen recessive bits — electrically indistinguishable from an idle bus, hence invisible to other nodes and to bus monitors. The threat model is a remotely compromised ECU running arbitrary code, with **no prior knowledge of the vehicle's internals** beyond its make and model, and restricted to what a standard CAN controller can do — no bit-level bus control.

## What it showed

**Vulnerability 1 — passive error regeneration.** A passive error frame needs 14 recessive bit-periods to complete, but only 11 recessive bit-periods separate a frame's acknowledgment bit from the next start-of-frame (8 delimiter/EOF bits plus the 3-bit intermission) — the further idle time the standard assumes is neither provided by a busy bus nor enforceable. So when a passive node tries to signal an error, another node begins transmitting first; its dominant start bit lands inside the passive frame's delimiter, the passive node reads a **form error**, adds **+8 to its TEC**, and signals again — into the same interruption. The cycle is self-sustaining: one initial collision can walk a passive node to TEC 256 and bus-off with no further attacker action, silently, because every signal it emits is recessive. CANOX measured the asymmetry: an error active node's TECC per collided message is a fixed +7 net regardless of load, while a passive node's grows with bus load — at 100% load, a single collision carried it from error passive to bus-off.

**Exploit — Single Frame Bus Off (SFBO).** (1) The attacker forges a message with the victim's ID but higher-priority content and collides it with the victim's message (preceded-ID synchronization, inherited from Cho & Shin). (2) Automatic retransmissions collide 16 times; both nodes reach TEC 128, error passive — the original attack's phase 1. (3) The victim's passive error frame no longer interrupts the attacker, whose message now succeeds; the attacker returns to error active. (4) The attacker sends 15 back-to-back **clutter messages** (arbitrary ID); each starts while the victim is re-signalling, regenerating its error: the victim's TEC follows 135 + 8·N_clutter and crosses into bus-off at 15. The whole attack targets **one victim message in one round** — TEC 0→256 in ≈5 ms on the testbed, against the original attack's minimum 19 rounds and ≈190–210 ms (≈36× slower). Stopping the clutter early is a second exploit: the victim's TEC can be **set to any chosen value** in the 135–255 range.

**Vulnerability 2 — deterministic recovery.** The standard does not say what happens to a message left buffered when a node goes bus-off. CANOX found it is transmitted **at the exact moment of recovery** (recovery takes a learnable interval — bare minimum, fixed, sequenced, or random, depending on the ECU). An attacker therefore knows the recovery message's ID, content, and timing in advance: the **Persistent Bus Off** exploit re-runs SFBO against every recovery attempt, converting an ephemeral DoS into a standing one.

**Vulnerability 3 — error state outspokenness.** A passive node must additionally wait out an 8-bit suspend transmission period before retransmitting or sending successive messages, which measurably lowers its effective priority (≈240 µs of extra standby delay observed). That leak identifies senders: push one message's sender into error passive, collide with a second message, and read the *attacker's own* TEC change — +7 means the second message's sender is the same, now-passive ECU; +16 means a different, error active ECU. This groups IDs by transmitting ECU with no special equipment, and — unlike clock-skew or voltage fingerprinting — also works for **aperiodic** messages whose ID and arrival are deterministic (e.g. diagnostic request/response pairs); with OBD-II probing it identifies each ECU's function.

**The combined attack — Scan-Then-Strike (STS).** Four stages: map the network (which IDs each ECU sends), identify a safety-critical ECU among them, learn its recovery behaviour, then strike and keep it down. Evaluated on a five-node Arduino testbed at 500 kbit/s and on a real vehicle — a 2011 car whose make and model the authors anonymize ("ExpCar1"), attacked through an Arduino node wired to CANH/CANL at the OBD-II port. Mapping was exact on both: 4 ECUs and 20 IDs in ≈3 minutes on the testbed; **4 ECUs (EBCM, BCM, TCM, ECM) and 50 periodic IDs in ≈9 minutes on the vehicle, at 100% accuracy**. Suppression rate — the fraction of time the victim stays in bus-off under continuous recovery prevention — averaged **97.5% (EBCM), 91.4% (BCM), 85% (TCM), 83% (ECM)** on the vehicle over 15 minutes, with the brake module held at 100% for ≈2.4 s stretches; on the testbed it exceeded 99.99% over 30 minutes, where the same attack built on the original bus-off primitive managed only 1.3–15.5%. That gap is explained by ECU diversity: the original attack gains only +7 TEC per round while the victim's *other* messages each repay 1, so against an ECU sending many IDs (diversity ratio ≥8) its rounds grow exponentially and it becomes infeasible; SFBO is indifferent to diversity.

## Where it fits

This paper is the second half of the [bus-off](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) story. Cho & Shin attack from error active and must win a fresh collision against every periodic retransmission; Serag et al. show that once their phase 1 has made the victim error passive, the standard's own signalling rules become the weapon — the attacker stops colliding and merely talks over a signal the victim cannot make heard. The [CANvas](canvas-fast-and-inexpensive-automotive-network-mapping.md) comparison cuts the other way: CANvas maps senders passively from clock offsets and needs an external below-controller tap to isolate receivers, while STS's mapping is active, runs through an unmodified controller, covers aperiodic messages, and doubles as the attack's reconnaissance stage. CANvas also documented that message-level bus-off is fragile under real jitter; SFBO keeps the same deliberate-collision precondition for its opening — what changes is the endgame, which no longer depends on repeated precise collisions. For the CAN availability/DoS concept (issue #43), this cluster contributes two distinct primitives: SFBO/persistent bus-off (availability) and arbitrary TEC setting (error-state manipulation). The vulnerabilities were disclosed to Bosch PSIRT, routed by ISO to the SAE committee, and filed with CISA.

## Limits and safety notes

As the paper states them: **A compromised ECU is assumed** — STS is a post-compromise attack, not an entry point. **The collisions are not stealthy:** the paper's own limitation section notes that a collision-counting IDS could suspect an attack; its mitigations are procedural (stages 1–3 can run low-and-slow) and structural (a detected attack still cannot be stopped without changing the standard). **Platform scope:** CANOX's measurements and the testbed attack use one controller family (MCP2515) on Arduino-class nodes; the vulnerabilities are argued from the standard's text and confirmed on one anonymized test vehicle, not surveyed across controller implementations. **Random-recovery ECUs resist prediction:** the two vehicle ECUs with random recovery intervals show the lowest suppression rates (83–85%), held down only by attacking their trailing recovery messages. **Defences are recommendations only:** revise the standard; reset the victim's controller; clear transmit buffers at bus-off; randomize the suspend interval. None is in production silicon.

## Status and sources

Status: **published** — a finished 2021 publication; the testbed and attack were research prototypes. **DOI: none** — USENIX does not assign DOIs to its proceedings papers; no aggregator identifier is substituted (verified by Crossref query, 2026-11-01; the same group's separate AutoSec 2022 demo paper has a DOI and is a different work). Full text open at USENIX; read in full 2026-11-01.

## Related

- [Error Handling of In-Vehicle Networks Makes Them Vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) — the original bus-off attack whose phase 1 SFBO inherits
- [CANvas: Fast and Inexpensive Automotive Network Mapping](canvas-fast-and-inexpensive-automotive-network-mapping.md) — the passive, clock-based mapping this active method contrasts with
- [CANflict](canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks.md) — a software route to the bit-level timing this attack family needs
- [Silently Disabling ECUs and Enabling Blind Attacks on the CAN Bus](silently-disabling-ecus-and-enabling-blind-attacks-on-the-can-bus.md) — the sibling stealth bus-off, one year later
- [Fingerprinting Electronic Control Units for Vehicle Intrusion Detection](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md) — CIDS; sender identification from the defence side
