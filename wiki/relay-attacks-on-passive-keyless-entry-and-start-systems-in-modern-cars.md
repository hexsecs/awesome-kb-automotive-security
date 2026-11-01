---
title: "Relay Attacks on Passive Keyless Entry and Start Systems in Modern Cars"
summary: "Francillon, Danev, and Capkun, NDSS 2011. Demonstrates the relay attack that still underpins most keyless vehicle theft today, against ten PKES systems from…"
type: entity
category: "Research Papers"
url: "https://www.ndss-symposium.org/ndss2011/relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars/"
status: unknown
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Francillon, Danev, and Capkun, NDSS 2011. Demonstrates the relay attack that still underpins most keyless vehicle theft today, against ten PKES systems from eight manufacturers."
sources:
  - url: "https://www.ndss-symposium.org/ndss2011/relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars/"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - key-fob-relay-attacks
  - comprehensive-experimental-analyses-of-automotive-attack-surfaces
  - security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study
---

Francillon, Danev, and Capkun, NDSS 2011. Demonstrates the relay attack that still underpins most keyless vehicle theft today, against ten PKES systems from eight manufacturers.

## What it is

The first systematic experimental demonstration that passive keyless entry and start (PKES) systems can be defeated by relaying their own radio signals — by Aurélien Francillon, Boris Danev, and Srdjan Capkun of ETH Zurich, at NDSS 2011, San Diego, February 2011. How PKES works, as the paper describes it: the car talks to the key on LF (120–135 kHz) — wake-up beacons followed by a challenge — and the key replies on UHF (315/433 MHz, roughly 10–100 m range). LF also does inside/outside region detection: in active mode the key is localized to 1–2 m; in passive backup mode (key placed at a predefined spot such as the start button) a battery-free LF RFID mode is used.

The root flaw, in the paper's terms: the car verifies that it *can communicate with* the correct key and treats communication neighbourhood as physical neighbourhood — "in adversarial settings communication neighborhood cannot be taken as a proof of physical proximity." The relay the paper builds works at the physical layer: it neither interprets nor modifies the signal, so it is completely independent of modulation, protocol, and any authentication or encryption — a PKES system using AES or RSA would still be vulnerable. Only the LF car-to-key direction needs relaying, because the key's UHF reply already travels 10–100 m on its own. The procedure: present the relay antenna at the door handle; the key emits the open authorization; move the relay antenna inside the car; the start challenge goes to the key; the engine starts. The lineage the paper names is mafia-fraud and wormhole attacks.

## What it showed

**Two relay realizations.** Over cable: two loop antennas joined by coaxial cable with an optional amplifier, capturing the LF field at the car and reproducing it at the key. Over the air: an emitter up-converts the LF signal to 2.5 GHz, amplifies and transmits it; a receiver down-converts back to LF and drives a loop antenna. The car-side relay device must sit within ≤30 cm of the car in their setup. **Total cost of the relay setups: between $100 and $1,000**, depending on components. Measured relay delays (LF channel): cable at 30 m — 160 (±20) ns, "opening and starting the engine works reliably"; cable at 60 m — 350 (±20) ns; wireless at 30 m — 120 (±20) ns — against 15–20 µs for demodulating relays.

**The fleet.** Ten PKES systems from eight manufacturers (nine cars plus one lab-only aftermarket unit; models anonymized in the paper). The cable relay at 7, 30, and 60 m **always succeeded when tested**. Key excitation ranged from a few centimetres to 2 m unamplified, and **2–8 m with a 2–5 W amplifier — with the fob in the owner's pocket**. The cars' maximum acceptable response delays ranged from 35 µs to 10–20 ms, giving a theoretical relay reach of 10–3,000 km over air; the keys' own response-time spread (11–436 µs) makes timing-based detection infeasible, since the smallest spread dwarfs the relay's ~120 ns added delay. **No evaluated car stopped its engine when the key vanished after start.** The attack leaves no traces, and the car's logs show the *owner's* key.

**Countermeasures, in the paper's three tiers.** Owner measures — Faraday shielding of the fob, battery removal — are effective but disable PKES's convenience. Mid-term measures (a button to disable PKES, restrictions on handle-pull unlocking) are deterrents that do not prevent the attack. Literature measures — signal strength, signal properties, corruption detection, multi-channel checks — are assessed as weak. The paper's own proposal is **RF distance bounding**: a 30 m cable relay adds about 250 ns of round-trip delay, so detection needs a round-trip-time standard deviation under ~6 ns for a 1 m bound; the paper cites a 62 ps prover variance from the distance-bounding literature as feasibility evidence, and verifiable multilateration with at least three in-car nodes for the start check.

## Where it fits

This is the anchor paper for the KB's [key-fob relay attacks](concepts/key-fob-relay-attacks.md) concept page: the attack class it demonstrates — pure signal relay against proximity assumptions — is the technique behind the keyless-theft wave that followed, and its distance-bounding proposal frames the countermeasure discussion the concept page carries forward. It is also the third of the 2010–11 wireless-entry results in this batch, alongside [Rouf et al.'s](security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md) TPMS work and [Checkoway et al.'s](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md) remote attack surfaces.

## Limits and safety notes

Stated in the paper: the evaluated fleet is ten systems, models anonymized (this page does not name or guess them); the wireless relay was tested at 30 m, with longer distances argued achievable rather than demonstrated at kilometre scale; the distance-bounding countermeasure is a proposal with feasibility evidence from the literature, not a system the authors built into a car. The attack's practical precondition is proximity at both ends at once — one relay end at the car, the other within excitation range of the owner's fob. One internal inconsistency is noted for the record: the paper's response-time table and its text give different spread ranges for one model; this page rests nothing on the disputed figure.

## Status and sources

Status: **unknown** — a finished 2011 publication; no living artefact. No DOI is confirmed (NDSS papers of this era typically carry none). Full text openly available from NDSS and ETH author mirrors; read in full 2026-11-01.

## Related

- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md)
- [Comprehensive Experimental Analyses of Automotive Attack Surfaces](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md)
- [Security and Privacy Vulnerabilities of In-Car Wireless Networks: A Tire Pressure Monitoring System Case Study](security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md)
