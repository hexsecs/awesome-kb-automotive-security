---
title: "Race to Charge: Concurrency Bugs and State Integrity Violations in EV Charging Infrastructure"
summary: "Lee and Lee, USENIX VehicleSec 2026. Audits the open-source EVerest charging stack and finds 11 CVE-assigned flaws, from data races confirmed with…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/vehiclesec26/presentation/lee"
status: published
last_checked: 2026-11-01
created: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: 61ba124
list_summary: "Lee and Lee, USENIX VehicleSec 2026. Audits the open-source EVerest charging stack and finds 11 CVE-assigned flaws, from data races confirmed with sanitizers to logic exploits such as charging that continues after a remote stop."
sources:
  - url: "https://www.usenix.org/conference/vehiclesec26/presentation/lee"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.5281/zenodo.19548057"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - everest
  - ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations
  - ocpp-charging-attacks
  - current-affairs-a-security-measurement-study-of-ccs-ev-charging-deployments
---

Lee and Lee, USENIX VehicleSec 2026. Audits the open-source EVerest charging stack and finds 11 CVE-assigned flaws, from data races confirmed with sanitizers to logic exploits such as charging that continues after a remote stop.

## What it is

Jaeyeong Lee (independent researcher) and Seonhyeong Lee (SK Shieldus). Short paper, *4th USENIX Symposium on Vehicle Security and Privacy* (VehicleSec '26), Baltimore, MD, August 2026, pp. 209–215, with an artifact appendix. The target is **everest-core release 2025.12.1**, the Linux Foundation Energy open-source EV charging stack, deployed in commercial chargers (the paper names the Pionix BelayBox). An EVSE stack is inherently concurrent: the charging state machine runs on its own thread while OCPP callbacks, MQTT handlers, authorisation responses, and vehicle/meter updates each arrive on others. The authors manually audited that threading and callback architecture — four module groups (EVSE Manager, OCPP 1.6, OCPP 2.0.1, Auth Handler), five execution contexts, seven shared state fields mapped by which threads touch them under which locks — then built a Google Test proof of concept for every suspect site, confirming memory races with ThreadSanitizer, AddressSanitizer, and UBSan, and state-integrity flaws by replaying event sequences. The threat model grants no code execution inside the charger: the attacker merely delivers *legitimate* messages at adversarial timing over three channels — a compromised or malicious CSMS sending OCPP commands, a vehicle-side adversary shaping CP/ISO 15118 timing and plug behaviour, and an exposed MQTT/API management plane. The framing result: these bugs are reachable even when the protocol is implemented correctly, and several fire under normal operation with no attacker present.

## What it showed

Eleven vulnerabilities, all now carrying public CVE IDs, clustering into three root-cause patterns:

**Inconsistent locking discipline (8 of 11).** Each everest module manages its own locking, so access paths that cross module boundaries lose it. In the OCPP 2.0.1 module (V4, CVE-2026-26074), the error handler pushes session events under `session_event_mutex` while the firmware- and log-status callbacks push to the same queue with no lock at all — the window is widest during startup, before the stack finishes initialising (TSan). The OCPP 1.6 module repeats the pattern in its powermeter key callback (V5, CVE-2026-26073; ASan/UBSan). The SoC map `evse_soc_map` is read by the powermeter callback, written by the EV-info callback, and reset at session end with no synchronisation in either OCPP version (V6, CVE-2026-26072; V8, CVE-2026-26070) — an `std::optional` invalidated between check and use throws `std::bad_optional_access`. The EVCC ID string is raced the same way (V7, CVE-2026-26071), producing a heap-use-after-free confirmed by ASan. An MQTT `switch_three_phases_while_charging` command writes the Charger's `shared_context` without the state-machine mutex (V9, CVE-2026-33009): TSan reported four races and UBSan caught a `bool` field holding the value 190 — and because phase state selects single- vs three-phase power delivery, corrupted values propagate into power control. Further fields in the same method are raced likewise (V10, CVE-2026-27814). The Auth Handler's Boost.Asio timeout timer can be stopped and fired concurrently from plug-in, authorisation, session-end, and deauthorisation paths, leaving its callback referencing a destroyed `io_context` (V11, CVE-2026-27813; heap-use-after-free).

**Non-atomic state transitions (V1, V2).** Session state is spread across separate flags — `authorized`, `transaction_active`, the current state — never updated as one unit. V1 (CVE-2026-33015): `cancel_transaction()` does not clear `transaction_active` immediately, so a BCB toggle during the StoppingCharging window after a RemoteStop restarts the session and the charger stays energised.

**Missing state validation on asynchronous events (V2, V3).** V2 (CVE-2026-33014): a stop sequence sets `authorized = false`, but a delayed response to an earlier authorisation request arriving afterwards calls `authorize(true)` unconditionally, resurrecting the flag in StoppingCharging state; when the vehicle disconnects, the stop path is skipped and the transaction hangs open — a billing-integrity violation. The authors reproduced V2 on a Raspberry Pi 4 running the *unmodified* everest-core 2025.12.1 with software-in-the-loop EVSE modules: at injected authorisation delays of 30, 50, and 70 ms the stop request was accepted in every run, yet no TransactionEvent(Ended) and no local transaction finish followed. They are explicit about the trigger's reach: the delayed response travels everest-core's internal MQTT/API command plane, so V2 is remotely triggerable when that plane is reachable — **not** a pure CSMS-only exploit. V3 (CVE-2026-29044): a WithdrawAuthorization that lands before TransactionStarted is reflected in the Auth Handler takes the deauthorise-only path instead of stopping the transaction, so a session persists after its authorisation is withdrawn — the operator revokes a stolen RFID credential, the command appears to succeed, and charging continues.

The impact classes are unauthorised charging continuation and billing-integrity violation (V1, V2), authorisation bypass (V3), and denial of service or state corruption through memory unsafety (V4–V11); V6–V8 can manifest during ordinary charging, and an attacker forcing rapid plug/unplug cycles can convert them into deliberate denial of service.

## Where it fits

The implementation layer underneath this cluster's protocol papers. [Current Affairs](current-affairs-a-security-measurement-study-of-ccs-ev-charging-deployments.md) measures what deployed chargers *negotiate*; this paper shows what a deployed charger stack *does under timing pressure* — authorisation finality and RemoteStop irreversibility turn out to be implementation invariants that a race can silently void, not properties the protocols guarantee. Its relation to the [OCPP concept](concepts/ocpp-charging-attacks.md) needs the same care as the other papers' boundaries: everest speaks OCPP on the charger↔backend link and several races are *reached through* OCPP callbacks, but the defects live inside the EVSE process and its threading, not in the protocol or the backend — this is the "harden and fuzz the EVSE implementation" layer the concept page points at. The methodological contrast is with [OCPPStorm](ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations.md) (VehicleSec '24), which fuzzed message content and format; Lee and Lee position their manual timing audit as the complement — every one of these bugs survives a perfectly correct protocol implementation, which input fuzzing does not see. EVerest previously had a single input-validation memory bug in this space (the V2GTP overflow, CVE-2024-37310); this paper is its concurrency companion. A pattern-level inspection of other open-source stacks (OpenEVSE WiFi, Java-OCA-OCPP, WWCP_OCPP, SteVe) found the same precondition — multiple asynchronous control paths converging on shared session state — but the paper is explicit that those stacks were not audited and no equivalent vulnerabilities are claimed for them.

## Limits and safety notes

As the paper states them: **one framework, one release** — commercial EVSE implementations were not examined and may have different concurrency patterns. The hardware validation covers V2 only, on a Raspberry Pi with software-in-the-loop EVSE modules, **not** production charger hardware with real contactors, PLC modems, and grid-side power electronics. The methodology is manual code review, so additional concurrency bugs may well exist beyond the eleven. V2's remote trigger requires reachability of the everest-core MQTT/API management plane; it is not exploitable from the CSMS channel alone. The cross-stack observations are architectural pattern-matching, not findings.

## Status and sources

Status: **published** — a finished 2026 conference publication (short paper). Bibliographic record: *Proceedings of the 4th USENIX Symposium on Vehicle Security and Privacy*, pp. 209–215, artifact appendix pp. 216–217 (ISBN 978-1-939133-56-4). **DOI: none** — USENIX does not assign DOIs to its proceedings papers, and a Crossref bibliographic title query (2026-11-01) returned no record for this paper. (The Zenodo DOI 10.5281/zenodo.19548057 belongs to the paper's artifact — source snapshot, scanner, and Raspberry Pi replay harness — not to the paper.) The eleven CVE IDs are CVE-2026-33015, CVE-2026-33014, CVE-2026-29044, CVE-2026-26074, CVE-2026-26073, CVE-2026-26072, CVE-2026-26071, CVE-2026-26070, CVE-2026-33009, CVE-2026-27814, and CVE-2026-27813; per the CVE records, affected everest-core versions are those before 2026.02.0, which contains the fixes. Full text read end-to-end, artifact appendix included, from the USENIX proceedings PDF, 2026-11-01.

## Related

- [EVerest(everest.md) — the audited stack's entity page
- [OCPPStorm(ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations.md) — the content-fuzzing complement: message format vs execution timing
- [OCPP and charging attacks](concepts/ocpp-charging-attacks.md) — the charger↔backend link several of these races are triggered across
- [Current Affairs](current-affairs-a-security-measurement-study-of-ccs-ev-charging-deployments.md) — the deployment-side companion: what chargers negotiate vs what their stacks withstand
