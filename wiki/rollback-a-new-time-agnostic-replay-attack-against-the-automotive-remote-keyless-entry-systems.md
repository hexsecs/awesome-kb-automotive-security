---
uid: 01a19d3c-afce-7761-b78f-15ccafd87f03
title: "RollBack: A New Time-Agnostic Replay Attack Against the Automotive Remote Keyless Entry Systems"
summary: "Csikor et al., Black Hat USA 2022. Replaying already-invalid rolling codes in sequence triggers a resynchronisation rollback, unlocking a vehicle…"
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/2210.11923"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Csikor et al., Black Hat USA 2022. Replaying already-invalid rolling codes in sequence triggers a resynchronisation rollback, unlocking a vehicle indefinitely and defeating the countermeasure that stopped RollJam."
sources:
  - url: "https://arxiv.org/abs/2210.11923"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1145/3627827"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it
  - lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems
  - gone-in-360-seconds-hijacking-with-hitag2
  - key-fob-relay-attacks
  - rolling-code-failure-classes
---

Csikor et al., Black Hat USA 2022. Replaying already-invalid rolling codes in sequence triggers a resynchronisation rollback, unlocking a vehicle indefinitely and defeating the countermeasure that stopped RollJam.

## What it is

Levente Csikor, Hoon Wei Lim, Jun Wen Wong, Soundarya Ramesh, Rohini Poolat Parameswarath, and Mun Choon Chan — Institute for Infocomm Research (A*STAR), NCS Group, and National University of Singapore. Black Hat USA 2022; extended text arXiv:2210.11923 (September 2022); journal version *ACM Transactions on Cyber-Physical Systems* 8(1), 2024. RollBack is a replay-and-resynchronize attack on rolling-code remote keyless entry (RKE) — the button-press lock/unlock system, not PKES. The background machinery, as the paper states it (from Microchip's public KeeLoq documentation): fob and receiver each keep a counter (16-bit in the classic design); a code is valid only in step. To tolerate out-of-range presses, the receiver accepts desynchronization through two windows — a **single window** (difference < ~16: immediate resync on the first press, skipped codes invalidated) and a **resync/double window** (~16 to 2^15: the receiver stores the counter and resyncs only if the *next* signal is exactly one higher, acting on that second signal); beyond that lies a blocked window and the signal is discarded. RollJam (Kamkar, 2015) had already weaponized the single window by jamming and banking an unused future code — but the banked code dies the moment the owner next uses the fob unjammed. RollBack attacks the resynchronization machinery itself.

## What it showed

**The phenomenon.** Replaying a few previously captured, already-invalid signals (invalid because the owner has used the fob since) consecutively triggers a rollback-like mechanism: the receiver resynchronizes *backwards* to the counter state of the replayed sequence, the instruction in the last replayed signal is executed, and every later captured signal becomes valid again. The genuine fob keeps working normally; the owner notices nothing. Against RollJam the properties invert: **no jamming is required** (jamming only speeds up capture); capture happens **once**; the captured signals can be replayed **at any future time, as many times as desired** — the authors validated the time-agnostic property with signals stored for ~100 days. And RollBack is **instruction-agnostic**: the replayed sequence may mix lock and unlock signals freely, because only the final signal's instruction is executed — capture rides on the owner's ordinary lock presses (the near-universal double-press habits: confirming a lock, two-stage passenger unlock), and a captured later lock signal replayed after the unlocks re-locks the car, covering the attacker's tracks.

**Four variants.** Receivers differ in three parameters — how many signals (#SIGNALS), whether they must be strictly consecutive (SEQUENCE), and within what replay pace (TIMEFRAME). *RollBack^Loose_N(2)*: two signals, loose sequence (need not be strictly consecutive; the fob may be used between captures), no time limit. *RollBack^Strict_N(2)*: two strictly consecutive signals replayed within an N-second timeframe (5 s and 8 s instances appear below). *RollBack^Strict_N(3)* / *RollBack^Strict_N(5)*: three / five strictly consecutive signals.

**The evaluation.** Around 20 vehicles (Asian makes available in Singapore; owners' consent, isolated environment); about **70% were vulnerable** to some variant. Vulnerable, per the paper's Table 2: Honda Fit (hybrid 2016; 2018), City (2017), Vezel (2017) — NXP (F2951X, 61X0915), five-signal strict; Hyundai Elantra (2015, Omron MD-015) and Kia Cerato/Forte K3 (2017 and 2015, Omron MD-011) — the loose two-signal variant, the weakest requirement found; Mazda 3 (2018), 2 Sedan (2018), 2 Hatchback (2020), CX-3 (2019), CX-5 (2018) — NXP (A2V25, F7953), three-signal strict; Nissan Latio (2009, Microchip) — two-signal strict within 5 s; Nissan Sylphy (NXP F7952) — two-signal strict within 8 s. **Not vulnerable:** Hyundai Elantra (2012, NXP 32182C15), Hyundai Avante (2020, NXP F793616), Nissan Teana (2014, NXP), and every Toyota tested (Wish, Corolla Axio (TI 37143ADN), Altis (TI 37200A), Prius (2020, TI)) — TI-based systems uniformly immune in this sample. The paper's own cautions: the vulnerable component is the *receiver* in the car, not the fob (which only sends) — transponder vendor correlates with vulnerability, but receivers come from different OEMs, and an NXP transponder alone decides nothing, as the immune NXP systems show. Hardware needs are RollJam-class or less (a dedicated device at tens of dollars).

**Root cause: unproven, with a named suspect.** Documented design says replayed counters below the receiver's should be discarded, so the authors hunt for a legitimate receiver behaviour that accepts old consecutive counters. Their candidate is the **key-fob learning process** — the procedure that pairs a new fob — documented publicly only for Microchip's KeeLoq (HCS200/HCS300): the receiver derives the fob's key from its serial number, authenticates the first signal, *buffers* its counter without checking it against the vehicle's counter, and on a second signal with counter exactly one higher stores serial number, counter, and key as learned. Nothing in it checks whether the fob is already known. The paper lists five mismatches against its own hypothesis — learning requires an explicit learn mode that RollBack never triggers (vulnerable cars would have to sit in a "forever learn mode"); the timeframe property appears in no documentation; loose and five-signal variants do not match a two-press learning sequence; learning does not obviously execute the last signal's instruction, yet RollBack always does; and re-learning an already-known fob is undefined in the documentation. In disclosure, NXP's PSIRT (March 2022) confirmed the behaviour is a receiver-side vulnerability, not a feature; Omron did not respond; Auto-ISAC members acknowledged the findings and cleared the Black Hat presentation.

## Where it fits

The [Stealing Cars SoK](sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it.md) summarises RollBack in one sentence — replaying two consecutive recorded signals rolls the receiver back through its resynchronization procedure (Kia and Mazda confirmed) — and the primary paper both confirms and corrects the compression: two signals is only the loosest variant (Omron-based Kia/Hyundai, and strict two-signal Nissan), while Honda needs five strictly consecutive signals and Mazda three, and the confirmed set is wider (Honda, Hyundai, Kia, Mazda, Nissan). Within the KB's RKE line, RollBack completes the counter-machinery family beside [Lock It and Still Lose It](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md): Garcia et al. abused the acceptance window and global keys from the key-recovery side, RollJam banked a *future* code, Rolling-PWN (Honda 2012–2022; its exact sequence was never publicly specified) found a similar Honda resync behaviour independently, and RollBack resurrects *past* codes through the resync path itself. No cryptography is broken anywhere in it: encryption is why an attacker cannot flip a captured lock into an unlock — and irrelevant to an attack that replays genuine signals to a receiver that accepts them. The mitigations the paper discusses mark the class boundary: timestamps in the signal (as in Ultimate KeeLoq, adoption unconfirmed) defeat replay generally; separate rolling codes per instruction would break the instruction-agnostic capture; owner vigilance detects only the jamming-assisted variant — against purely passive capture there is, the paper states, no way for the owner to notice.

## Limits and safety notes

As the paper bounds them: **the sample is small and regional** — ~20 vehicles, Asian manufacturers, Singapore availability, analysis explicitly ongoing; "~70% vulnerable" is a property of that sample, not a fleet estimate, and the authors maintain a crowd-sourced results database to widen it. **Unlocking is not stealing**: RollBack alone opens doors; the immobilizer still guards engine start (which is why the car-sharing scenario, fob inside the car, is the paper's worst case). **The root cause is a hypothesis**, receiver-side by NXP's confirmation and by correlation, but the learning-process explanation carries the authors' own five objections and no receiver teardown settles it. **This page follows the arXiv text**; the 2024 journal version was not the copy read. Experiments ran in an isolated environment on consenting owners' cars, captured signals were deleted after testing, and the authors state replaying signals causes no harm to vehicle or fob.

## Status and sources

Status: **published** — Black Hat USA 2022; extended version arXiv:2210.11923; journal version *ACM Transactions on Cyber-Physical Systems* 8(1), pp. 1–25, 2024. DOI [10.1145/3627827](https://doi.org/10.1145/3627827), verified against Crossref (record's title, all six authors, venue, volume/issue, and page range match the journal version), 2026-11-01. Full text read end-to-end from the open arXiv version, 2026-11-01.

## Related

- [SoK: Stealing Cars Since Remote Keyless Entry Introduction](sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it.md) — the secondary account this page is the primary source for
- [Lock It and Still Lose It](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md) — window abuse and cloning, from the key-recovery side
- [Gone in 360 Seconds: Hijacking with Hitag2](gone-in-360-seconds-hijacking-with-hitag2.md) — correlation attack on the other major rolling-code scheme
- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md) — the concept page; RollBack is counter-state abuse, neither relay nor cloning
