---
uid: 01a19d3c-afba-7c15-92de-ea86fefa378b
title: "OWASP Automotive Security Cheat Sheet"
summary: "OWASP cheat sheet covering threat modeling, message authentication, secure boot, and update verification for vehicle ECUs and connected services."
type: entity
category: "Learning Resources"
url: "https://cheatsheetseries.owasp.org/cheatsheets/Automotive_Security_Cheat_Sheet.html"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "OWASP cheat sheet covering threat modeling, message authentication, secure boot, and update verification for vehicle ECUs and connected services."
sources:
  - url: "https://cheatsheetseries.owasp.org/cheatsheets/Automotive_Security_Cheat_Sheet.html"
    retrieved: 2026-11-01
  - url: "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Automotive_Security_Cheat_Sheet.md"
    retrieved: 2026-11-17
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - secure-firmware-updates
  - uds-seed-key
  - automotive-cyber-security
  - automotive-cybersecurity-engineering-handbook
  - automotive-security-research
---

OWASP cheat sheet covering threat modeling, message authentication, secure boot, and update verification for vehicle ECUs and connected services.

A single-page developer reference in the OWASP Cheat Sheet Series: start from a threat model, then concrete guidance on authenticating vehicle messages (AUTOSAR SecOC with freshness), TLS for external connections, secure boot, Uptane-style signed update verification, per-operation authorization, hardware-backed key protection, and lifecycle testing and logging — cross-referenced throughout to NHTSA best practices, AUTOSAR, NIST, and the Uptane standard.

It is for engineers building ECU or connected-service software who need defensible defaults quickly, and it is unusually honest for the genre: nearly every control is paired with what it does *not* do (SecOC does not encrypt; secure boot does not stop runtime exploitation). It is guidance, not a standard or a compliance checklist — the depth lives in the documents it points to.

## How it works

The page is organised into five short sections, each a set of imperatives with an inline limitation. The structure is itself the method: start with a threat model, then work outward from communications to the lifecycle.

**Introduction.** Map external connections, diagnostic access, sensitive data, and paths to safety-critical functions first. The distinctive instruction is to agree on *safe failure* behaviour with the vehicle's safety engineers before deploying anything — automatically shutting down a moving vehicle can introduce danger. NHTSA's best-practices document is the named development framework.

**Protect communications and inputs.** Four controls, each paired with its blind spot:

- **Separate trust zones** — isolate infotainment, wireless connectivity and diagnostics from safety-critical controls, and allow only required flows through gateways. Limitation: segmentation bounds a compromise's reach but does not authenticate messages *within* a segment.
- **Authenticate vehicle messages** — conventional CAN has no sender authentication, so use a platform scheme such as AUTOSAR SecOC with freshness checks against replay. Limitation: SecOC authenticates configured data only; it does not encrypt, does not stop bus flooding, and a compromised sender can still emit authenticated messages.
- **Protect external connections** — TLS with certificate validation to backend and app, authenticating vehicles individually. Limitation: an encrypted connection alone does not authorize commands.
- **Validate before acting** — check lengths, types, ranges and whether the action is permitted in the current vehicle state, even on authenticated inputs. Limitation: authentication does not establish that a sensor reading is physically correct.

**Verify software and updates.** Secure boot with a protected trust root for the boot chain, including recovery firmware (NIST SP 800-193 §§4.3–4.4). For OTA and workshop updates, verify signed metadata, image hashes, target hardware, freshness and rollback policy against Uptane's requirements. Activate only under agreed safe conditions and recover from interrupted installs without bypassing rollback. Two limits: secure boot does not prevent runtime exploitation of trusted-but-vulnerable software, and signatures say nothing about whether the software is free of bugs — the supply chain needs protecting too.

**Restrict access and protect data.** Authorize each operation for the specific vehicle and action in both backend and ECU handlers; separate owner, fleet and service privileges and revoke them when access ends. Disable production debug access and authenticate necessary diagnostics without breaking authorized repair — physical access is not authorization (NHTSA §§7–8.4). Avoid fleet-wide shared secrets; use hardware-backed key protection with renewal and revocation, minimise retained location and personal data, and encrypt storage with keys held separately. Encryption limits offline extraction but software authorised to decrypt can still expose the data.

**Test and maintain.** Follow NHTSA §4.2 lifecycle practices: track component versions against deployed vehicles, test rejected commands, malformed inputs, replay and interrupted updates on isolated benches or simulators, log failures and privileged operations without secrets, and plan replacement for unpatchable components. Gateway filtering reduces exposure but does not repair vulnerable firmware.

## Where it fits

This is the KB's compact "what should a defensive ECU engineer actually do" reference, and the one entry that consistently names the limits of its own advice. The message-authentication guidance is the applied counterpart of [CAN message authentication: the retrofit design space](concepts/can-message-authentication.md); the update-verification section is the applied form of [Secure firmware updates](concepts/secure-firmware-updates.md); and the diagnostic-access rule assumes the mechanism described in [UDS seed/key](concepts/uds-seed-key.md). For the standards and process view behind the cheat sheet's shorthand, the KB's [TARA methodology](concepts/tara-methodology.md) and the [Automotive Cybersecurity Engineering Handbook](automotive-cybersecurity-engineering-handbook.md) go deeper.

## Limits and safety notes

It is guidance, not a standard or a compliance checklist, and deliberately shallow: the substance is in the linked NHTSA, AUTOSAR, NIST and Uptane documents, which this page summarises rather than replaces. The safety framing is load-bearing — "fail safe" is to be negotiated with safety engineers, not assumed. The control catalogue is defensive and ECU/backend-centric; it does not attempt attack tooling or vulnerability research, and its sandbox-test advice assumes access to a bench or simulator. Content was read from the Cheat Sheet Series master markdown on 2026-11-17; a live site can move between checks.

## Status and sources

Status: **active** — published and maintained as part of the OWASP Cheat Sheet Series; the page is live and current at https://cheatsheetseries.owasp.org/cheatsheets/Automotive_Security_Cheat_Sheet.html — checked 2026-11-01.

## Related

- [Secure firmware updates](concepts/secure-firmware-updates.md) — the concept behind the cheat sheet's update-verification section
- [UDS seed/key](concepts/uds-seed-key.md) — the diagnostic-access mechanism its access-control guidance assumes
- [Automotive Cyber Security](automotive-cyber-security.md)
- [Automotive Cybersecurity Engineering Handbook](automotive-cybersecurity-engineering-handbook.md)
- [automotive-security-research](automotive-security-research.md)
