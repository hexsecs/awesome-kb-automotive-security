---
uid: 01a1d439-cc57-767e-8abb-6d2724494f8f
title: "How I Discovered and Hacked Learning Codes of the Key Fob of a Car Assembled in My Country"
summary: "Erazo, DEF CON 32 Car Hacking Village 2024. Breaks the learning-code key fob of a locally assembled car with replay, a receiver backdoor, and a brute-force…"
type: entity
category: "Conference Presentations"
url: "https://media.defcon.org/DEF%20CON%2032/DEF%20CON%2032%20villages/DEF%20CON%2032%20villages%20captions/DEF%20CON%2032%20-%20Car%20Hacking%20Village%20-%20How%20I%20discovered%20and%20hacked%20Learning%20Codes%20of%20the%20key%20job%20of%20a%20car%20assembled%20in%20my%20country%20-%20Danilo%20Erazo.eng.srt"
status: published
last_checked: 2026-11-17
created: 2026-11-13
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 6a8b17c
list_summary: "Erazo, DEF CON 32 Car Hacking Village 2024. Breaks the learning-code key fob of a locally assembled car with replay, a receiver backdoor, and a brute-force tool."
related:
  - car-hacking-village
  - lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems
  - my-other-car-is-your-car-compromising-the-tesla-model-x-keyless-entry-system
  - rollback-a-new-time-agnostic-replay-attack-against-the-automotive-remote-keyless-entry-systems
  - rolling-code-failure-classes
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-13
  - url: "https://media.defcon.org/DEF%20CON%2032/DEF%20CON%2032%20villages/DEF%20CON%2032%20villages%20captions/DEF%20CON%2032%20-%20Car%20Hacking%20Village%20-%20How%20I%20discovered%20and%20hacked%20Learning%20Codes%20of%20the%20key%20job%20of%20a%20car%20assembled%20in%20my%20country%20-%20Danilo%20Erazo.eng.srt"
    retrieved: 2026-11-17
---

Erazo, DEF CON 32 Car Hacking Village 2024. Breaks the learning-code key fob of a locally assembled car with replay, a receiver backdoor, and a brute-force tool.

## What it is

A talk by Danilo Erazo, a self-taught hardware-security researcher and penetration tester from Ecuador, at DEF CON 32's Car Hacking Village in 2024. The subject is the *learning-code* remote keyless entry (RKE) fob of a car assembled locally in his country. The talk moves from discovering that the fob is effectively fixed-code, through reversing the frame format and building a brute-force tool, to implanting a permanent backdoor in the receiver and demonstrating the systemic code-collision problem that learning codes create.

## How it works

The signal is on **370 MHz** with **ASK** modulation, captured at **500 symbols per second**. A simple replay confirmed that the car responded to a recorded unlock command — evidence that the link was not using rolling codes. Disassembling the fob revealed an **HS2240 learning-code chip**. Unlike a fixed-code fob, whose code is soldered onto the board, a learning-code fob holds its code in the IC and the receiver microcontroller "learns" it: during programming, the receiver saves the transmitted code to memory and will store **up to four** different codes. Each fob has a distinct code.

Reversing the encoding with a logic analyser gave the frame layout: a **20-bit code** (so 2^20, about one million possible codes) plus a **4-bit mode** field, with the code and mode repeated four times to make a **96-bit frame**; the whole frame repeats around 25 times per button press. With only a million codes and a known format, brute force is practical. Erazo's tool transmits candidate codes at a configurable inter-signal delay (default about **30 ms**); in the demo, unlocking a Kia Rio took roughly **one minute**. The same attack worked against a Kia Picanto and a Renault model, and he notes other vulnerable cars in Ecuador.

The receiver can also be subverted. Wiring the **STM8** receiver's programming input to the ignition voltage and pressing a button **six times** puts it into learning mode, letting an attacker enrol an arbitrary code of their choosing; the car then unlocks on that code indefinitely. Because up to four codes can be stored, a backdoor can coexist with the owner's legitimate fobs. The talk also covers a rolljam-style attack against genuine rolling codes using **two SDRs** (record one code while blocking it, then replay later), and a **code-collision** failure mode: with a global pool of only a million codes, a random fob will eventually open someone else's car, and nobody will know why.

The tool, **AutoRFKiller**, is about **1,300 lines of Python**. Its features include brute force against a code database, checking whether a car has already been backdoored (if an unexpected code opens it, it has), brute force with arbitrary parameters (including a 22-bit space), generating custom backdoor signals, and replay.

## Where it fits

This is the low-cost, learning-code counterpart to the more sophisticated RKE work in the corpus. [Lock it and still lose it](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md) and [My other car is your car: compromising the Tesla Model X keyless entry system](my-other-car-is-your-car-compromising-the-tesla-model-x-keyless-entry-system.md) cover stronger OEM implementations, and [Rollback: a new time-agnostic replay attack](rollback-a-new-time-agnostic-replay-attack-against-the-automotive-remote-keyless-entry-systems.md) is the modern replay variant. The session sits within [Car Hacking Village](car-hacking-village.md).

## Limits and safety notes

The primary source is an **auto-generated caption transcript**, so several proper nouns are garbled ("key job" for key fob, "K4" for the fob, "Akia Soluto" for an unnamed Kia model); the frequencies, bit widths, timings and chip part number are quoted as spoken and were not independently verified. The talk demonstrates proximity-based RF attacks and a backdoor that requires physical access to the receiver's ignition/programming wiring — this is not a remote internet compromise. The tool is described in the talk but no repository or capture is linked from the source entry, so the claims are the speaker's. Unlocking vehicles without authorisation is unlawful; the relevance here is to understanding why fixed and learning codes are unsafe by design. No RF hardware or vehicle was exercised for this page.

## Status and sources

Checked 2026-11-17. **Published** — DEF CON 32 Car Hacking Village, 2024; official caption transcript hosted by DEF CON.

- [DEF CON 32 caption transcript](https://media.defcon.org/DEF%20CON%2032/DEF%20CON%2032%20villages/DEF%20CON%2032%20villages%20captions/DEF%20CON%2032%20-%20Car%20Hacking%20Village%20-%20How%20I%20discovered%20and%20hacked%20Learning%20Codes%20of%20the%20key%20job%20of%20a%20car%20assembled%20in%20my%20country%20-%20Danilo%20Erazo.eng.srt)

## Related

- [Car Hacking Village](car-hacking-village.md)
- [Lock it and still lose it: on the (in)security of automotive remote keyless entry systems](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md)
- [My other car is your car: compromising the Tesla Model X keyless entry system](my-other-car-is-your-car-compromising-the-tesla-model-x-keyless-entry-system.md)
- [Rollback: a new time-agnostic replay attack against the automotive remote keyless entry systems](rollback-a-new-time-agnostic-replay-attack-against-the-automotive-remote-keyless-entry-systems.md)
- [Rolling-code failure classes](concepts/rolling-code-failure-classes.md)
