---
uid: 01a19d3c-af88-78f7-bff4-12cd07cf4311
title: "Expanding the Attack Scenarios of SAE J1939: A Comprehensive Analysis of Established and Novel Vulnerabilities in Transport Protocol"
summary: "Lee, Lee, Jun, and Kim, escar USA 2024. Presents 14 attack scenarios against the J1939 protocol used in commercial vehicles, seven of them new."
type: entity
category: "Conference Presentations"
url: "https://zenodo.org/records/18715820"
status: published
last_checked: 2026-11-17
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Lee, Lee, Jun, and Kim, escar USA 2024. Presents 14 attack scenarios against the J1939 protocol used in commercial vehicles, seven of them new."
related:
  - pretty-j1939
  - truckdevil
  - cybersecurity-for-commercial-vehicles
  - reversing-a-brake-ecu-firmware-update
  - perspective-shift-attacks-against-optical-perception-sensors-a-novel-attack-vector-on-lidar-and-camera
  - fleet-cyber-challenge
  - j1939
  - the-vehicle-may-be-sick-denial-of-diagnostic-services-by-exploiting-the-can-transport-protocol
sources:
  - url: "https://zenodo.org/records/18715820"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
---

Lee, Lee, Jun, and Kim, escar USA 2024. Presents 14 attack scenarios against the J1939 protocol used in commercial vehicles, seven of them new.

## What it is

An escar USA 2024 conference paper (Michigan) by Hwejae Lee, Hyosun Lee, Saehee Jun and Huy Kang Kim, deposited on Zenodo as DOI 10.5281/zenodo.18715820 with the full 8.5 MB PDF attached. Its subject is the **SAE J1939** protocol family used in trucks, coaches and other commercial vehicles — a target the authors describe as far less examined than passenger-car CAN despite its extensive application. The paper's premise is that CAN IDS and vulnerability-analysis work accelerated after the UN Regulation, while J1939 lagged, raising safety concerns.

## How it works

The scope is deliberately narrow: the **Request** mechanism and the J1939 **Transport Protocol (TP)**, which carries messages longer than eight bytes via TP.CM (connection management) and TP.DT (data transfer) frames. Generic CAN attacks such as fuzzing, DoS, spoofing, replay, suspension and masquerade are excluded so the results stay J1939-specific.

The authors develop **14 attack scenarios**, seven drawn from prior research and seven newly proposed:

1. **Request overload** — flood a target ECU with Request messages (PGN 59904) so it can no longer serve normal traffic; in the testbed, engine-fluid PGN 65263 changed from a 0.5 s interval to irregular 0.27–0.72 s and displayed 0.
2. **Malicious Acknowledgment** — answer a Request with a false ACK/NACK/access-denied response so an active PGN appears inactive.
3. **Malicious TP.CM RTS** — inject a competing RTS declaring a different packet count or length; the receiver accepts the most recent one, causing lost data or aborted sessions.
4. **Connection exhaustion** — hold a session open with periodic TP.CM CTS messages so no legitimate multi-packet session can start.
5. **TP.CM BAM block** — the same session-occupation idea aimed at the ECU broadcasting BAM messages.
6. **Memory leak via TP.CM CTS 1**, 7. **2**, 8. **3** — request data packets starting beyond the originally declared count, reading memory the sender did not intend to release.
9. **TP.CM EndofMsgACK interruption** — disrupt session teardown.
10. **TP.Conn Abort interruption** — disrupt sessions with abort frames.
11. **Out of memory via TP.CM BAM** and 12. **via TP.CM RTS** — exhaust the receiver's multi-packet buffers.
13. **Overwrite memory via TP.DT** — corrupt a specific segment of a multi-packet transfer; the paper demonstrates altered data being acknowledged as a successful transfer.
14. **TP.DT spoofing** — inject surplus data frames before the legitimate session ends, aiming at buffer overflow.

The testbed uses **Au SAE J1939 simulators (Generation II)** with Kvaser USBcan Pro 2xHS v2 interfaces and Python injection scripts built on CANlib; the assumed attacker has unauthorised access to the J1939 bus, for example through infotainment or a parked vehicle's accessible wiring. Of the 14 scenarios, **11 executed successfully** in the authors' testbed. Their comparative table marks the Malicious Acknowledgment, Memory Leak CTS 3 and TP.DT spoofing scenarios as not producing the intended impact there. A key observation is that **some attacks inject only a single message**, which makes them correspondingly hard for an IDS to detect.

## What you get

The Zenodo deposit contains the full paper (not just slides): the scenario catalogue, testbed design, per-scenario results with figures and tables, and an appendix with the detailed scenario descriptions. It is the natural entry point for heavy-vehicle network security work and for anyone porting CAN IDS thinking to J1939.

## Where it fits

[pretty-j1939](pretty-j1939.md) is the protocol tooling for working with J1939, and [TruckDevil](truckdevil.md) is the research platform for commercial-vehicle networks. [Cybersecurity for commercial vehicles](cybersecurity-for-commercial-vehicles.md) and [Reversing a brake ECU firmware update](reversing-a-brake-ecu-firmware-update.md) cover the broader heavy-vehicle security context, and [Fleet Cyber Challenge](fleet-cyber-challenge.md) is the hands-on fleet programme. [The Vehicle May Be Sick](the-vehicle-may-be-sick-denial-of-diagnostic-services-by-exploiting-the-can-transport-protocol.md) is the directly analogous transport-protocol attack study on passenger-car ISO-TP by the same research group. [Perspective-Shift Attacks](perspective-shift-attacks-against-optical-perception-sensors-a-novel-attack-vector-on-lidar-and-camera.md) shares the Kim co-author.

## Limits and safety notes

These are **testbed demonstrations**, not attacks on a production truck in service, and three of the fourteen did not produce the intended impact in the authors' setup. The scope is the transport protocol layer, not every J1939 application profile; the paper says so explicitly. The attacker model assumes bus access already obtained. The Zenodo record was created in 2026 for a 2024 conference paper, so the deposit date is not the research date. No simulator, vehicle or bus was exercised for this page.

## Status and sources

Checked 2026-11-17. **Published** — escar USA 2024; full paper PDF open on Zenodo under DOI 10.5281/zenodo.18715820.

- [Zenodo proceedings deposit](https://zenodo.org/records/18715820)
- [DOI](https://doi.org/10.5281/zenodo.18715820)

## Related

- [pretty-j1939](pretty-j1939.md) — J1939 tooling for working with the protocol this paper attacks
- [TruckDevil](truckdevil.md) — a research platform for J1939/commercial-vehicle networks
- [Cybersecurity for Commercial Vehicles](cybersecurity-for-commercial-vehicles.md)
- [Reversing a brake ECU firmware update](reversing-a-brake-ecu-firmware-update.md)
- [Perspective-Shift Attacks Against Optical Perception Sensors](perspective-shift-attacks-against-optical-perception-sensors-a-novel-attack-vector-on-lidar-and-camera.md)
- [Fleet Cyber Challenge](fleet-cyber-challenge.md)
- [J1939 transport security](concepts/j1939.md)
