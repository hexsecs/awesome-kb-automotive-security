---
title: "Diagnostic-service abuse"
summary: "The diagnostic service set is the highest-privilege surface on the vehicle network: what it actuates, how its gates fail, and the one case where they held."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [uds-seed-key, experimental-security-analysis-of-a-modern-automobile, adventures-in-automotive-networks-and-control-units, remote-exploitation-of-an-unaltered-passenger-vehicle, comprehensive-experimental-analyses-of-automotive-attack-surfaces, beneath-the-bonnet-a-breakdown-of-diagnostic-security, simos18-sboot, can-availability, bootloader-stages]
sources:
  - url: "https://www.usenix.org/legacy/events/sec10/tech/full_papers/Koscher.pdf"
    retrieved: 2026-11-01
  - url: "https://www.usenix.org/system/files/conference/usenixsecurity13/sec13-paper_miller.pdf"
    retrieved: 2026-11-01
  - url: "https://illmatics.com/Remote%20Car%20Hacking.pdf"
    retrieved: 2026-11-01
---

Normal traffic on a vehicle network is narrow: an ECU broadcasts what it measures, and receivers act on it. The diagnostic service set is different in kind. It exists so that a technician — or a factory tool — can command the car: run the brake bleed, drive an actuator, download new firmware, silence a module for testing. Across this KB's paper pages, nearly every highest-privilege effect runs through a diagnostic service rather than through forged normal traffic: brakes released and locked at speed, engines killed, code uploaded and executed, ECUs silenced so their identity can be borrowed. The [seed/key gate](uds-seed-key.md) has its own page; this page is about what the gate protects — and the recurring cases where there is no gate, the gate is not checked, or the service itself is the payload.

The service families recur across manufacturers and decades: session and communication control (enter a programming session; disable an ECU's normal transmissions), IO control and proprietary actuation services (Koscher's **DeviceControl** — a proprietary service as its paper names it, not a standard UDS service ID), RoutineControl (run a named routine), and the download trio (RequestDownload / TransferData / RequestTransferExit). The failures organise into four modes.

## Ungated services

The simplest mode: the service answers anyone on the bus. In [Miller & Valasek 2013](../adventures-in-automotive-networks-and-control-units.md), a RoutineControl kills the Escape's engine at any speed **with no diagnostic session at all**, and on the Prius most diagnostic functions need no SecurityAccess — including dealer "active tests" that drive the pre-collision seat-belt pre-tensioner motors, with no restriction on when they may be issued. In [Koscher 2010](../experimental-security-analysis-of-a-modern-automobile.md), all fifteen BCM DeviceControl effects — locks, lights, horn, shift-lock — worked at speed and **none required unlocking the BCM**; the gating pattern was per-ECU and inconsistent even within one car (every ECM effect did require the key). An attacker who reaches the bus inherits whichever of these the manufacturer left open, and the KB's record gives no way to predict which from outside.

## State and session rules not enforced

The standards anticipate danger and fence it with state: some services must be refused while the vehicle is moving, some sessions must not be enterable with the engine running. Koscher's car accepted the disable-communications command **while moving**, against the standard's own safety rule, and engine/transmission modules entered reflashing mode with the engine running. The failure is not a missing check in one routine but a pattern: the rule exists in the specification, the implementation does not enforce it, and nothing downstream notices. Protocol-aware diagnostic fuzzing (a filed companion concept) is the method that finds these gaps systematically; the point here is that they are *specification-compliance* failures, invisible to anyone who only audits the service list.

## The service as execution path

Twice in the corpus, the diagnostic download path stops being a channel and becomes the exploit itself. Miller & Valasek 2013: data uploaded to the Escape's PAM through the diagnostic download path, beginning with a magic header, is **called as code** via a RoutineControl — arbitrary code execution with CAN read/write, from a service whose nominal job is calibration. [Beneath the Bonnet](../beneath-the-bonnet-a-breakdown-of-diagnostic-security.md) generalises it: across four manufacturers, diagnostic services download a "secondary bootloader" into RAM and a RoutineControl jumps into it, yielding memory, firmware, and peripheral access — diagnostics alone, entry to execution, with only the level-1 secret ever needed because extracted firmware holds the rest. [Simos18](../simos18-sboot.md) shows the mode-confusion variant: an **undocumented UDS routine** switches an otherwise signature-verified boot chain from its locked ASW stage into the weaker SBOOT stage. In each case the service set's *composition* — download plus jump, routine plus boot stage — is the vulnerability, not any single service's access control.

## Diagnostics as silencing

The fourth mode uses diagnostics not on the target but on a *third party*: enter a diagnostic session with a genuine ECU to silence its normal transmissions, then transmit in its name. Miller & Valasek 2015 steered the Jeep only after **silencing the genuine parking-assist module** this way; Koscher's component results show the system-level weight of a mute — with the ECM silenced the speedometer reads 0, with the BCM silenced the instrument cluster froze and the car could not be restarted. Silencing is the bridge between this page and [CAN injection](can-injection.md): injection forges a sender, diagnostics can first remove the real one, so plausibility checks that assume the genuine ECU is still talking never fire.

## The counter-case: when the gate held

The corpus has one clear instance of state enforcement working. In [Miller & Valasek 2015](../remote-exploitation-of-an-unaltered-passenger-vehicle.md), the Jeep's diagnostic routines carried the physical effects (fuel-injector kill, brake bleed) — and the session/state rules **did** gate them to low speeds, which is why the remote chain's high-speed effects had to come from elsewhere. The lesson cuts both ways: enforcement is implementable on production hardware of the era, so its absence elsewhere is a choice or an oversight, not a constraint — and a determined attacker routes around a working gate rather than through it, which bounds what gating alone can promise.

## Boundary with the gate

Seed/key weakness — short seeds, constants, keys in dealer tools and firmware — is the [uds-seed-key](uds-seed-key.md) page's subject and is deliberately not duplicated here. The split matters because the two fail independently: Beneath the Bonnet's gate fell to extracted ciphers *and* the gated services were execution paths; Koscher's BCM needed no gate defeated because none was asked. Auditing either layer alone misprices the other. The diagnostic *tooling* substrate (udsoncan, UDSim, conescan and peers) lives on the KB's Diagnostic Tools entity pages; this page synthesises the attack record, not the tools.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source.

## Related

- [UDS seed/key](uds-seed-key.md) — the gate this page looks behind
- [Experimental Security Analysis of a Modern Automobile](../experimental-security-analysis-of-a-modern-automobile.md) — Koscher 2010; DeviceControl and the unenforced state rules
- [Adventures in Automotive Networks and Control Units](../adventures-in-automotive-networks-and-control-units.md) — Miller & Valasek 2013; ungated routines and the download-execution path
- [Remote Exploitation of an Unaltered Passenger Vehicle](../remote-exploitation-of-an-unaltered-passenger-vehicle.md) — Miller & Valasek 2015; silencing, and the low-speed gate that held
- [Beneath the Bonnet](../beneath-the-bonnet-a-breakdown-of-diagnostic-security.md) — diagnostics-only RCE across four manufacturers
- [Simos18 SBOOT](../simos18-sboot.md) — the undocumented routine as boot-stage confusion
