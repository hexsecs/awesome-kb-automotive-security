---
uid: 01a19d3c-af3b-789f-9db9-7a4f437a0c7d
title: "Brokenwire: Wireless Disruption of CCS Electric Vehicle Charging"
summary: "Kohler, Baker, Strohmeier, and Martinovic, NDSS 2023. Aborts CCS rapid-charging sessions wirelessly from tens of metres with off-the-shelf radio hardware…"
type: entity
category: "Research Papers"
url: "https://www.ndss-symposium.org/ndss-paper/brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Kohler, Baker, Strohmeier, and Martinovic, NDSS 2023. Aborts CCS rapid-charging sessions wirelessly from tens of metres with off-the-shelf radio hardware, against individual vehicles or whole fleets."
sources:
  - url: "https://www.ndss-symposium.org/ndss-paper/brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging/"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.14722/ndss.2023.23251"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging
  - charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment
  - pyplc
  - ocpp-charging-attacks
---

Kohler, Baker, Strohmeier, and Martinovic, NDSS 2023. Aborts CCS rapid-charging sessions wirelessly from tens of metres with off-the-shelf radio hardware, against individual vehicles or whole fleets.

## What it is

Sebastian Köhler and Richard Baker (equal contribution) and Ivan Martinovic, University of Oxford, with Martin Strohmeier (Armasuisse Science + Technology). *Network and Distributed System Security (NDSS) Symposium 2023*, San Diego, CA. Brokenwire is a wireless **availability** attack on the Combined Charging System (CCS): it aborts DC rapid-charging sessions from a distance, with no contact with vehicle, cable, or charger, and leaves both ends in an error state from which charging does not automatically resume. The attack sits at the same physical layer as this group's earlier [Losing the Car Keys](losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging.md) — the HomePlug Green PHY (HPGP) power-line communication CCS runs over the cable's Control Pilot and Protective Earth lines — but runs it in the opposite direction: where the 2019 paper *received* the cable's unintentional emissions, Brokenwire *transmits into* them. The susceptibility follows from the wiring: the communication pair is single-ended and the cable unshielded, so an over-the-air signal couples onto the wires. And the behaviour exploited is mandatory: HPGP's medium access is CSMA/CA, the carrier-sense collision-avoidance scheme familiar from Wi-Fi — a node that detects another transmission defers, retries after a random backoff, and defers again, indefinitely.

## What it showed

**The mechanism.** Every HPGP frame begins with a standard preamble, defined in the public specification, which receivers are built to detect efficiently: per the standard, a preamble must be recognised at a signal-to-noise ratio of just **≥2 dB**. Brokenwire transmits nothing but repeated preambles, generated from the public spec — or, simpler, a captured snippet of genuine charging traffic with its preamble replayed — the authors' own evaluation method, chosen to show no signal-processing knowledge is needed. Every listening modem perpetually senses a busy channel and never transmits. The higher layers then do the damage: ISO 15118 sessions run on short message timeouts (an average of 1.5 s, per the paper), so roughly **two seconds** of attack ends the session. When the transmission stops, the link recovers — but the session does not: vehicle and charger sit in an error state, and in no test did a vehicle fall back to basic PWM charging or resume on its own; restarting means unplugging, replugging, and re-authenticating by hand. Broadcasting *before* a session starts prevents it from starting at all.

**Laboratory results.** The testbed used two Devolo HPGP evaluation boards carrying the same Qualcomm QCA7000 chips used in vehicles and chargers, joined by 4 m of CP/PE-replica cable; the attacker was a LimeSDR with a 1 W amplifier and a dipole of plain copper wire. **10 mW of transmit power disrupted the link from 10 m.** Through the floor of a limestone building — attacker one storey below, ~6 m including a 20 cm ceiling — about 100 mW sufficed. The comparison that frames the result: broadband noise jamming essentially does not work against HPGP's robust (ROBO/QPSK) modes. Driving Gaussian white noise at up to 20 W at 1 m produced **no degradation at all** — the preamble attack outperforms noise jamming by over three orders of magnitude, because it exploits the protocol's politeness rather than overpowering the signal.

