# Facet: Sensors & perception

LiDAR, camera, radar, GNSS and physical-channel attacks.

Generated from page frontmatter by tools/ingest.py; 27 pages. Do not edit by hand.

## RF and Key Fob Analysis

- [rtl_433](rtl-433.md) — Generic ISM band receiver for decoding TPMS sensors and key fobs at 315/433/868/915 MHz with RTL-SDR.

## Infotainment and IVI

- [gen5fw](gen5fw.md) — Python tools for decrypting, patching, and redeploying firmware on Mobis Gen5 navigation head units in Hyundai, Kia, and Genesis vehicles, including…

## Datasets

- [VeReMi Extension](veremi-extension.md) — Simulated V2X misbehavior detection dataset generated with F2MD over the Luxembourg SUMO scenario, labelling position, speed, timing, replay, DoS, and Sybil…

## Research Papers

- [A First Physical-World Trajectory Prediction Attack via LiDAR-induced Deceptions in Autonomous Driving](a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving.md) — Lou et al., USENIX Security 2024. Attacks trajectory prediction indirectly, by placing physical objects that deceive LiDAR perception, instead of…
- [Adversarial Sensor Attack on LiDAR-based Perception in Autonomous Driving](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) — Cao et al., ACM CCS 2019. Spoofs LiDAR returns to inject a fake obstacle into the perception pipeline of a production autonomous driving stack.
- [All Your GPS Are Belong To Us: Towards Stealthy Manipulation of Road Navigation Systems](all-your-gps-are-belong-to-us-towards-stealthy-manipulation-of-road-navigation-systems.md) — Zeng et al., USENIX Security 2018. Spoofs GPS to reroute a driver to an attacker-chosen destination while keeping the displayed route plausible.
- [Does Physical Adversarial Example Really Matter to Autonomous Driving? Towards System-Level Effect of Adversarial Object Evasion Attack](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md) — Wang et al., ICCV 2023. Measures published physical adversarial attacks against a full driving pipeline rather than the perception model alone, and finds…
- [Drift with Devil: Security of Multi-Sensor Fusion based Localization in High-Level Autonomous Driving under GPS Spoofing](drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing.md) — Shen et al., USENIX Security 2020. Shows sensor fusion does not neutralise GPS spoofing, taking an autonomous vehicle off its lane with gradual position drift.
- [Illusion and Dazzle: Adversarial Optical Channel Exploits Against Lidars for Automotive Applications](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) — Shin, Kim, Kwon, and Kim, CHES 2017. Saturates and spoofs an automotive LiDAR over its optical channel, creating fake points and blinding it entirely; the…
- [Invisible for both Camera and LiDAR: Security of Multi-Sensor Fusion based Perception in Autonomous Driving](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md) — Cao et al., IEEE S&P 2021. Defeats the multi-sensor fusion designs that production stacks actually use, with a single adversarial object invisible to camera…
- [On the Realism of LiDAR Spoofing Attacks against Autonomous Driving Vehicle at High Speed and Long Distance](on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance.md) — Sato et al., NDSS 2025. Moving-vehicle spoofing rig and an adaptive high-frequency removal attack that succeed at 60 km/h and 110 m against production…
- [Perspective-Shift Attacks Against Optical Perception Sensors: A Novel Attack Vector on LiDAR and Camera](perspective-shift-attacks-against-optical-perception-sensors-a-novel-attack-vector-on-lidar-and-camera.md) — Calipari et al., USENIX VehicleSec 2026. Introduces a new physical attack class that uses Direction Turning Film to shift LiDAR and camera fields of view…
- [Remote Attacks on Automated Vehicles Sensors: Experiments on Camera and LiDAR](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) — Petit, Stottelaar, Feiri, and Kargl, Black Hat Europe 2015. First practical spoofing and blinding of automotive camera and LiDAR using commodity hardware.
- [Security and Privacy Vulnerabilities of In-Car Wireless Networks: A Tire Pressure Monitoring System Case Study](security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md) — Rouf et al., USENIX Security 2010. Shows TPMS sensors are unauthenticated and trackable at roughly 40m, the first published wireless in-car network attack.
- [SoK: How Sensor Attacks Disrupt Autonomous Vehicles: An End-to-end Analysis, Challenges, and Missed Threats](sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats.md) — Zhang et al., arXiv 2025. Traces how sensor-induced errors propagate through perception, localization, planning, and control to physical impact, and…
- [SoK: The Next Frontier in AV Security: Systematizing Perception Attacks and the Emerging Threat of Multi-Sensor Fusion](sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion.md) — Khan, Islam, and Hasan, arXiv 2026. Systematizes 48 studies of perception-layer attacks into a taxonomy of 20 attack vectors and shows how…
- [The Heat is On: Understanding and Mitigating Vulnerabilities of Thermal Image Perception in Autonomous Systems](the-heat-is-on-understanding-and-mitigating-vulnerabilities-of-thermal-image-perception-in-autonomous-systems.md) — Bhupathiraju et al., NDSS 2026. Shows heat sources degrade thermal-camera pedestrian detection and sensor fusion, including in real driving, and proposes…
- [WALNUT: Waging Doubt on the Integrity of MEMS Accelerometers with Acoustic Injection Attacks](walnut-waging-doubt-on-the-integrity-of-mems-accelerometers-with-acoustic-injection-attacks.md) — Trippel, Weisse, Xu, Honeyman, and Fu, IEEE EuroS&P 2017. Acoustic resonance attacks that forge accelerometer output, establishing analogue sensor integrity…

