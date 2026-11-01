---
title: "Lock It and Still Lose It: On the (In)Security of Automotive Remote Keyless Entry Systems"
summary: "Garcia, Oswald, Kasper, and Pavlides, USENIX Security 2016. Recovers shared global keys covering most Volkswagen Group vehicles sold over two decades, and…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/garcia"
status: unknown
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Garcia, Oswald, Kasper, and Pavlides, USENIX Security 2016. Recovers shared global keys covering most Volkswagen Group vehicles sold over two decades, and breaks the Hitag2 rolling-code scheme."
sources:
  - url: "https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_garcia.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - gone-in-360-seconds-hijacking-with-hitag2
  - dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer
---

Garcia, Oswald, Kasper, and Pavlides, USENIX Security 2016. Recovers shared global keys covering most Volkswagen Group vehicles sold over two decades, and breaks the Hitag2 rolling-code scheme.

## What it is

A large-scale security analysis of automotive remote keyless entry (RKE) systems — the rolling-code schemes that lock and unlock a car from the fob — by Flavio D. Garcia and Pierre Pavlidès (University of Birmingham, the Hitag2 case study), David Oswald (Birmingham), and Timo Kasper (Kasper & Oswald GmbH, the VW Group case study). *25th USENIX Security Symposium*, Austin, TX, August 2016, pp. 929–944. Where the immobilizer breaks of the preceding years (DST40, Hitag2, Megamos) attacked the system that *starts* the car, this paper attacks the system that *opens* it. The authors' stated motivation includes the then-unexplained burglaries of locked vehicles reported in the press. The team's eavesdropping setup is an Arduino-based RF transceiver costing about $40; SDRs do the same job.

## What it showed

**Case study 1 — VW Group: sound ciphers, one global key each.** The authors identified at least seven VW Group RKE schemes (VW-1 to VW-7) and analysed the four covering the most vehicles. Rather than attacking the remotes (mask-ROM microcontrollers), they extracted firmware from the receiving ECUs and recovered the cryptographic algorithms by static analysis.

- **VW-1** (until ~2005): no cryptography at all — the "rolling code" is an obfuscated LFSR state used as a counter. From a single eavesdropped signal (UID and current LFSR state) an adversary can generate valid codes at will.
- **VW-2** (~2004 on) and **VW-3** (~2006 on): a proprietary 8-byte block cipher the authors identify as AUT64 (12 rounds; ~91.6-bit effective key — beyond brute force, and not cryptanalysed). It did not matter: **both schemes use a single fixed, worldwide master key**, different per scheme, with no key diversification whatsoever.
- **VW-4** (~2009–2016): the cipher improves to XTEA (128-bit key; the best known attack is a theoretical related-key result the paper dismisses as irrelevant here) — and the key management does not: again **one single worldwide key** for every vehicle on the scheme. The authors verified this end to end on an Audi Q3, model year 2016, decrypting its codes and generating new valid ones to open and close the car.

The attack is therefore identical across VW-1–VW-4: eavesdrop **one** rolling code from the target remote (eavesdropping discussed at up to 100 m), decrypt it with the global key to learn the UID and current counter, and clone the remote — lock or unlock the target vehicle an arbitrary number of times. Scope as stated: "most VW Group vehicles manufactured between 1995 and today" — VW Group sold almost 100 million cars in 2002–2015 and the authors have "strong indications that the vast majority is vulnerable". A long model list is given (the practically tested subset is marked), US-market 315 MHz remotes were tested and found equally vulnerable, and at least one platform twin outside the group (Ford Galaxy) carries the same flawed system. A side observation: most VW-4 cars **block** the genuine remote if they receive a valid code whose counter is more than 2 behind — so two attacker-sent codes desynchronise and then block the owner's remote (a possible indicator that an attack occurred).