**Real-world results.** Eight vehicles (anonymised in the paper as Vehicles A–H, spanning subcompact to shooting-brake classes, 50–270 kW charging capacity) and 20 DC charging stations, across both plug variants (Combo 1/2) and both application standards (DIN 70121, ISO 15118): **the attack succeeded in every observed combination**. The longest demonstrated range was **47 m at just under 700 mW** — attacker across a road intersection from the victim; at the other extreme, one vehicle was stopped from 1.5 m with the bare SDR at ~0.3 mW. Power requirements varied by site (two vehicles at 10 m needed ~600 mW, against <10 mW in the lab — the uncontrolled electromagnetic environment is the paper's own explanation), and liquid-cooled cables made no difference (the coolant does not wrap the CP/PE pair). Scenarios demonstrated include a slow drive-by at ~10 mph (so wardriving works), attacks from a closed trunk with a coiled antenna, through perimeter fences, and with no line of sight: **three vehicles charging at once were disrupted simultaneously**, and in a car-park test 20 vehicles stood within range. A coverage model converts range into scale: 25 m covers the area of ~80 standard EU/UK bays. The prototype cost under $1,000, and a later battery version ran over 10 hours from a power bank — rucksack- or drone-portable, or plantable for remote operation.

**Impact framing.** The threat model distinguishes a single targeted vehicle, fleet denial (delivery, bus, and emergency-service fleets charge densely and on schedule), and widespread disruption of charging hubs — megawatts of controllable load, with vehicle-to-grid services set to deepen the grid coupling. CCS derivatives inherit the link: the Megawatt Charging System and SAE J3105 both use ISO 15118 over PLC, and the authors see no fundamental reason the attack would not transfer (neither was tested). One tested ISO 15118-20 domestic AC bidirectional charger was equally susceptible — the growth direction as home chargers adopt the same communication.

**Countermeasures.** None is a fix; each only raises the attacker's budget. Electromagnetic hardening helps partially (a coaxial construction raised the required power at 3 m from 1.4 mW to 8.5 mW) but at roughly $1,200 per replacement cable it cannot retrofit the installed base. Raising the preamble-detection SNR threshold is the same arms race in software. Automatic session re-establishment — safe, the authors argue, while the Proximity Pilot shows the cable never left the vehicle — reduces the harm of one-off attacks without touching the vulnerability. Modem-internal counters can detect the attack's impossible signature. The cheapest effective measure is counterintuitive: **add noise**. A small noise source at the modem raises the floor the preamble must beat; 25 mV of injected noise multiplied the required transmit power fifty-fold at 1 m (0.37 mW → 20.6 mW) and defeated the authors' 1 W setup at 10 m.

## Where it fits

Scope, as with its predecessor: this is the **vehicle↔charger link** only — the cable in the parking bay, never the [OCPP](concepts/ocpp-charging-attacks.md) charger↔backend link. Within that link it completes a pair with [Losing the Car Keys](losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging.md): the same single-ended wiring that makes CCS traffic *readable* from the next bay (confidentiality) makes it *stoppable* from across the street (availability), and both flaws are properties of the standard's design, not of any vendor's implementation — every compliant HPGP modem must implement CSMA/CA, and every known implementation exhibits the behaviour. A detail worth keeping: SLAC, the association protocol the earlier paper found running in plaintext, exists partly because of this same cross-talk — it is how a vehicle avoids pairing with a neighbouring charger it can overhear.

## Limits and safety notes

As the paper states them: **Range and power are environment-dependent.** Real-world requirements varied by orders of magnitude between sites; the 47 m figure is a best case, not a specification. **Selectivity is poor:** at range, nearby vehicles are affected together — singling out one vehicle is hard, because directional antennas at these frequencies are large. **Transfer beyond the tested set is argued, not shown:** further vehicles and chargers, HPGP modems other than the QCA7000, the MCS and SAE J3105 derivatives, and any PWM-fallback behaviour (a specified option, never observed) rest on a standards-compliance argument, not measurement. The laboratory distance series runs to 10 m; longer-range prediction leans on a Friis-equation comparison the authors themselves qualify (near-field mismatch). The ~12 million affected-vehicle figure is the paper's 2023 estimate. Ethics and disclosure: tests ran only when no other vehicles were charging, at sites with no other charging parks in range, capped at 1 W outside the lab, in collaboration with a government department and a local charge-point operator; findings were disclosed to CharIN, Auto-ISAC, and government bodies, the code was embargoed during disclosure and is now public, and the work is recorded as CVE-2022-0878.

## Status and sources

Status: **published** — a finished 2023 conference publication. DOI [10.14722/ndss.2023.23251](https://doi.org/10.14722/ndss.2023.23251), verified against Crossref (record's title, all four authors, NDSS 2023 event, and publisher match the paper), 2026-11-01. Full text read end-to-end, appendices included, from the authors' Oxford copy of the NDSS version, 2026-11-01. Evaluation code: github.com/ssloxford/brokenwire.

## Related

- [Losing the Car Keys: Wireless PHY-Layer Insecurity in EV Charging](losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging.md) — the same lab's passive attack on the same physical layer: reading the emissions Brokenwire transmits into
- [Charge It to My Neighbor: a Relay Attack on ISO 15118 Plug & Charge Payment](charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment.md) — the authorisation layer above the session this attack aborts
- [pyPLC](pyplc.md) — the CCS toolkit implementing the SLAC/ISO 15118 state machines whose medium access this attack starves
- [OCPP and charging attacks](concepts/ocpp-charging-attacks.md) — the other charging link (charger↔backend), linked to keep the boundary explicit
