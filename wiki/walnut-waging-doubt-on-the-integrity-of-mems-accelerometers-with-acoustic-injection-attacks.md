---
title: "WALNUT: Waging Doubt on the Integrity of MEMS Accelerometers with Acoustic Injection Attacks"
summary: "Trippel, Weisse, Xu, Honeyman, and Fu, IEEE EuroS&P 2017. Acoustic resonance attacks that forge accelerometer output, establishing analogue sensor integrity…"
type: entity
category: "Research Papers"
url: "https://spqrlab1.github.io/papers/trippel-IEEE-oaklawn-walnut-2017.pdf"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Trippel, Weisse, Xu, Honeyman, and Fu, IEEE EuroS&P 2017. Acoustic resonance attacks that forge accelerometer output, establishing analogue sensor integrity as its own threat model."
sources:
  - url: "https://spqrlab1.github.io/papers/trippel-IEEE-oaklawn-walnut-2017.pdf"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1109/EuroSP.2017.42"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving
---

Trippel, Weisse, Xu, Honeyman, and Fu, IEEE EuroS&P 2017. Acoustic resonance attacks that forge accelerometer output, establishing analogue sensor integrity as its own threat model.

## What it is

Timothy Trippel, Ofir Weisse, Kevin Fu, and Peter Honeyman (University of Michigan) with Wenyuan Xu (University of South Carolina). *IEEE European Symposium on Security and Privacy (EuroS&P) 2017*, Paris, 26–28 April 2017, pp. 3–18. DOI: [10.1109/EuroSP.2017.42](https://doi.org/10.1109/EuroSP.2017.42) (verified via Crossref; the author PDF is marked "To Appear"). WALNUT is an **analogue sensor-integrity** attack: sound at a capacitive MEMS accelerometer's mechanical resonant frequency displaces its sensing mass exactly as real acceleration does, so the sensor's output becomes a linear combination of true acceleration and the acoustic signal (model validated experimentally). Two signal-conditioning flaws turn resonance into forged output:

- **Insecure low-pass filter** — cutoff above or too close to the resonant frequency, so the resonant signal reaches the ADC undersampled and **aliases** to a *fluctuating* false measurement (**output biasing** class).
- **Insecure amplifier** — the resonant signal exceeds the amplifier's dynamic range and is **asymmetrically clipped**, producing a DC component the LPF passes, i.e. a *constant shifted* false measurement (**output control** class).

**Threat model.** The attacker cannot read the digitised sensor output or touch the sensor, but can obtain an identical device to profile. Sound in the **2–30 kHz** band is delivered by an external speaker, or by a speaker in/at the device itself (victim tricked into playing malicious audio, or remotely exploited multimedia software — the paper's "drive-by ditty"; co-located speaker = **self-stimulation attack**, standoff ~zero).

## What it showed

- **Survey:** **20 sensor models × 2 instances = 40 sensors, 5 manufacturers** (Bosch, STMicroelectronics, InvenSense, Analog Devices, Murata), swept 2–30 kHz in 50 Hz steps at ~110 dB SPL, speaker 10 cm above, false output = ≥0.1 g deviation. **15/20 models (75%) vulnerable to output biasing; 13/20 (65%) to output control.** Both instances of every model behaved identically — resonant frequency is a model property, so an attacker can profile one unit and attack another. Largest false amplitude: ADXL345 at 7.9 g. The Murata automotive parts were largely resistant (SCA610, SCA1000, SCA2100: no resonance found; SCA820 and SCA3100: output control only, ≤0.15 g); the paper observes most unaffected sensors are physically larger.
- **Output biasing:** tuning the acoustic frequency to the resonance plus an integer multiple of the ADC sampling frequency aliases the signal to DC; amplitude or phase modulation shapes the forged signal (PM gives both polarities/full range; AM one half). Demonstrated spelling "WALNUT" on digital sensors (ADXL350 via PM, ADXL345 via AM) but controllable only **1–2 seconds** (sampling-phase drift), and on analogue sensors with accurate ADCs (ADXL337, LIS344ALH) for tens of seconds.
- **Output control:** amplitude-modulating the clipping needs **no aliasing** and gives **indefinite full control** regardless of ADC sampling regime; demonstrated spelling "WALNUT" on the MIS2DH and MPU6500 at up to 1 g peak-to-peak — the most stable of the three demos.
- **End-to-end (a): Fitbit One.** External speaker at the tracker's resonant frequency, **no modulation needed** (fluctuating output suffices for step counting): ~40 minutes produced **2,100 registered steps and 21 Higi.com rewards points** (the abstract frames the rate as ~3,000 steps/hour with a $5 speaker). Rewards were **not claimed**; manufacturers were notified.
- **End-to-end (b): self-stimulation.** A **Samsung Galaxy S5** (InvenSense MPU6500) playing a malicious WAV file **from its own speaker** forged X-axis accelerometer readings that steered an RC car via the i-Spy Toys app (WiFi/TCP): the audio drove the car forward, backward, and to a stop. Packaging shifts resonance slightly inside phones and attenuates amplitude (Galaxy Note 3: 0.4 g).

## Defences (paper §8)

- **Hardware:** a **secure LPF** (cutoff below half the sampling frequency with the transition band not overlapping resonance — via lower cutoff, narrower transition band, or stiffer spring/higher resonance, each with stated costs); a **secure amplifier** (larger dynamic range, or pre-filtering amplifier inputs at resonant frequencies); **acoustic dampening** materials. Per the paper's Table 3, only secure-LPF-plus-amplifier and dampening defeat **both** attack classes.
- **Software** (firmware-updatable, but they **only mitigate output biasing, not output control**, and require analogue sensors with software-controlled ADCs): **randomised sampling** (random per-sample delay destroys DC-alias predictability; a moving average then recovers true acceleration) and **180° out-of-phase sampling** (sample pairs half a resonant period apart average the acoustic component away — a software notch filter). Both demonstrated attenuating spoofed signals.

## Where it fits

WALNUT establishes the analogue side channel as a sensor-integrity threat in its own right: the sensor is not buggy and no digital interface is attacked — the physics of the sensing element is the vulnerability, and the digital output is faithfully wrong. In this KB it is the acoustic member of the sensor-attack family whose automotive branch is [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md)'s optical attack on lidar: both exploit a transducer that cannot authenticate its physical input, and both find the flaw in the conditioning chain around the element rather than in software. Its automotive relevance is direct — accelerometers feed stability control and airbag systems — even though the end-to-end demos are a fitness tracker and a phone-steered RC car; the Murata automotive parts in the survey were also its most resistant.

## Limits and safety notes

- The attacker controls acoustic phase only relative to the sensor's **unknown sampling phase** — precise biasing attacks need hand-tuning or feedback, which is why digital-sensor control lasts only seconds.
- The survey used high sound pressure (~110 dB SPL) at 10 cm; real-world delivery depends on speaker proximity/power and device packaging.
- Disclosure was coordinated via ICS-CERT; Analog Devices, Bosch PSIRT, InvenSense, and the Fitbit security team acknowledged.

## Status and sources

Status: **published** (finished 2017 publication). The author PDF was read in full for this page; pp. 3–18 and the event dates rest on the Crossref record (the PDF itself is marked "To Appear" and carries no proceedings pagination). One internal discrepancy in the paper: its body/Fig. 12 spell the STMicroelectronics part "MIS2DSH" while Table 1 lists "MIS2DH"; this page uses the Table 1 form. Project page: spqr.eecs.umich.edu/walnut.

## Related

- [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) — the optical analogue against lidar
- [Remote Attacks on Automated Vehicles Sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md)
