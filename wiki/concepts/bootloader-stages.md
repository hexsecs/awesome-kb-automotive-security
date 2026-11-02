---
title: "Bootloader stages and bootstrap entry"
summary: "ECUs boot through layers owned by different parties; the corpus's breaks concentrate at the stage transitions and the weakest stage, not the application."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [simos18-sboot, tc1791-can-bsl, secoc-key-extractor, vw-flash, diagnostic-service-abuse, secure-firmware-updates]
sources:
  - url: "https://github.com/0xD006/TC1791_CAN_BSL"
    retrieved: 2026-11-01
  - url: "https://github.com/bri3d/VW_Flash"
    retrieved: 2026-11-01
---

An ECU does not boot its application directly. Between power and application sits a chain of smaller programs, each loading and (in principle) verifying the next, and each typically owned by a different party: the **silicon vendor's** ROM bootstrap, the **Tier-1 supplier's** bootloader, and the **application-stage** loader that starts the OEM's software. This page synthesises what the KB's firmware corpus shows about that chain — because the demonstrated breaks do not attack the application head-on. They enter at a stage transition, or drop into the weakest stage and work from there. A layered boot only helps if every layer holds; the corpus is a record of layers that didn't.

## The stages as the corpus documents them

**The ROM bootstrap loader (BSL).** Masked into the silicon, immutable, entered by hardware state (strapping pins) rather than by software request. The [TC1791 CAN BSL](../tc1791-can-bsl.md) is the documented instance: Infineon's TriCore bootstrap, speaking over CAN, gated by a 32-bit boot password. Because the ROM cannot be patched, its gate is permanent — an unprotected or weakly passworded BSL is a lifetime property of every ECU built on that silicon, and its read/write primitives operate below every later stage's verification.

**The supplier bootloader.** Flash-resident, updatable in principle, and the stage where the corpus's richest case lives. [Simos18](../simos18-sboot.md) (Continental's engine ECU line) boots a locked ASW bootloader — but beneath it sits **SBOOT**, a weaker resident stage reachable two ways: by design, through a PWM signal on a pin; and in practice, through an **undocumented UDS routine** that switches the locked stage into SBOOT. SBOOT's own gate is a boot password — recoverable because the password check is a CRC with a bounds-check flaw, turning the credential into a computation. [VW_Flash](../vw-flash.md) productised the whole chain: BSL/BSL-adjacent entry plus password recovery, packaged as a flashing tool for the MQB platform.

**The application-stage loader and RAM paths.** Some ECUs' update machinery itself becomes the entry: [secoc-key-extractor](../secoc-key-extractor.md)'s target, a Toyota EPS ECU, exposes a bootloader update path that accepts code uploaded to RAM — intended for servicing, functioning as a code-execution hook for whoever reaches it. The stage designed to *replace* stages is, reached out of turn, an execution primitive inside the chain.

## Entry modes, collected

The corpus's entries into the chain, abstracted: (1) **hardware state** — pins strapped at reset (BSL entry; needs physical access or a designed-in signal like Simos18's PWM line); (2) **a diagnostic routine** — the undocumented UDS routine into SBOOT, a software request crossing a stage boundary that the architecture treated as trusted (the boundary with [diagnostic-service abuse](diagnostic-service-abuse.md): the routine is a diagnostic service, but what it *does* is stage transition, which is why this page owns the consequence and that page owns the service); (3) **the update path itself** — RAM-upload servicing hooks; (4) **credential recovery against the stage's own gate** — the CRC bounds-check flaw making SBOOT's password computable rather than guessable.

## Per-stage credentials do not compose

Each stage carries its own credential — BSL boot password, SBOOT boot password, the application's seed/key — provisioned by different parties at different times, with no shared strength floor. The architecture's security is therefore the *minimum* over stages for an attacker who can choose their entry, while the defender must hold *all* of them. Simos18 is the worked proof: a signature-verified ASW stage did not save the chain, because the chain also contained SBOOT. This is the boot-side mirror of Beneath the Bonnet's multi-level collapse (only the level-1 secret ever needed) on the [diagnostic-service abuse](diagnostic-service-abuse.md) page — at every layering in this corpus, the layers share fate through their weakest member.

## Boundary with delivery-time verification

[Secure firmware updates](secure-firmware-updates.md) asks whether an *arriving image* is authentic. This page asks a prior question: which code runs the check, and how did the checker itself get loaded and gated? An update verified by a stage the attacker can bypass or replace was never verified in any sense that binds. Acquisition channels (the [firmware acquisition](firmware-acquisition.md) page) intersect here too — the BSL is simultaneously a boot stage and a read channel; the same password gates both directions.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source.

## Related

- [Simos18 SBOOT](../simos18-sboot.md) — the layered chain and its weakest stage, in full
- [TC1791 CAN BSL](../tc1791-can-bsl.md) — the ROM stage and its permanent gate
- [VW_Flash](../vw-flash.md) — the entry-plus-recovery chain, productised
- [SecOC key extractor](../secoc-key-extractor.md) — the update path as execution hook
- [Diagnostic-service abuse](diagnostic-service-abuse.md) — the service that crosses the boundary
- [Secure firmware updates](secure-firmware-updates.md) — delivery-time verification, downstream of the chain
