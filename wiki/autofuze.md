---
title: "AutoFuze"
summary: "Python toolkit for fuzzing and penetration testing ECUs over UDS, XCP, SOME/IP, and OBD, across CAN, DoIP, USB, and SPI transports."
type: entity
category: "Penetration Testing"
url: "https://github.com/DanAurea/AutoFuze"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python toolkit for fuzzing and penetration testing ECUs over UDS, XCP, SOME/IP, and OBD, across CAN, DoIP, USB, and SPI transports."
related: [pyxcp, python-doipclient, someip-protocol-fuzzer, caringcaribou, nullsec-carfuzz, someip]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/DanAurea/AutoFuze"
    retrieved: 2026-11-01
  - url: "https://github.com/DanAurea/AutoFuze/blob/master/README.md"
    retrieved: 2026-11-01
---

Python toolkit for fuzzing and penetration testing ECUs over UDS, XCP, SOME/IP, and OBD, across CAN, DoIP, USB, and SPI transports.

## What it is

A Python toolkit for communicating with automotive ECUs in order to fuzz and penetration-test them. It implements the main AUTOSAR-era diagnostic and calibration protocols — UDS, XCP, SOME/IP and SOME/IP-SD, and OBD — as readable Python libraries with playground and tester code on top, aimed at automated ECU testing rather than interactive use. It is a single-author project; there is no licence file in the repository, so reuse terms are unstated.

## How it works

The repository is organised by concern: `protocols/` holds one package per protocol (`uds`, `xcp`, `obd`, `some_ip`, `some_ip_sd`), with `core/`, `network/`, `tester/`, `playground/` and `test/` alongside. Per the README's protocol matrix, UDS runs over Ethernet (DoIP) and CAN; XCP runs over USB, Ethernet, SxI (serial) and CAN — the README notes UDS and XCP are the practically important pair because they reach software flashing, NVM updates and other embedded parameters. SPI appears in the list only as "check whether it's interesting or not" — aspirational, not implemented. The fuzzing angle is architectural rather than a named fuzzer module: the protocol stacks are exposed as Python APIs so tests can mutate and replay diagnostic and calibration traffic programmatically. The most recent work (HEAD, 2024-01-18) is on the XCP path.

## Where it fits

The broadest protocol-coverage entry in this section: the one toolkit spanning diagnostics (UDS), calibration (XCP), and Ethernet service protocols (SOME/IP) in a single codebase. It complements the single-protocol libraries elsewhere in the KB — [pyxcp](pyxcp.md) for XCP, [python-doipclient](python-doipclient.md) for DoIP, [someip-protocol-fuzzer](someip-protocol-fuzzer.md) for SOME/IP — overlaps [CaringCaribou](caringcaribou.md) on UDS-over-CAN testing with breadth traded against focus, and is the Python counterpart to [NullSec CarFuzz](nullsec-carfuzz.md)'s Rust fuzzing of the same protocol family.

## Limits and safety notes

The README's own disclaimer sets the design envelope: "This toolkit hasn't been done to provide a high performance library but a readable one with focus on maintainability" — throughput-critical fuzzing campaigns are out of scope by design. SPI support is unimplemented (above). The README names no specific CAN interface hardware or vehicle prerequisites, and carries no safety warnings; which physical interfaces the CAN and DoIP paths expect is not documented there.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived and received commits spread across 2020–2024, the latest on 2024-01-18 (XCP fixes and playground update); there are no releases. Observable life, but nothing in roughly the last 22 months. Documentation claims above come from the following primary sources; no ECU was connected for this page.

- [Upstream repository](https://github.com/DanAurea/AutoFuze)
- [Upstream README](https://github.com/DanAurea/AutoFuze/blob/master/README.md)

## Related

- [pyxcp](pyxcp.md)
- [python-doipclient](python-doipclient.md)
- [someip-protocol-fuzzer](someip-protocol-fuzzer.md)
- [CaringCaribou](caringcaribou.md)
- [NullSec CarFuzz](nullsec-carfuzz.md)
- [SOME/IP and SOME/IP-SD](concepts/someip.md)
