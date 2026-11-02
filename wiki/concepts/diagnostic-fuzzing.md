---
uid: 01a19d3c-af60-75e8-872d-1adf279d3fb0
title: "Protocol-aware diagnostic fuzzing"
summary: "Fuzzing reaches the deep diagnostic states only when generation is grammar- and state-aware: sessions and SecurityAccess are the fuzzer's real problem."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [autofuze, nullsec-carfuzz, caringcaribou, cantoolz, udsim, diagnostic-service-abuse, simulation-and-test-doubles]
sources:
  - url: "https://github.com/nccgroup/autofuze"
    retrieved: 2026-11-01
  - url: "https://github.com/einride/can-tools"
    retrieved: 2026-11-01
---

Fuzzing is this corpus's oldest discovery method — [Koscher 2010](../experimental-security-analysis-of-a-modern-automobile.md)'s headline result began as fuzzing a proprietary service and correlating bits with behaviours — and the tool pages since have split into two kinds that share a name. **Frame-random mutation** generates malformed CAN frames and watches for effects; it finds disruption cheaply and Koscher's own verdict stands (a fuzzer is a near-universal *disruption* tool). **Protocol-aware fuzzing** exists because disruption is not the deep result: the states where the dangerous services live — programming sessions, routine execution, memory access — sit behind session management and SecurityAccess, and a mutator that cannot hold a session open, answer a seed, and sequence services in a valid order never reaches the code it exists to test. This page synthesises the strong instances' shared design, and says plainly, as its filing evaluation required, that several corpus pages' fuzzing claims are thin or aspirational — the page is written from the strong instances.

## Generation strategies

- **Random / bit-level mutation** of observed frames (the CAN fuzzing modules spread across [CANToolz](../cantoolz.md), [CaringCaribou](../caringcaribou.md), [SavvyCAN](../savvycan.md)): cheap, broad, shallow — finds hangs, resets, and undefined behaviour in frame parsers; structurally unable to pass a seed/key gate.
- **Grammar-aware generation:** the fuzzer models the diagnostic protocol itself — service IDs, sub-function structure, DID/routine parameter layouts — and mutates *within* the grammar, so most inputs reach the handler logic instead of dying at the length check. [AutoFuze](../autofuze.md) is the corpus's named instance aimed at the diagnostic surface; [NullSec CarFuzz](../nullsec-carfuzz.md) works the CAN frame layer with structure-aware generation.
- **Replay-mutation:** start from recorded valid exchanges (a real session, a learned ECU profile) and perturb one field at a time — the strategy that inherits validity from the recording. It pairs naturally with the [simulation](simulation-and-test-doubles.md) layer's replay doubles, and shares their limit: the unexplored state space beyond the recording stays unexplored.

## The state problem

A diagnostic target is a state machine, not a parser. Reaching a deep test requires: entering and *holding* an extended or programming session (with TesterPresent keep-alives inside the session timeout), completing SecurityAccess (which costs the fuzzer a working seed/key implementation per target — the [uds-seed-key](uds-seed-key.md) corpus is the fuzzer's prerequisite reading), sequencing enabling services in the order the ECU demands, and recovering state between cases (a crashed or bus-off ECU ends the campaign, so reset detection and re-entry are part of the harness, not an afterthought). [UDSim](../udsim.md)'s loop is the rehearsal pattern: learn the target's state behaviour against a double before spending the real ECU's patience. [TruckDevil](../truckdevil.md) carries the same discipline to J1939's sessionless-but-stateful heavy-vehicle surface.

## Oracles: what counts as a finding

Without a crash oracle a fuzzer is a noise generator. The corpus's working oracles: **liveness** (the ECU stops answering, misses its heartbeat frames, or leaves the bus — detectable by a bus monitor watching the traffic the target *should* emit); **negative-response anomalies** (NRC codes outside the documented set, response timing outliers, a service that answers in a state where the specification says it must refuse — the [state-enforcement gaps](diagnostic-service-abuse.md) this method exists to surface); **state leakage** (a subsequent benign request behaving differently — the stuck-brake lesson: fuzzing writes persistent state, so the harness must diff behaviour, not just watch for silence); and **differential response** between firmware versions. The output of a good campaign is rarely a crash: it is a map of where the implementation's behaviour diverges from the specification's promises.

## The inverted case

The same machinery runs backwards: simulated ECUs fuzzing the *testers*. A diagnostic client (a flasher, a scan tool, a workshop tester) parses ECU responses with the same trust a vehicle parses requests, and malformed-response fuzzing from a double — the declarative and replay rungs of the [simulation](simulation-and-test-doubles.md) page — tests the service toolchain's parsers. The corpus documents the pattern more than the practice; it is recorded here because the boundary matters for scope: this page owns fuzzing *of* the diagnostic surface in both directions, while the surface's abuse modes themselves belong to [diagnostic-service abuse](diagnostic-service-abuse.md).

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source.

## Related

- [Diagnostic-service abuse](diagnostic-service-abuse.md) — the surface this method explores
- [AutoFuze](../autofuze.md) — the corpus's named protocol-aware instance
- [UDSim](../udsim.md) — rehearsal against a learned double before the real ECU
- [Simulation and test doubles](simulation-and-test-doubles.md) — the doubles fuzzing runs against, and inverts
- [CaringCaribou](../caringcaribou.md) and [CANToolz](../cantoolz.md) — the frame-layer fuzzing modules
