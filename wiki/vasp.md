---
uid: 01a1e6dc-fe85-71e9-83dc-76304f7c4065
title: "VASP"
summary: "V2X Application Spoofing Platform from Qualcomm that runs a library of BSM spoofing and falsification attacks on top of Veins, the artifact of the…"
type: entity
category: "V2X Security"
url: "https://github.com/quic/vasp"
status: archived
last_checked: 2026-11-17
created: 2026-11-15
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: a570090
list_summary: "V2X Application Spoofing Platform from Qualcomm that runs a library of BSM spoofing and falsification attacks on top of Veins, the artifact of the VehicleSec 2023 paper; archived in 2026."
related:
  - veins
  - on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance
  - drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing
  - autohack
  - passive-and-active-attacks-on-tpms-systems
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-15
  - url: "https://github.com/quic/vasp"
    retrieved: 2026-11-17
  - url: "https://raw.githubusercontent.com/quic/vasp/main/README.md"
    retrieved: 2026-11-17
  - url: "https://api.github.com/repos/quic/vasp"
    retrieved: 2026-11-17
---

V2X Application Spoofing Platform from Qualcomm that runs a library of BSM spoofing and falsification attacks on top of Veins, the artifact of the VehicleSec 2023 paper; archived in 2026.

## What it is

VASP (V2X Application Spoofing Platform) is Qualcomm's research framework for simulating attacks on V2X networks. It is a submodule that sits on top of the [Veins](veins.md) vehicular network simulator and provides a library of Basic Safety Message (BSM) spoofing and falsification attacks. It is the artifact of the VehicleSec 2023 paper by Ansari, Petit, Monteuuis and Chen, and is MIT-licensed.

## How it works

VASP does not implement its own network stack or traffic model: it relies on a specific toolchain pinned in the README — OMNeT++ 5.6.2 (built with `CXXFLAGS=-std=c++14`), SUMO 1.8.0 and Veins 5.2, plus two headers dropped into the system include directory (`CSVWriter.h` and nlohmann `json.hpp` renamed to `json.h`). The repo is added as a submodule under `<veins>/src/vasp`, then the whole Veins tree is configured and built. Simulations run by starting `veins_launchd`, changing to `src/vasp/scenario/` and running `./run [-u Cmdenv]`, which writes a trace file into `scenario/results`. Documentation covers configuring a scenario, reading the trace-file columns and implementing a new attack; authors are asked to cite the VehicleSec 2023 paper.

## Where it fits

VASP is the application-layer spoofing counterpart to [Veins](veins.md) itself: where Veins supplies the simulation, VASP supplies adversarial BSM behaviour for evaluating V2X applications and misbehaviour detection. It sits in the same V2X security neighbourhood as [AutoHack](autohack.md), and its sensor-spoofing siblings — [on the realism of LiDAR spoofing attacks](on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance.md) and [Drift with Devil](drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing.md) — cover the perception side of the same threat model. [Passive and active attacks on TPMS systems](passive-and-active-attacks-on-tpms-systems.md) is the other short-range wireless case in the corpus.

## Limits and safety notes

The repository was **archived by its owner** and was last pushed 2023-03-28, so treat it as a historical reference implementation, not a maintained tool: the pinned OMNeT++/SUMO/Veins versions are old and may not build on current systems, and the archive means no upstream fixes. It is a simulation framework — nothing here was executed against real vehicles or roadside units, and no simulation was run for this page. Its attack library models falsified BSMs at the application layer; it is not a radio transmitter or a key-extraction tool, and results depend entirely on how the scenario is configured.

## Status and sources

Checked 2026-11-17. **Archived** at this check: public, archived, MIT, 25 stars / 12 forks / 1 open issue, last default-branch push 2023-03-28. The VehicleSec 2023 paper remains the citation for the design.

- [Upstream README](https://raw.githubusercontent.com/quic/vasp/main/README.md)
- [Repository metadata](https://api.github.com/repos/quic/vasp)
- [VehicleSec 2023 paper](https://doi.org/10.14722/vehiclesec.2023.23071)

## Related

- [Veins](veins.md)
- [On the realism of LiDAR spoofing attacks against autonomous driving vehicles](on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance.md)
- [Drift with Devil: security of multi-sensor fusion based localization under GPS spoofing](drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing.md)
- [AutoHack](autohack.md)
- [Passive and active attacks on TPMS systems](passive-and-active-attacks-on-tpms-systems.md)
