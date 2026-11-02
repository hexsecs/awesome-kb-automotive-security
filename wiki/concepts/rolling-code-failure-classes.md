---
title: "Rolling-code failure classes"
summary: "Rolling codes move trust from the code's secrecy to the receiver's counter state; the failure classes attack that state: windows, resync, harvesting, blocking."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [key-fob-relay-attacks, lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems, rollback-a-new-time-agnostic-replay-attack-against-the-automotive-remote-keyless-entry-systems, flipper-arf, keyfob-analysis-toolkit-kat, sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it]
sources:
  - url: "https://arxiv.org/abs/2210.11923"
    retrieved: 2026-11-01
  - url: "https://www.usenix.org/conference/usenixsecurity16/presentation/garcia"
    retrieved: 2026-11-01
---

Remote keyless entry has three attack families. Relay extends a live exchange (the [key-fob relay](key-fob-relay-attacks.md) page). Cryptanalysis recovers key material and clones the fob (the Hitag2/Megamos and DST breaks that page contrasts against). This page covers the third family: attacks on the **freshness machinery itself**. A rolling code makes each fob transmission single-use by encrypting a counter; the receiver accepts a transmission whose counter falls inside a forward window of the last-seen value. The security therefore no longer rests on the code's secrecy alone — it rests on the **receiver's counter state**: how wide the window is, what the resynchronisation protocol permits, and what the receiver does when counters move the wrong way. Every class below attacks that state rather than the cipher. The [Stealing Cars SoK](../sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it.md)'s taxonomy reaches the same organisation from the literature side; its record that none of the published defences is deployed is the family's deployment baseline.

## Static and harvested codes

The degenerate member: systems that never actually roll, or accept a fixed fallback, fall to plain replay. The interesting member is **harvesting** — obtaining a *valid future* code without breaking anything. **RollJam** (Kamkar, 2015; treated on the relay page as background) jams the receiver while capturing the fob's press, lets the owner press again (capturing the second code while replaying the first), and banks the unused second code for later. [Lock It and Still Lose It](../lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md) documented the refined, cipher-independent variant: **selective jamming of one checksum byte** — the receiver rejects the corrupted frame, the attacker captures it intact, and the owner's retry behaviour supplies cover. Harvesting defeats rolling codes at their premise: the banked code is genuinely fresh, genuinely in-window, and genuinely the owner's.

## Resynchronisation abuse

Receivers must tolerate out-of-range counters (a fob pressed in a pocket fifty times must not brick the car), so they implement resync: a defined sequence of transmissions with counters in a wider window re-anchors the receiver's state. [RollBack](../rollback-a-new-time-agnostic-replay-attack-against-the-automotive-remote-keyless-entry-systems.md) (Csikor et al.) weaponised the tolerance: replaying carefully ordered *old* signals — captured days or ~100 days earlier — executes the resync procedure in reverse, rolling the receiver's counter state **back** so previously spent codes become valid again ("time-agnostic" replay). The vulnerable set was receiver-implementation-specific, not cipher-specific: Honda, Hyundai/Kia, Mazda, and Nissan implementations across NXP, Omron, and Microchip parts, with TI-based receivers uniformly immune and two NXP systems immune — a property of how each vendor coded the resync machine (its signal count, strictness, and time windows). Rolling-PWN is the Honda instance of the same class found independently. The class lesson: the resync protocol is a second, rarely audited state machine beside the counter itself, with its own acceptance rules an attacker can drive.

## Window and counter brute-force

Between the last-seen counter and the window's edge lies accepted space an attacker can simply *search*: transmit synthetic codes across the plausible counter range and let the receiver's window do the rest. The corpus's tooling ([flipper-arf](../flipper-arf.md), the [Keyfob Analysis Toolkit](../keyfob-analysis-toolkit-kat.md)) operationalises counter brute-force and window probing for the common transponder families. Garcia et al.'s counter-window analysis belongs here too: where the acceptance window and the counter's effective width are both small, exhaustive search over the gap is practical — the window sized for owner convenience becomes the attacker's search bound.

## Desynchronisation as effect

The mirror class: instead of moving the attacker's state forward, move the *owner's* state out of validity. Receivers with a **counter-behind blocking rule** (the VW Group 4 behaviour documented in [Lock It and Still Lose It](../lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md): a fob whose counter falls behind the receiver's stored value is refused) let an attacker who advances the receiver's counter — with harvested or synthetic in-window codes — lock the genuine fob out of its own car. Desync is usually catalogued as a side effect of the other classes; as a denial-of-entry attack in its own right it needs no code secrecy break at all, only write access to the receiver's state through its own acceptance rules.

## The unifying claim

Rolling codes did not remove a trust decision; they relocated it — from "does the presenter know the secret?" to "what does the receiver believe about the counter?" Windows, resync sequences, and blocking rules are that belief's mechanics, and each is an attack surface with a usability excuse: windows exist for pocket presses, resync for dead batteries and lost sync, blocking for clone detection. The corpus's defences are correspondingly receiver-side and mostly undeployed per the SoK: narrow windows with strict resync, resync that cannot run backwards, and treating counter-state anomalies as security events rather than housekeeping.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source. Its filing caveat (the RollBack paper then at stub depth) no longer applies: that page reached full depth in the papers campaign and the class now rests on it directly.

## Related

- [Key-fob relay attacks](key-fob-relay-attacks.md) — the live-extension family; this page is the counter-state family
- [Lock It and Still Lose It](../lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md) — selective jamming, counter windows, the VW-4 blocking rule
- [RollBack](../rollback-a-new-time-agnostic-replay-attack-against-the-automotive-remote-keyless-entry-systems.md) — resynchronisation abuse, the class's fullest study
- [Stealing Cars SoK](../sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it.md) — the taxonomy and the undeployed-defences baseline
