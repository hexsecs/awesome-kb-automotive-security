---
uid: 01a19d3c-af5a-7e5d-bdf3-698d5606511e
title: "The calibration plane (XCP/A2L)"
summary: "Beside diagnostics sits a second access plane into production ECUs: XCP's direct memory access and the A2L maps that name everything it can touch."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [pyxcp, pya2l, caringcaribou, autofuze, diagnostic-service-abuse, beneath-the-bonnet-a-breakdown-of-diagnostic-security]
sources:
  - url: "https://github.com/christoph2/pyxcp"
    retrieved: 2026-11-01
  - url: "https://github.com/christoph2/pya2l"
    retrieved: 2026-11-01
---

The [diagnostic plane](diagnostic-service-abuse.md) is not the only standardised way into a production ECU. Beside UDS sits **XCP** (Universal Measurement and Calibration Protocol), the ASAM standard built for development: connect to a running ECU, read and write its memory directly, adjust calibration values live, and watch internal variables at rate. XCP exists so calibration engineers can tune an engine on a dyno without reflashing between iterations. The security question this page collects is what happens when that development plane survives into production vehicles — because its trust model was written for a laboratory, and the corpus documents it reachable from the vehicle network.

## The plane's shape

Where UDS offers *services* (named operations with defined semantics), XCP offers *memory*: upload/download of raw address ranges, calibration-page switching, and synchronous data acquisition from named variables. [pyXCP](../pyxcp.md) is the corpus's implementation — a full XCP master over CAN, Ethernet, USB, and serial transports. The addressing knowledge lives outside the protocol, in **A2L files**: the ASAM MCD-2 MC description that names every calibration parameter, measurement variable, memory address, and data type for a specific ECU software build. [pyA2L](../pya2l.md) parses them. An A2L file is therefore a sensitive artefact in itself: unauthenticated metadata that converts XCP's raw memory access into a named map of everything tunable — the difference between writing bytes and turning the specific knob that governs, say, a torque limit.

## The trust model, and its differences from diagnostics

XCP has its own protection: resources (calibration, data acquisition, stimulation, programming) can each be locked behind **seed-and-key** unlock, conceptually parallel to UDS SecurityAccess. The differences from the diagnostic plane are the point:

- **Granularity of effect.** A diagnostic service does what its designer enumerated; a memory write does what the address map allows. The calibration plane's blast radius is the whole calibration dataset plus any writable RAM — including, on some architectures, the variables other safety logic trusts.
- **Development provenance.** The plane's presence in production is usually an inheritance, not a decision: the calibration build's XCP slave, its A2L, and its unlock DLL shipped because removing them was a step nobody owned. Beneath the Bonnet's corpus adds the strangest provenance in the KB: ECUs that *lack* XCP natively receive it at runtime — diagnostic services download the XCP stack into RAM (on the [diagnostic-service abuse](diagnostic-service-abuse.md) page's execution-path evidence), so the two planes compose rather than compete.
- **The gate's ecosystem.** XCP seed/key lives in vendor DLLs distributed through the calibration toolchain (INCA/CANape-class tools), the same dealer/toolchain leakage pattern as UDS keys, with an even smaller distribution audience and correspondingly less scrutiny.

## The corpus's tooling posture

The attack-side tooling treats XCP as enumerated surface, not theory: [CaringCaribou](../caringcaribou.md)'s XCP module performs discovery, information retrieval, and memory dumping as a standard reconnaissance step beside its UDS and DoIP modules; [AutoFuze](../autofuze.md) fuzzes XCP beside UDS in one framework, its most recent development on the XCP path. That is the practical verdict: on a modern ECU audit, probing for a live XCP slave with an unlocked calibration resource is a checklist item, and the A2L hunt (leaked in toolchain packages, supplier shares, and tuning forums) is part of the same step.

This page synthesizes the KB's own full entity pages named above and in its frontmatter. Its filing evaluation recorded the fold-into-diagnostic-abuse alternative explicitly; the page stands alone because the plane's trust model (memory semantics, development provenance, A2L sensitivity) is distinct from the diagnostic services' — but the two pages cross-link throughout, and a reader of either should read the other's framing section.

## Related

- [pyXCP](../pyxcp.md) — the corpus's XCP master implementation
- [pyA2L](../pya2l.md) — parsing the maps that make memory access meaningful
- [CaringCaribou](../caringcaribou.md) — XCP as enumerated attack surface
- [Diagnostic-service abuse](diagnostic-service-abuse.md) — the neighbouring plane, and the channel that sometimes installs this one
- [Beneath the Bonnet](../beneath-the-bonnet-a-breakdown-of-diagnostic-security.md) — the XCP-stack-in-RAM composition case
