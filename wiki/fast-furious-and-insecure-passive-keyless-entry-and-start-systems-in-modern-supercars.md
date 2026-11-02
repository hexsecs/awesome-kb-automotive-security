---
title: "Fast, Furious and Insecure: Passive Keyless Entry and Start Systems in Modern Supercars"
summary: "Wouters et al., CHES 2019. Breaks the DST40-based PKES used by Tesla and others, cloning a key fob from a few seconds of proximity."
type: entity
category: "Research Papers"
url: "https://tches.iacr.org/index.php/TCHES/article/view/8289"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Wouters et al., CHES 2019. Breaks the DST40-based PKES used by Tesla and others, cloning a key fob from a few seconds of proximity."
sources:
  - url: "https://tches.iacr.org/index.php/TCHES/article/view/8289"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - key-fob-relay-attacks
  - relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars
  - lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems
  - gone-in-360-seconds-hijacking-with-hitag2
  - dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer
---

Wouters et al., CHES 2019. Breaks the DST40-based PKES used by Tesla and others, cloning a key fob from a few seconds of proximity.

## What it is

Lennert Wouters, Eduard Marin, Tomer Ashur, Benedikt Gierlichs, and Bart Preneel — imec-COSIC, KU Leuven (Marin also University of Birmingham). *IACR Transactions on Cryptographic Hardware and Embedded Systems* 2019, issue 3, pp. 66–85 (TCHES is the CHES journal; the list records the venue as CHES 2019). The paper fully reverse engineers a production Passive Keyless Entry and Start (PKES) system — the one designed by Pektron and deployed in the Tesla Model S. PKES unlocks and starts the car on proximity alone; before this work the design had received little attention besides relay attacks, and the paper's question is whether it withstands attacks of its own. The entry point was public: the FCC filing identifies the Model S fob's chip as Texas Instruments' TMS37F128 — a package pairing a Digital Signature Transponder die (TMS37126) with an MSP430F1232 microcontroller. From TI's abridged datasheet the authors expected DST80, TI's 2008 successor cipher. What the fob was actually running was DST40 — the 40-bit proprietary cipher Bono et al. reverse engineered in 2005 and brute-forced on an FPGA cluster in under an hour.

## What it showed

**The transponder had undocumented commands, and the fob used the weakest of them.** Without the NDA-gated datasheets, the authors fuzzed the DST chip's SPI interface from an Arduino breakout board — the busy line errors on an invalid command byte, and a length byte of 0xFF exposes each command's true length the same way — and recovered every valid command, including four undocumented challenge–response commands: two independent DST40 implementations under two 40-bit keys, two implementations of an unknown 40-bit function (DST_UNK; also reverse engineered and similar in nature to DST40, but its description is left out of the paper), and commands to change both keys. On the fob, the MSP430's JTAG fuse was not blown and its debug pads easily accessible, so the full firmware was read out with an Olimex debugger — no readout protection, in the paper's terms — and analysis of the SPI traffic showed the fob uses exactly one cipher command: 0x86, DST40. No new cryptanalysis was needed: a 40-bit key falls to exhaustive search, and because the 40-bit challenge is compressed to a 24-bit response, two challenge–response pairs pin the key down.

**The protocol gives the attacker everything else.** The car polls with 3-byte LF (134.2 kHz) wake frames — a 2-byte car identifier and a command byte; the fob's reply is a fixed value calculable from the wake frame by byte swaps and shifts, so it authenticates nothing. The car then sends a 40-bit challenge and the fob answers over UHF (433.92 MHz) with the 24-bit DST40 response. Three structural failures compound the weak cipher: there is **no mutual authentication**, so the fob answers any correctly formatted challenge from anyone — a chosen-input oracle; there is **no security partitioning**, so the same 40-bit key unlocks the car and then, in a second identical exchange at the brake pedal, satisfies the immobilizer and starts it; and there is **no distance bounding** (the system is separately relay-vulnerable, as ADAC had confirmed in practice). The button-press RKE protocol reuses the same key: a 40-bit EEPROM counter serves as the DST40 input, and the packet is an action byte plus the 3-byte response plus the counter's two low bytes. The action byte is unauthenticated, so the rolling code is open to RollJam-style jam-and-replay — and a captured lock command can be flipped into an unlock before retransmission.

**A car-only attack exists but is impractical — and nothing rate-limits it.** Interrogating the car itself takes on average ~2^23 key guesses (≈97 days at one per second) for a first challenge–response pair, then a ~2^16 candidate list testable in about 9 hours more — under 100 days total. Judged impractical without a speedup, but the precondition is verified: 40,000 timed-out protocol runs in 12 hours on a Model S met no rate limiting or lockout.

