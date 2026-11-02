---
uid: 01a19d3c-af8e-722c-bbca-b8415ee283e1
title: "Fingerprinting Electronic Control Units for Vehicle Intrusion Detection"
summary: "Cho and Shin, USENIX Security 2016. Clock-based IDS that fingerprints ECUs from clock skew in periodic messages, the most-replicated CAN IDS baseline."
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/cho"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Cho and Shin, USENIX Security 2016. Clock-based IDS that fingerprints ECUs from clock skew in periodic messages, the most-replicated CAN IDS baseline."
sources:
  - url: "https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_cho.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - error-handling-of-in-vehicle-networks-makes-them-vulnerable
  - vatican-vetted-authenticated-can-bus
  - viden-attacker-identification-on-in-vehicle-networks
  - gids-gan-based-intrusion-detection-system-for-in-vehicle-network
  - exposing-new-vulnerabilities-of-error-handling-mechanism-in-can
  - evading-voltage-based-intrusion-detection-on-automotive-can
  - in-vehicle-intrusion-detection
---

Cho and Shin, USENIX Security 2016. Clock-based IDS that fingerprints ECUs from clock skew in periodic messages, the most-replicated CAN IDS baseline.

## What it is

Kyong-Tak Cho and Kang G. Shin, Real-Time Computing Laboratory, University of Michigan. *25th USENIX Security Symposium* (USENIX Security '16), Austin, TX, August 10–12, 2016, pp. 911–927. The paper proposes CIDS (Clock-based IDS), an anomaly-based intrusion detection system for CAN that fingerprints each transmitting ECU by its clock skew and — unlike prior CAN IDSs — can identify *which* ECU mounted an attack. It is the companion piece to the same authors' bus-off paper (same batch): CIDS is the defensive half of their 2016 programme.

## What it showed

**The fingerprinting primitive.** CAN messages carry no transmitter identity, which is why content/periodicity IDSs cannot attribute attacks. Prior clock-skew fingerprinting needed timestamps embedded in packets, which CAN does not have. CIDS instead exploits the *periodicity* of in-vehicle messages: a monitoring ECU timestamps arrivals, computes the average clock offset per batch of N = 20 messages of a given ID, and accumulates the offsets over time. Because an ECU's clock skew is constant, the accumulated offset grows linearly and its slope is the skew — a physical fingerprint of the transmitter that an attacker cannot fake with forged timestamps, since there are none.

**The detector.** Per message ID, CIDS fits the linear model (accumulated offset = skew × elapsed time + identification error) with Recursive Least Squares (forgetting factor λ = 0.9995), and runs a two-sided CUSUM change detector (reference value κ = 5, control limit Γ_L = 5) over the identification errors. Fabrication (injected messages arrive off-schedule), suspension (a silenced ECU's messages stop), and masquerade (a different ECU transmits under the victim's ID, so the skew itself changes) each shift the error mean away from zero and trip the detector. A verification step discounts alarms plausibly caused by bus contention.

**Message-pairwise detection.** For two periodic messages from the same ECU, their instantaneous average clock offsets are strongly correlated (≈1); for different ECUs, ≈0. A second RLS+CUSUM stage on offset correlations covers the worst case the per-message stage cannot see — an attacker whose skew nearly equals the victim's. In the paper's Camry data, one ECU pair's skews differed by only ~3% (345.3 ppm vs 334.1 ppm), yet their offset correlations separated them cleanly (0.9860 same-ECU pair vs 0.0331 cross-ECU); in a simulated worst-case masquerade on the Honda data, the correlation of the victim's message pair collapsed from 0.9533 to 0.1201 at takeover, which the pairwise stage caught while the per-message stage (skew unchanged) could not.

**Results.** On a 3-node CAN prototype (Arduino UNO + MCP2515/MCP2551, 500 kbit/s), two message IDs sent by one node yielded the same skew (13.4 ppm) and a third node's message a distinct one (27.2 ppm). On a real 2013 Honda Accord (logged via OBD-II), message pairs verified to share an ECU shared a skew ({0x1B0, 0x1D0}: 78.4 ppm; {0x294, 0x295}: 199.8 ppm) and singletons differed (265.7 ppm, 95.78 ppm); logged traffic from a 2010 Toyota Camry and a 2010 Dodge Ram Pickup fingerprinted correctly the same way. Evaluated against fabrication, suspension, and masquerade attacks on the prototype and the Accord, using four datasets of 300 intrusions each built from 30 minutes of recorded traffic (≈2.25 million messages), the hardest case — the timed masquerade attack under per-message detection alone — was detected with **100% true positives at a false-positive rate of 0.055%** (the paper's headline figure); at false-positive rates below 0.055%, 97% of anomalies were still detected. Adding message-pairwise detection **eliminated all false positives** in the evaluation while still detecting all attack types. On detection, the changed fingerprint identifies the compromised ECU — the root-cause capability prior IDSs lacked.

## Where it fits

The founding clock-skew CAN IDS and the baseline later CAN IDS work compares against (the list summary's "most-replicated CAN IDS baseline" framing). Within this batch it is the detection-side answer to the problem the other two papers frame from opposite ends: the [bus-off paper](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) shows an attack that protocol-level error handling enables and that content/periodicity IDSs misread as system errors — CIDS's transmitter fingerprinting is precisely the missing signal such attacks try to hide behind — while [vatiCAN](vatican-vetted-authenticated-can-bus.md) takes the other defensive route, authenticating messages so impersonation fails cryptographically instead of statistically. CIDS's stated niche: an IDS needs no key management, no protocol change, and no extra bus traffic, at the price of detecting rather than preventing.

## Limits and safety notes

As the paper states them: **periodic messages only** — clock skews can only be extracted from periodic messages; if an attacker injects *aperiodically*, CIDS can still detect the intrusion but cannot pinpoint which ECU sent the attack messages. **Near-identical skews exist:** by the birthday paradox, some ECU pairs have near-equivalent skews (≈3% apart in the Camry data); per-message detection alone can miss a masquerade between them, which is why the pairwise stage exists — and if two ECUs' clock behaviours are *still* indistinguishable, the paper suggests excluding them from examination, trading coverage for fewer false positives. **False positives are not zero for the base detector:** 0.055% (per-message only, worst-case attack). **Defeating CIDS is discussed honestly:** an attacker who learns the victim's skew could in principle heat or cool the compromised ECU to match it, but must then also match the victim's instantaneous clock *offsets* to defeat pairwise detection; and an attacker who compromises the ECU running CIDS itself is countered only if CIDS is distributed across several ECUs. Evaluation scope: one live vehicle (2013 Honda Accord) plus logged data from two more; applicability to synchronized/time-triggered protocols (TTCAN, FlexRay) is conditional.

## Status and sources

Status: **published** — a finished 2016 publication; no living artefact (CIDS was a research prototype). **DOI: none** — USENIX does not assign DOIs to its proceedings papers; no aggregator identifier is substituted. Full text openly available from USENIX; read in full 2026-11-01.

## Related

- [Error Handling of In-Vehicle Networks Makes Them Vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md)
- [vatiCAN: Vetted, Authenticated CAN Bus](vatican-vetted-authenticated-can-bus.md)
- [Viden: Attacker Identification on In-Vehicle Networks](viden-attacker-identification-on-in-vehicle-networks.md) — the same authors' voltage-fingerprint follow-on; identification that survives aperiodic injection
- [GIDS: GAN based Intrusion Detection System for In-Vehicle Network](gids-gan-based-intrusion-detection-system-for-in-vehicle-network.md)
