---
title: "Shared, default, and global secrets: the break-once pattern"
summary: "The decisive failure is rarely cipher strength — it is one secret shared by a fleet or a type, or a default nobody changed. Break one, break all."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems, beneath-the-bonnet-a-breakdown-of-diagnostic-security, experimental-security-analysis-of-a-modern-automobile, gone-in-360-seconds-hijacking-with-hitag2, dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer, uds-seed-key, secure-firmware-updates]
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity16/presentation/garcia"
    retrieved: 2026-11-01
  - url: "https://www.usenix.org/legacy/events/sec10/tech/full_papers/Koscher.pdf"
    retrieved: 2026-11-01
---

Read the corpus's breaks in sequence and a pattern emerges that no single page is about: the cipher usually survives, and the **secret management** fails. Again and again, a sound primitive is deployed behind a key that is shared by an entire fleet, identical across every unit of a type, left at its factory default, or derived from a constant — so the cost of the break is paid *once*, on one unit, on a bench, and the yield is every vehicle that shares the secret. This page collects the four shapes the pattern takes, because the countermeasure is the same in all of them and the corpus's authors keep having to restate it.

## Shape 1: the global master key

[Lock It and Still Lose It](../lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md) is the landmark: Volkswagen Group's RKE schemes used respectable ciphers (AUT64, XTEA) for their rolling codes — behind a **single worldwide master key per scheme, with no per-vehicle diversification**, the key extractable from one ECU's firmware. One extraction, roughly 100 million vehicles (2002–2015) cloneable. The cipher's strength was never consulted; the key's *scope* was the vulnerability.

## Shape 2: the per-type shared secret

[Beneath the Bonnet](../beneath-the-bonnet-a-breakdown-of-diagnostic-security.md)'s diagnostic ciphers are per-*manufacturer*, and within a type the same secret serves every ECU — so extracting a seed/key algorithm from one unit's firmware (the paper's standard method) retires the gate for the type. Its compounding detail: only the level-1 secret is ever needed, because extracted firmware holds the higher levels' secrets too — the multi-level scheme shares fate downward. The [uds-seed-key](uds-seed-key.md) page owns the diagnostic instance in detail; the shape is recorded here because it is the same economics: break-one-break-all, scoped to a type instead of a fleet.

## Shape 3: the unchanged default

[Hitag2](../gone-in-360-seconds-hijacking-with-hitag2.md) deployments shipped with the transponder password at its default and keys predictable — in at least half the cars the researchers tested, the "secret" was the datasheet value. [Megamos](../dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md) transponders sat unlocked or behind a publicly known default PIN. Foster et al.'s fleet case (on its survey-cluster page) is the infrastructure twin: a **shared root SSH key across the fleet**, plus unsigned updates to spend it through. A default is a global secret that was never even generated — its scope is every unit that left the line unconfigured, and no extraction is required because the value is published.

## Shape 4: the constant or predictable challenge

The seed side of the same failure: Miller & Valasek 2013's PAM returned the **constant seed 11 22 33** (leftover debug code overwriting the randomised challenge), making SecurityAccess a formality; Koscher's telematics unit hardcoded a challenge/response pair **common to all units of the part number**. A constant challenge converts a challenge-response protocol into a password — a shared, static, extractable one — while preserving the protocol's outward shape, which is why these survive design review: the diagram still shows a seed flowing.

## The fleet arithmetic, and the counter-designs

The shared property is economic: the defender pays the secret's protection cost per design; the attacker pays the extraction cost *once per scope* and amortises it over every unit in that scope. This is why these failures outrank cipher breaks in the corpus's real-world consequences — the Megamos and VW cases reached litigation and injunctions precisely because the scope was the fleet. The counter-designs the corpus itself proposes are uniformly about **scope reduction**: per-vehicle and per-ECU key diversification (a unique key derived or provisioned per unit, so extraction retires one vehicle), per-device credentials in the V2X systems (the [credential management](v2x-credential-management.md) page's whole architecture is diversification as a premise), and [Uptane](secure-firmware-updates.md)'s per-vehicle metadata binding — the update framework binding instructions to one vehicle's manifest so a compromised artefact does not generalise. Where a shared secret is genuinely unavoidable (a bootstrap password, a group key), the corpus's lesson is to treat its extraction as a fleet event in the threat model — because that is what it will be in the incident report.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source.

## Related

- [Lock It and Still Lose It](../lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md) — the global master key, ~100M vehicles
- [Beneath the Bonnet](../beneath-the-bonnet-a-breakdown-of-diagnostic-security.md) — per-type secrets and the level collapse
- [Gone in 360 Seconds (Hitag2)](../gone-in-360-seconds-hijacking-with-hitag2.md) and [Dismantling Megamos Crypto](../dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md) — the default-credential shape
- [UDS seed/key](uds-seed-key.md) — the diagnostic instance, in detail
- [Secure firmware updates](secure-firmware-updates.md) — the counter-design: per-vehicle binding