**The practical attack clones a fob in seconds.** Impersonating the car, the attacker sends two chosen challenges to the victim's fob from roughly a metre away — a few seconds of proximity, e.g. walking past the owner — exploiting the missing mutual authentication. Key recovery is a time–memory trade-off prepared in advance: a 5.4 TB lookup grouping all keys by their response to one fixed challenge (2^24 files of ~2^16 keys). The first pair selects the candidate file; the second resolves the key in ~2^15 DST40 invocations — under 2 seconds on one 1.4 GHz ARM core. The whole platform (Proxmark III with a modified LF receive path, YARD Stick One, Raspberry Pi 3, 6 TB drive, battery) is off-the-shelf, cost about $600, and fits in a backpack. The full attack was carried out on two Tesla Model S vehicles with the owners' consent — unlocking and driving away; one car was provided by Tesla's own engineering team.

## Where it fits

This is a **cloning** break, and the KB's [key-fob relay attacks](concepts/key-fob-relay-attacks.md) concept page cites it in exactly those terms. A relay attack forwards a genuine key's exchange and works against sound cryptography; here the cryptography itself is recovered, after which the attacker's device authenticates on its own, at any later time, with no genuine key nearby. Within the transponder-cipher line the KB already tells — DST40 (2005), KeeLoq, [Hitag2](gone-in-360-seconds-hijacking-with-hitag2.md) (2012), [Megamos](dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md) (2015) — this paper's sting is different: DST40 was the first of those ciphers to fall, in 2005, and fourteen years later it was still the deployed cipher in a flagship luxury car, now protecting entry *and* start with one shared key. [Lock It and Still Lose It](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md) (2016) is the nearest comparison and the failure modes mirror: there, one eavesdropped code plus a recovered global key clones a remote; here, two elicited pairs plus a precomputed table clone a fob. The difference is key management — VW's keys were global, this key is per-fob — and it saves nothing, because 40 bits is brute-forceable per fob. The paper's framing: the secrecy regime around the system (NDA datasheets, an unscrutinized proprietary cipher) prevented exactly the review that would have caught this.

## Limits and safety notes

- **Proximity is required for the practical attack:** about a metre from the fob for a few seconds; the authors made no effort to extend that range, and a longer-range variant is not a result in the paper.
- **Scope beyond Tesla is the authors' inference, not a measurement.** The same Pektron PKES is used by McLaren, Karma, and Triumph motorcycles, and the findings "most likely apply" to them — but the authors had no access to those vehicles and did not verify the attack on any of them. The vendor statements in the paper's Appendix A cut both ways: McLaren's addresses mainly the ~100-day car-only method and calls the risk low; Triumph's describes the attack as a relay attack, which the authors note it is not.
- **Disclosure and response, as documented in the paper:** Tesla was notified on 31 August 2017, confirmed the findings, and hosted a demonstration on an engineering vehicle. Its statement (Appendix A.1) records the shipped mitigations: an over-the-air option to disable passive entry, PIN to Drive, and — with its supplier — more robust cryptography in Model S fobs from June 2018, with earlier owners able to switch to the new fobs. Texas Instruments was also informed; Pektron did not reply.
- **The paper's own short-term mitigations are labelled stopgaps:** moving to DST80 would defeat search and trade-off attacks but rests on another unscrutinized proprietary cipher ("no new vehicle … should rely on DST80"); the preferred directions are a vetted lightweight cipher computed in the fob's microcontroller firmware, mutual authentication, an authenticated RKE action byte, and independent keys for unlock and start.
- **Deliberate omissions:** DST_UNK's description is withheld, and whether the undocumented commands amount to a working DST80 implementation is inference from the command set — the fob uses only the DST40 command.

## Status and sources

Status: **unknown** — a finished 2019 publication; no living artefact. Bibliographic record: *IACR Transactions on Cryptographic Hardware and Embedded Systems* 2019(3), pp. 66–85, published 9 May 2019. The paper carries DOI 10.13154/tches.v2019.i3.66-85, printed in the paper itself and on the publisher's article page, and registered with DataCite (record checked 2026-11-01: title and publisher match). It has **no Crossref record** (works endpoint returns 404, checked 2026-11-01), so it is flagged rather than asserted silently; every other bibliographic element was verified against the publisher's page and the paper. Full text read in full from the publisher's open PDF, 2026-11-01.

## Related

- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md) — the contrasting attack class this paper is *not*
- [Relay Attacks on Passive Keyless Entry and Start Systems in Modern Cars](relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars.md) — the relay attack the same system also admits
- [Lock It and Still Lose It](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md) — RKE cloning by global keys, the mirror failure
- [Gone in 360 Seconds: Hijacking with Hitag2](gone-in-360-seconds-hijacking-with-hitag2.md)
- [Dismantling Megamos Crypto](dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md)
