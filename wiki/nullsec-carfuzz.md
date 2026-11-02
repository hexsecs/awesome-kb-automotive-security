---
title: "NullSec CarFuzz"
summary: "Rust fuzzer for CAN, UDS, OBD-II, and DoIP with grammar-aware test generation and coverage tracking."
type: entity
category: "Penetration Testing"
url: "https://github.com/bad-antics/nullsec-carfuzz"
status: maintenance
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Rust fuzzer for CAN, UDS, OBD-II, and DoIP with grammar-aware test generation and coverage tracking."
related: [autofuze, truckdevil, uds-seed-key, caringcaribou]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/bad-antics/nullsec-carfuzz"
    retrieved: 2026-11-01
  - url: "https://github.com/bad-antics/nullsec-carfuzz/blob/main/USAGE.md"
    retrieved: 2026-11-01
---

Rust fuzzer for CAN, UDS, OBD-II, and DoIP with grammar-aware test generation and coverage tracking.

## What it is

A Rust command-line fuzzer for automotive protocols, written as part of the NullSec Linux security distribution's automotive suite. It generates test traffic for CAN, UDS (ISO 14229), OBD-II (ISO 15031) and DoIP (ISO 13400) targets, using knowledge of each protocol's grammar to build edge-case messages rather than purely random bytes, and watches ECU responses to guide further mutation and to detect crashes — ECU resets, hangs, and error responses. Licence: MIT.

## How it works

A single Rust binary (the whole implementation is three source files) that talks to the target over a SocketCAN-style interface — every documented example uses `--interface can0`, including the DoIP examples, so a CAN interface is the documented transport even for the IP-based protocol. The README's feature set: grammar-aware mutation per protocol; coverage tracking ("monitor ECU responses to guide mutation strategy"); a protocol state machine to reach deep states; a session manager handling diagnostic session changes and UDS security access; crash detection; and a report generator producing crash reports with reproduction steps. Its protocol table gives fuzzing depth per protocol: CAN 2.0A/B at frame level, UDS at service + sub-function, OBD-II at PID + mode, DoIP as "full TCP/UDP stack", XCP partial, KWP2000 at service level. USAGE.md documents safety features: `--rate-limit` to prevent bus flooding, `--filter` to restrict to specific arbitration IDs, `--timeout`, and `--dry-run` to validate without sending.

## Where it fits

The section's second fuzzing framework and the direct overlap with [AutoFuze](autofuze.md) — UDS/XCP/OBD fuzzing, but Rust and single-transport where AutoFuze is Python and multi-transport. Its J1939 mode (documented in USAGE.md only) neighbours [TruckDevil](truckdevil.md)'s J1939 fuzzer, and its security-access bruteforce mode belongs to the failure class in [UDS seed/key](concepts/uds-seed-key.md). It complements passive and analysis tooling such as [CaringCaribou](caringcaribou.md) rather than replacing it.

## Limits and safety notes

The README's own legal line is the operative constraint: "For authorized automotive security testing only. Never fuzz ECUs in vehicles in traffic." Documentation inconsistency is itself a limit: the README and USAGE.md describe two different command surfaces (subcommands vs flag-driven modes, with different protocol lists), and USAGE.md's quick start runs an `install.sh` that does not exist in the repository. The implementation is very small — three source files, six commits — so the deeper claims (coverage guidance, full DoIP stack) should be read as project claims, not established capability, and the documented feature breadth as aspirational until verified against a build.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived and was created in January 2026, but its six commits are thin and sporadic, the latest on 2026-04-04; there are no releases. Recent creation with some life, short of demonstrably active. Documentation claims above come from the following primary sources; no ECU was fuzzed for this page.

- [Upstream repository](https://github.com/bad-antics/nullsec-carfuzz)
- [USAGE.md](https://github.com/bad-antics/nullsec-carfuzz/blob/main/USAGE.md)

## Related

- [AutoFuze](autofuze.md)
- [TruckDevil](truckdevil.md)
- [UDS seed/key](concepts/uds-seed-key.md)
- [CaringCaribou](caringcaribou.md)
