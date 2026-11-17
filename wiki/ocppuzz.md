---
uid: 01a1d968-3520-7d75-98ad-221f09f3698c
title: "OCPPuzz"
summary: "Specification-driven fuzzer for OCPP charging station management systems that extracts message rules and state transitions from the specification with a…"
type: entity
category: "EV Charging Security"
url: "https://github.com/jongchan-hong/OCPPuzz"
status: active
last_checked: 2026-11-17
created: 2026-11-14
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 46f5cc7
list_summary: "Specification-driven fuzzer for OCPP charging station management systems that extracts message rules and state transitions from the specification with a language model and reports deviations, uncovering denial-of-service and free-charging flaws in open-source systems."
related:
  - ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations
  - emuocpp
  - everest
  - truckdevil
  - race-to-charge-concurrency-bugs-and-state-integrity-violations-in-ev-charging-infrastructure
  - ocpp-charging-attacks
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-14
  - url: "https://github.com/jongchan-hong/OCPPuzz"
    retrieved: 2026-11-17
  - url: "https://raw.githubusercontent.com/jongchan-hong/OCPPuzz/main/README.md"
    retrieved: 2026-11-17
  - url: "https://api.github.com/repos/jongchan-hong/OCPPuzz"
    retrieved: 2026-11-17
facets: [ev-charging, attack, tools, standards]
---

Specification-driven fuzzer for OCPP charging station management systems that extracts message rules and state transitions from the specification with a language model and reports deviations, uncovering denial-of-service and free-charging flaws in open-source systems.

## What it is

OCPPuzz is an open-source testing framework for OCPP Charging Station Management Systems (CSMS), accepted at FSE 2026. Its distinguishing idea is to derive the oracle from the specification rather than from hand-written cases: message formats, rules and scenario state transitions are collected with an LLM from the OCPP documents and turned into constraints for generated tests. The target is the management system, not the charger firmware — it exercises how a CSMS handles protocol messages and state.

## How it works

The repository splits collection, generation and execution into separate stages. Three collector scripts — `message_direction_collector.py`, `rule_collector.py` and `scenario_collector.py` — need a GPT API token (the latter two also an AWS bucket) and populate a MySQL database with message direction, rule and scenario data. Parsing modules read the OCPP specification appendices and message JSON files; generator modules apply format, item, length, population and size constraints and mutate formats. A Kafka-backed test controller drives four bundled open-source CSMS targets — CitrineOS, OCPP.Core, ocpp-go and Maeve — each with its own docker-compose file, while `validator.py` records results in `results/`. The runtime prerequisites are Python 3.13+, Docker and ODBC Driver 17 for SQL Server; the default compose stack brings up the database, Kafka and ZooKeeper.

## Where it fits

OCPPuzz is the specification-driven counterpart to [OCPPStorm](ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations.md), which fuzzes OCPP implementations from a different angle; [EVerest](everest.md) is one of the open charging stacks such a fuzzer targets. [emuOCPP](emuocpp.md) and [TruckDevil](truckdevil.md) cover simulation and EV-charging exploitation respectively, and [Race to Charge](race-to-charge-concurrency-bugs-and-state-integrity-violations-in-ev-charging-infrastructure.md) is the closely related work on concurrency and state-integrity bugs in the same infrastructure. The upstream claim of denial-of-service and free-charging findings comes from the FSE 2026 paper; this page records the claim, not an independent reproduction.

## Limits and safety notes

The tool is research infrastructure, not a one-command scanner: it needs an LLM token, cloud storage, ODBC, Docker and a per-target CSMS build, and the paper's camera-ready version was not yet on the ACM Digital Library at this check. Because the oracle comes from an LLM reading the specification, findings are only as reliable as that extraction — a deviation may be a genuine implementation bug or an artefact of the inferred rule, and should be checked against the normative text before being reported. All bundled targets are local open-source systems; pointing a mutated OCPP stream at a production CSMS would be an attack on live billing and charging infrastructure and is out of scope. No Docker stack or fuzzing campaign was run for this page.

## Status and sources

Checked 2026-11-17. **Active** at this check: public, not archived, MIT, default branch last pushed 2026-06-03, with the associated paper accepted at FSE 2026. It had no stars, forks or open issues at this check — a very early research artifact, not a mature tool.

- [Upstream README](https://raw.githubusercontent.com/jongchan-hong/OCPPuzz/main/README.md)
- [Repository metadata](https://api.github.com/repos/jongchan-hong/OCPPuzz)

## Related

- [OCPPStorm: a comprehensive fuzzing tool for OCPP implementations](ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations.md)
- [emuOCPP](emuocpp.md)
- [EVerest](everest.md)
- [TruckDevil](truckdevil.md)
- [Race to Charge: concurrency bugs and state integrity violations in EV charging infrastructure](race-to-charge-concurrency-bugs-and-state-integrity-violations-in-ev-charging-infrastructure.md)
- [OCPP and charging attacks](concepts/ocpp-charging-attacks.md)
