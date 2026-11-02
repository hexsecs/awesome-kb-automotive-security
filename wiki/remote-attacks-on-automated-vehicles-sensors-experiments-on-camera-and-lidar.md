---
title: "Remote Attacks on Automated Vehicles Sensors: Experiments on Camera and LiDAR"
summary: "Petit, Stottelaar, Feiri, and Kargl, Black Hat Europe 2015. First practical spoofing and blinding of automotive camera and LiDAR using commodity hardware."
type: entity
category: "Research Papers"
url: "https://blackhat.com/docs/eu-15/materials/eu-15-Petit-Self-Driving-And-Connected-Cars-Fooling-Sensors-And-Tracking-Drivers-wp1.pdf"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Petit, Stottelaar, Feiri, and Kargl, Black Hat Europe 2015. First practical spoofing and blinding of automotive camera and LiDAR using commodity hardware."
related: [potential-cyberattacks-on-automated-vehicles, illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications, walnut-waging-doubt-on-the-integrity-of-mems-accelerometers-with-acoustic-injection-attacks, adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://blackhat.com/docs/eu-15/materials/eu-15-Petit-Self-Driving-And-Connected-Cars-Fooling-Sensors-And-Tracking-Drivers-wp1.pdf"
    retrieved: 2026-11-01
---

Petit, Stottelaar, Feiri, and Kargl, Black Hat Europe 2015. First practical spoofing and blinding of automotive camera and LiDAR using commodity hardware.

## What it is

Jonathan Petit (Security Innovation), Bas Stottelaar and Michael Feiri (University of Twente), and Frank Kargl (University of Twente and University of Ulm). Black Hat Europe 2015 whitepaper; the full text was read from the paper PDF in the Black Hat materials archive (the stub's URL). **No DOI exists** for this paper (Crossref title query, 2026-11-01, returns no record for it). The paper's self-imposed constraints define it: only **remote** attacks (the attacker stays outside the target vehicle), only **black-box** attacks on the hardware layer, and only **commodity hardware — below US$60** in total. The systems under test are a **MobilEye C2-270** camera (a windshield-mounted driver-assistance unit: headway monitoring, pedestrian collision warning, lane departure warning, intelligent headlight control) and an **ibeo LUX 3** LiDAR (four-layer, rotating head with up to 110° view, up to 200 m range, up to three echoes per pulse, with an embedded Kalman-filter tracker following up to 65 objects classified as car/truck/bike/pedestrian/unknown). The automation model is Sense–Understand–Act; the paper attacks **Sense**, on the argument that fusion cannot work properly with "poor (or accurate but fake) raw sensor data."

**Attacker model** (adopted from Petit, Feiri & Kargl's *Revisiting attacker model for smart vehicles*, 2014): an external, active attacker with limited time and money, whose attack must be brief, cause no damage, and leave no trace, using low-sophistication commodity hardware. Three scenarios: **front/rear/side** (attack hardware in a second vehicle holding station next to the target), **roadside** (static installations, possibly several cooperating points), and **evil mechanic** (short physical access used to plant a device, e.g. a jammer on an unwitting carrier vehicle).

## What it showed

**Camera — blinding (§5.1).** Light sources (365 nm LED spot, white LED spot, 850 nm LED spot, 940 nm 5×5 LED matrix, 650 nm laser pointer) were fired at the MobilEye in bright (250 lx) and dark (0 lx) environments at 50–200 cm, effectiveness measured by tonal-distribution correlation of the 320×240 image. The **650 nm laser was the most effective source overall** — its blinding did not depend on environment, distance or power in these tests. Correlation rose with distance for everything else (inverse-square law); in bright conditions all non-laser sources sat at 0.95–1.0 correlation (little effect) except the white LED spot, while in darkness the cheapest source, the 940 nm LED matrix, was strongest. The paper is careful about the negative result: near-infrared sources did **not** fully blind the camera in the sustained-beam setup — but partial blinding suffices to hide objects, and LEDs mounted on a vehicle can make that vehicle unrecognizable to the MobilEye.

**Camera — confusing the auto controls (§5.2).** A burst attack on auto-exposure/auto-gain: switch the light on at full power and measure how long the image stays blinded while the iterative control loop restabilizes. With the 940 nm matrix at 50 cm in darkness the tonal correlation dropped from 1 to −0.012 and the camera was blinded for **5.3 seconds** (recovering 0.3 s after switch-off); several LED configurations blinded for over 5 s, and with the **650 nm laser the camera did not recover at all** (blinding time ∞ in the paper's table). Unlike the sustained attack, environment and distance mattered little. In the paper's application-layer test, a laser switched on against the MobilEye watching a simulated 130 km/h drive blanked its display: **the vehicle ahead was no longer detected**.

**LiDAR — relay (§6.1).** Two transceivers (an Osram SFH-213 photodetector, US$0.65, and an Osram SPL-PL90 laser, US$43.25) receive the LUX 3's 905 nm pulses at one point and re-emit them from another. No direct line of sight to the LiDAR is needed, because reflections travel past it. With transceivers one metre apart, the LiDAR — facing a wall at 1 m — additionally reported echoes from objects at **20 and 50 metres**. The demonstrated fact: the LUX 3's pulses are not encoded for the emitter that sent them, so pulses can be replayed and relayed into fake echoes.

**LiDAR — spoofing (§6.2).** Triggering off the victim's own pulse and re-emitting shaped copies after a controlled delay manufactures fake *objects*, not just echoes: copies of the 1 m wall were injected at ≈50 m, and multiple copies at 40, 50 and 70 m as second and third echoes, inside the 1.33 µs listening window the 200 m range implies. With the LUX 3's tracker attached, the fake walls were classified **"Unknown big" (sometimes "Car")** — and unstably: the same spoofed wall was re-identified as three new objects within 0.46 s. Replay and jamming attacks were also performed successfully but are not written up (the paper presents relay as replay's extension and spoofing as the developed form). The counterfeit objects' positions are controllable only **further away** than the attack hardware: an intrinsic 64 ns delay in cables and transceiver circuits set a 20 m floor for relayed objects and ≈40 m for spoofed copies (§7.1).

**Countermeasures proposed.** Camera: redundancy (the effective laser's beam was measured at ≈1.5 mm wide at 50 cm against a ≈5 mm lens, so one beam blinds one sensor — though a military "Dazzler" with a beam up to 12 cm is named as the counter-counterexample), near-infrared-cut filters (daytime-only unless switched, and a switchable filter gives the attacker a new lever), and photochromic materials. LiDAR: redundancy (multiple wavelengths; cross-checking against other vehicles' V2V reports — which opens its own attack surface), **random probing** (vary the pulse period non-predictably, or skip pulses and listen for answers to pulses never sent), probe-multiple-times (re-measure and reject outliers, at the cost of scan rate — four probes turn 50 Hz into 12.5 Hz), and shortening the pulse period (halving it halves the 200 m range to 100 m). Most are framed as software/firmware changes, because the automotive domain is cost-driven.

## Where it fits

This is the founding experimental paper of the KB's sensor-attack line, and it knows its place in the literature: its related-work section cites [Petit & Shladover](potential-cyberattacks-on-automated-vehicles.md) as having listed LiDAR and camera as attack surfaces "but no detail on how to perform attacks were given," and supplies the detail. [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) (Shin et al., CHES 2017) explicitly builds on it — "a spoofing-by-relaying attack improving on Petit et al.'s Black Hat Europe 2015 work against an IBEO LUX 3" — and removes its two hard limits: Dazzle's tool places fake points *closer* than the spoofer (impossible here, per §7.1) and adds saturation as a second attack class, against a Velodyne VLP-16 rather than the LUX 3. [WALNUT](walnut-waging-doubt-on-the-integrity-of-mems-accelerometers-with-acoustic-injection-attacks.md) is the labelled analogue on a different physical channel: both papers attack a sensor through the analogue quantity it exists to measure, black-box, with cheap commodity hardware, against a device that cannot authenticate its own input — WALNUT through acoustic resonance in MEMS accelerometers, this paper through light.

## Limits and safety notes

The paper's own discussion (§7) is unusually explicit, and this page keeps its limits rather than the abstract's stronger wording ("effective blinding, jamming, replay, relay, and spoofing"):

- **Laboratory only.** All experiments were indoors; no range tests were performed on the LiDAR attacks, and outdoor attacks on moving vehicles are future work. Aiming is the camera attack's practical problem (a 1.5 mm beam), synchronization the LiDAR attack's; the authors "expect similar results in outdoor experiments" — an expectation, not a result.
- **Nothing closer than the attacker.** Relayed objects could not be placed nearer than 20 m, spoofed copies nearer than ≈40 m (the 64 ns intrinsic delay); closer-than-spoofer spoofing had to wait for Shin et al.
- **Range shrinks the attack.** At 100 m the gap between successive LUX pulses is ≈1.47 m against a 5 mm photodetector aperture — catching pulses at distance needs multiple detectors, and distance also eats the 1.33 µs attack window.
- **Raw-data level only.** Both devices were tested below their processing stacks; how a full automation system reacts to malicious sensor data was explicitly not tested (the object-tracker experiments and §7.4's discussion — including flooding the 65-object tracker into a denial of service — are indications, not end-to-end demonstrations).

## Status and sources

Status: **published** — a finished 2015 conference publication; no living artefact. Sources: the paper PDF from the Black Hat Europe 2015 materials archive (the stub's URL), read in full 2026-11-01; Crossref queried 2026-11-01 (no DOI record exists for this paper); the KB's Illusion and Dazzle and WALNUT pages for the forward links; the list.

## Related

- [Potential Cyberattacks on Automated Vehicles](potential-cyberattacks-on-automated-vehicles.md) — the taxonomy this paper experiments under
- [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) — its direct successor on LiDAR
- [WALNUT](walnut-waging-doubt-on-the-integrity-of-mems-accelerometers-with-acoustic-injection-attacks.md) — the acoustic analogue
- [Adversarial Sensor Attack on LiDAR-based Perception in Autonomous Driving](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) — the perception-layer descendant
