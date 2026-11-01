---
title: "Dismantling Megamos Crypto: Wirelessly Lockpicking a Vehicle Immobilizer"
summary: "Verdult, Garcia, and Ege, USENIX Security 2015. Reverse engineers the Megamos immobilizer used by Audi, Fiat, Honda, Volkswagen, and Volvo; famously…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/verdult"
status: unknown
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Verdult, Garcia, and Ege, USENIX Security 2015. Reverse engineers the Megamos immobilizer used by Audi, Fiat, Honda, Volkswagen, and Volvo; famously injuncted for two years before publication."
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/verdult"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - gone-in-360-seconds-hijacking-with-hitag2
  - key-fob-relay-attacks
  - lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems
---

Verdult, Garcia, and Ege, USENIX Security 2015. Reverse engineers the Megamos immobilizer used by Audi, Fiat, Honda, Volkswagen, and Volvo; famously injuncted for two years before publication.

## What it is

Roel Verdult and Baris Ege (Radboud University Nijmegen) and Flavio D. Garcia (University of Birmingham). Presented at USENIX Security '15 and published in the *Supplement to the Proceedings of the 22nd USENIX Security Symposium*, pp. 703–718 — the bibliographic oddity is part of its publication history (see Status and sources). The paper reverse engineers the Megamos Crypto transponder, the first cryptographic immobilizer transponder manufactured by EM Microelectronic and, at the time of the research (fall 2012), one of the most widely deployed: the manufacturer claimed more than 100 million immobilizer chips sold including Megamos Crypto, and the paper lists vehicles that used it — among others most Audi, Fiat, Honda, Volkswagen, and Volvo cars, plus Alfa Romeo, Ferrari, Maserati, Porsche, Seat, and Skoda. The transponder is a passive 125 kHz RFID chip authenticating with a proprietary cipher and a 96-bit key; a 32-bit PIN guards write access on the newer chip. Within the industry, the paper notes, Megamos Crypto was believed to be unclonable. The authors extracted the cipher and protocol from the Tango Programmer locksmith tool's software using IDA Pro — defeating an executable obfuscator built on a custom virtual machine — and publish both in full. Experiments used a Proxmark III with custom firmware; the work was partly motivated by local police reports of cars stolen in ways nobody could explain.

## What it showed

**The cipher and protocol.** The cipher's internal state is built from a 23-bit Galois LFSR, a 13-bit non-linear FSR, and three 7-bit output registers — an effective state of only **56 bits against a 96-bit key**. In authentication, the car sends a 56-bit nonce and its 28-bit authenticator; the transponder answers with 20 bits, contributing no randomness of its own. One component is absent from the published paper by design: the definition of the non-linear output filter function is, in the paper's own words, "deliberately omitted in this paper".

**Weaknesses behind the first attack:** the state (56 bits) is much smaller than the key (96 bits); the successor function can be inverted — given a state and its ciphertext bit, the predecessor state is computable; initialization can likewise be undone, recovering later key bits from any initial state; the non-linear FSR starts from only 12 bits; the protocol's last steps yield 15 bits of known plaintext; and with no transponder-side randomness, replay is open.

**Attack 1 — cryptanalysis (all Megamos vehicles).** Two eavesdropped traces suffice. The rollback search over the 56-bit state costs 2^56 operations (under two days on a COPACOBANA-class FPGA machine); a state-splitting trade-off reduces it to 2^49 lookups at the price of a 12 TB table — which the paper itself calls difficult to mount on ordinary hardware.

**Attack 2 — partial key update (unlocked or default-PIN transponders).** Many transponders in the field have their memory unlocked, or locked with a publicly known default PIN, so anyone has write access — including to the key. The 96-bit key is stored as six 16-bit blocks written one block at a time: the update is not atomic. The attacker eavesdrops one genuine authentication trace, then overwrites one key block with a guess and replays the car's challenge; the transponder's acceptance identifies the correct block value. Choosing trace nonces carefully reduces this to **three writes and 3 × 2^16 authentication attempts — about 30 minutes end to end** with a Proxmark III. The authors executed this attack on several real cars, recovered the keys, emulated the transponders, and started the vehicles. The paper also proposes the owner-level fix — set the memory lock bit and a random PIN — and provides an open-source Proxmark III RFID library to do it.

**Attack 3 — weak keys.** Many keys recovered via attack 2 were weak: the first 32 bits all zero (the industry apparently uses only 64 of the 96 key bits, probably for compatibility with legacy systems), some keys with as few as ten 1-bits in total, and a manufacturer-dependent pattern further reducing entropy. For such keys, a rainbow-table trade-off over the 56-bit state (1.5 TB of storage) recovers the key from **two authentication traces with a few minutes of lookup on a standard laptop** — and unlike attack 2, this works even when the transponder is locked with a PIN.

**Practical exposure.** The authors' setup reads a transponder's identifier in under 14 ms; standing next to a victim for a fraction of a second suffices to pickpocket the identifier and user memory. The paper also records a design-level own goal: because long runs of 1-bits desynchronize the field modulation, the manufacturer's application note advises random numbers with more zeros than ones — deliberately dropping nonce entropy.

## Where it fits

The fourth and last of the widely deployed proprietary immobilizer ciphers to fall, after DST40 (2005), KeeLoq, and the same group's [Hitag2 break](gone-in-360-seconds-hijacking-with-hitag2.md) (2012) — of the four major immobilizer products, Megamos was the one with no known attack when the research began. In this KB it sits on the *cloning* side of the [key-fob relay attacks](concepts/key-fob-relay-attacks.md) distinction, which cites it in exactly those terms: the cipher was broken outright, so an emulated transponder authenticates with no genuine key nearby.

## Limits and safety notes

As the paper states them: the cryptanalytic attack needs two traces and either FPGA-class hardware or a 12 TB table the authors call hard to mount on ordinary hardware; attack 2 requires write access (unlocked memory or the default PIN) plus ~30 minutes of close-range interaction; attack 3 applies only to transponders with the observed weak-key patterns. All three need close-range access to the transponder, and starting a car additionally requires interacting with the vehicle — the paper names valet parking and car rental as the realistic exposure scenarios. Makes and models in the weak-key table are deliberately anonymized. Responsible disclosure per the paper: the authors notified the manufacturer in November 2012 and kept an open communication channel. The paper's conclusion stresses the keyless-ignition case: the mechanical key was removed from such vehicles but the cryptographic mechanisms were not strengthened to compensate.

## Status and sources

Status: **unknown** — a finished publication; no living artefact beyond the authors' open-source Proxmark III RFID library. No DOI (USENIX practice for the era). Full text openly available; read in full 2026-11-01.

**Publication and injunction history — sourced, not from the paper text.** The paper itself says only that the manufacturer was notified in November 2012, and that the output filter function is deliberately omitted. The list's summary records the paper was "famously injuncted for two years before publication". The documented record behind that line, from contemporary reporting (notably the Communications of the ACM account of *Volkswagen Aktiengesellschaft v Garcia et al.*): the paper was to be presented at USENIX Security in August 2013; Volkswagen (with Thales, originator of the algorithm) sued in the UK, and on 25 June 2013 the High Court granted an injunction, holding that the security of millions of cars outweighed academic free speech in that instance. Withdrawn from the 2013 symposium, it was finally presented at USENIX Security '15 and published in the supplement to the 2013 proceedings, with the filter function withheld. The litigation detail rests on the court reporting, not on the paper.

## Related

- [Gone in 360 Seconds: Hijacking with Hitag2](gone-in-360-seconds-hijacking-with-hitag2.md)
- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md)