## Conference Presentations

- [Back in the Driver's Seat: Recovering Critical Data from Tesla Autopilot Using Voltage Glitching](back-in-the-driver-s-seat-recovering-critical-data-from-tesla-autopilot-using-voltage-glitching.md) — Kuhnapfel, Werling, and Jacob, 37C3 2023. Voltage-glitching attack that gives root on Tesla Autopilot hardware and recovers protected data.
- [DriveThru Car Hacking: Fast Food, Faster Data Breach](drivethru-car-hacking-fast-food-faster-data-breach.md) — Chen et al., Black Hat Asia 2025. Attack chain against more than 24 dashcam models, delivered through a drive-through ordering flow, with an accompanying tool.
- [Over the Air: Compromise of Modern Volkswagen Group Vehicles](over-the-air-compromise-of-modern-volkswagen-group-vehicles.md) — Ivachev and Parnishchev, Black Hat Europe 2024. Bluetooth attack chain against Volkswagen Group MIB3 infotainment yielding persistent code execution…
- [Passive and Active Attacks on TPMS Systems](passive-and-active-attacks-on-tpms-systems.md) — Yago Lizarribar, DEF CON 33 Car Hacking Village 2025. Slides on long-term passive tracking of tire pressure sensors and active spoofing, both with commodity…

## Books

- [Automotive Cybersecurity: Protecting Connected and Autonomous Vehicles](automotive-cybersecurity-protecting-connected-and-autonomous-vehicles.md) — Alfred Basta and Sam Hana, Kendall Hunt 2026. Textbook covering threats from ECU networks and sensor spoofing to OTA patching, EV charging breaches, and…
- [Offensive Automotive Cybersecurity](offensive-automotive-cybersecurity.md) — Ahmad MK Nasser and Dennis Kengo Oka, Packt 2026. The two handbook authors together on the offensive side, covering exploitation of modern automotive platforms.

## Learning Resources

- [Fleet Cyber Challenge](fleet-cyber-challenge.md) — NMFTA's free self-paced capture-the-flag lab for commercial vehicle security, with scenarios on CAN traffic analysis, ELD compromise, GPS spoofing, firmware…

## Concepts

- [LIN as the trusted subordinate bus](concepts/lin-bus.md) — LIN sits behind gateways on door modules and sensors, so it is treated as trusted — yet its wiring is often the most reachable.
- [Physical-channel sensor attacks](concepts/physical-channel-sensor-attacks.md) — Attacks that manufacture the measurement itself — in acoustics, optics, RF, and heat — where no digital interface is touched and the output is faithfully wrong.