**Case study 2 — the Hitag2 rolling-code scheme: per-remote keys, a broken cipher.** The second scheme runs on NXP's PCF7946/PCF7947 remote-control ICs, following what appears to be NXP's reference design. The authors reverse-engineered the protocol black-box, from a remote whose key they legitimately knew — no firmware extraction. A button press sends the 32-bit UID in the clear, a 4-bit button identifier, the 10 least significant bits of a 28-bit counter, 32 bits of Hitag2 keystream, and an 8-bit XOR checksum. In contrast to VW, manufacturers here did **not** use a global key — each remote has its own 48-bit key — so the failure has to come from the cipher itself. The best prior practical attack on Hitag2 (the 2012 immobilizer attack) needs 136 authentication traces — impractical against RKE, where no victim presses a button 136 times. The paper's new **correlation attack** recovers the key from a **minimum of four eavesdropped rolling codes** (non-consecutive is better; consecutive codes usually need eight), at about **one minute of computation on a laptop** per guess of the counter's 18 unsent most-significant bits — and since those bits change only every 1,024 button presses, tested cars had values between 0 and 10, putting the total attack **under 10 minutes**. The authors built a key emulator and unlocked and locked 15 vehicles with freshly generated codes (model years 2004–2016, across twelve makes); a considerably longer list of models shipping the same scheme is taken from an aftermarket universal-remote guide and is presented as presumed, not tested. Harvesting the four codes can be accelerated by selectively jamming only the predictable final checksum byte, so the car ignores the code while the attacker records it and the owner presses again — a possible in-progress attack indicator.

## Where it fits

The RKE counterpart to the immobilizer breaks: DST40, Hitag2, and Megamos had shown the *starting* system could be cloned; this paper shows the *entry* system falls the same way, by two different failure modes — key management failure (one global key behind sound ciphers, VW) and cipher failure (sound key diversification behind a weak cipher, Hitag2). Its Hitag2 half is the direct continuation of [Gone in 360 Seconds](gone-in-360-seconds-hijacking-with-hitag2.md): the same cipher and overlapping authors, but a new attack shaped for the RKE setting, where traces are scarce. This is a **cloning** break — the attacker recovers key material and mints codes alone — not a relay attack: nothing here forwards a genuine key's exchange, and the paper discusses relay attacks on PKES only as background.

## Limits and safety notes

As the paper states them: the three remaining VW schemes (VW-5, VW-6, VW-7) and the group's luxury brands (Porsche, Bentley, Lamborghini, Bugatti) were not analysed; per a VW Group statement reported in the paper, the latest generation (e.g. the Golf 7 platform) uses individual keys — that is the manufacturer's claim, not something the authors verified. The affected-model list is explicitly non-exhaustive, and it is "not clear if and when a car model has been upgraded to a newer scheme". Deliberate withholdings under the disclosure agreements: the recovered key values, part numbers, and full VW-1 details are not in the paper. The authors analysed further RKE systems "with similar results" but could not publish them then (responsible-disclosure difficulty). RKE compromise by itself opens doors and disables the alarm; starting the car still requires defeating the immobilizer or programming a key via OBD — entry is the stealthy first stage, not the whole theft. Owner countermeasure, in the paper's summary: verifying the car locked is no longer sufficient, and the only reliable option is to stop using RKE and use the mechanical lock — "Lock It or Lose It? Remove It!" Disclosure: VW Group contacted November 2015, vulnerabilities acknowledged; NXP notified January 2016.

## Status and sources

Status: **unknown** — a finished 2016 publication; no living artefact. Bibliographic record: 25th USENIX Security Symposium (USENIX Security '16), Austin, TX, August 2016, proceedings pp. 929–944. **DOI: none** — no Crossref record exists (checked 2026-11-01); USENIX assigned no DOIs to its 2016 proceedings. Full text from USENIX; read in full 2026-11-01.

## Related

- [Gone in 360 Seconds: Hijacking with Hitag2](gone-in-360-seconds-hijacking-with-hitag2.md)
- [Dismantling Megamos Crypto: Wirelessly Lockpicking a Vehicle Immobilizer](dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md)
