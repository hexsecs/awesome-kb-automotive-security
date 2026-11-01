---
title: "Gone in 360 Seconds: Hijacking with Hitag2"
summary: "Verdult, Garcia, and Balasch, USENIX Security 2012. Breaks the Hitag2 immobilizer transponder, then fitted to over 200 car models, recovering the key by…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/verdult"
status: unknown
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Verdult, Garcia, and Balasch, USENIX Security 2012. Breaks the Hitag2 immobilizer transponder, then fitted to over 200 car models, recovering the key by radio in minutes."
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/verdult"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer
  - key-fob-relay-attacks
  - lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems
---

Verdult, Garcia, and Balasch, USENIX Security 2012. Breaks the Hitag2 immobilizer transponder, then fitted to over 200 car models, recovering the key by radio in minutes.

## What it is

Roel Verdult and Flavio D. Garcia (Radboud University Nijmegen) and Josep Balasch (ESAT/COSIC, KU Leuven), 21st USENIX Security Symposium 2012, pp. 237–252. The paper fully analyses Hitag2, the proprietary immobilizer transponder introduced by NXP Semiconductors in 1996 and, at the time of the research, the most widely used transponder in the car immobilizer industry: fitted by at least 34 car makes in more than 200 different car models. Hitag2 is a passive 125 kHz RFID tag embedded in the car key; in crypto mode — the mode used in immobilizers — reader and transponder mutually authenticate with a proprietary stream cipher and a shared 48-bit key. The cipher (a 48-bit LFSR with a non-linear filter function) had been reverse engineered and published in 2007; this paper is the first full cryptanalysis with practical, implemented attacks, carried out on a Proxmark III platform (~$200) that can eavesdrop on, emulate, and interrogate transponders and readers.

## What it showed

**Three design weaknesses.** (1) *Arbitrary-length keystream oracle:* the transponder has no pseudo-random number generator and never challenges the reader, so any captured reader authentication pair can be replayed to it and will authenticate; commands can be extended with redundancy messages, and because the read command on the identifier block returns known plaintext, an attacker can iteratively extend recovered keystream — 2,048 contiguous keystream bits in under 30 seconds, without knowing the key. (2) *Session dependence:* the 48-bit cipher state is initialized with the 32-bit transponder identifier and the first 16 key bits, then randomized by only a 32-bit reader nonce XORed with the remaining key bits — so 16 key bits are identical in every session. (3) *Low-degree filter determination:* because of the filter function's two-layer structure, with probability 1/4 a keystream bit is determined by only 34 of the 48 state bits. The cipher can also be run backwards: from any recovered internal state, the LFSR rolls back to time zero and the key falls out.

**Three practical attacks**, all using only wireless communication. (1) *Malleability:* replaying a captured authentication and spending the recovered keystream on read/write commands dumps the transponder's whole memory, including its password, in under one second. The key blocks carry an optional one-time-programmable read-protection bit; where manufacturers failed to set it, the secret key itself reads out directly — the case for most cars the team tested from one French manufacturer. (2) *Time/memory trade-off:* a precomputed 1.2 TB table (building it takes under a day on a standard laptop) plus ~30 seconds harvesting keystream from the victim's transponder reduces key recovery to under 30 seconds of table lookups — total execution about one minute, regardless of the read-protection setting. (3) *Cryptanalysis — the title attack:* this one needs only the car. Using a transponder emulator, the attacker gathers 136 partial authentication traces from the immobilizer in about one minute; combining the session-dependence and filter weaknesses gives a 2^35-operation search taking under five minutes on an ordinary laptop — **the whole attack completes in under 360 seconds**.

**Experiments and deployment findings.** All three attacks were implemented and executed on more than 20 vehicles of various makes and models; on each, the team recovered the key and started the engine with their transponder-emulating device. Beyond the cipher, the deployments themselves were weak: most tested cars seed the reader nonce generator with the time (identical nonces within a one-second window); one French car's nonces had only 8 bits of entropy; a recent Korean model used the default password "MIKR" and a key with half its nibbles fixed; at least half of the tested cars used default or predictable transponder passwords. White-listing is not a barrier: all tested cars white-list transponder identifiers, but a valid ID can be wirelessly pickpocketed over the LF interface in milliseconds at proximity range, or eavesdropped from a hybrid remote's UHF transmission — cited from prior work as feasible at 100 metres. Earlier published attacks were impractical by comparison: algebraic/SAT attacks needed two days, and chosen-IV attacks are infeasible against the real protocol, which does not let the attacker choose the nonce.

## Where it fits

Together with the DST40 break (2005) and KeeLoq, one of the three canonical proprietary-immobilizer cipher breaks, and the direct predecessor of the same Radboud group's [Megamos break](dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md) (USENIX Security 2015). It belongs on the *cloning* side of the KB's [key-fob relay attacks](concepts/key-fob-relay-attacks.md) distinction: relay attacks forward a genuine key's exchange and need no cryptanalysis, whereas this paper breaks the cryptography itself, so a cloned or emulated transponder authenticates on its own. The paper itself discusses the NDSS 2011 relay work as the complementary, crypto-independent attack on keyless systems.

## Limits and safety notes

As the paper states them: the car-only cryptanalytic attack presupposes a valid transponder identifier (all tested cars white-list), so an attacker must first pickpocket or eavesdrop one; the direct key readout works only where the read-protection bit was not set (otherwise attacks 2 or 3 are needed). The attacks were validated on the 20+ vehicles the authors could test, not on all 200+ Hitag2 models. Responsible disclosure per the paper: NXP was notified six months before publication and the authors helped compile the customer advisory; the paper notes NXP had for years encouraged migration to AES-based products. The durable lesson is the paper's own: a 48-bit proprietary cipher, a transponder with no randomness of its own, and a session randomized by a nonce smaller than the state cannot protect a sole remaining anti-theft mechanism.

## Status and sources

Status: **unknown** — a finished 2012 publication; no living artefact (the Proxmark III tooling is generic; the authors' attack implementations were not released as a maintained project). No DOI — USENIX proceedings papers of this era carry none, and no library identifier is substituted. Full text openly available from USENIX and author mirrors; read in full 2026-11-01.

## Related

- [Dismantling Megamos Crypto: Wirelessly Lockpicking a Vehicle Immobilizer](dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md)
- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md)
- [Lock It and Still Lose It: On the (In)Security of Automotive Remote Keyless Entry Systems](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md)
