---
title: "OWASP Automotive Security Cheat Sheet"
summary: "OWASP cheat sheet covering threat modeling, message authentication, secure boot, and update verification for vehicle ECUs and connected services."
type: entity
category: "Learning Resources"
url: "https://cheatsheetseries.owasp.org/cheatsheets/Automotive_Security_Cheat_Sheet.html"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "OWASP cheat sheet covering threat modeling, message authentication, secure boot, and update verification for vehicle ECUs and connected services."
sources:
  - url: "https://cheatsheetseries.owasp.org/cheatsheets/Automotive_Security_Cheat_Sheet.html"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - secure-firmware-updates
  - uds-seed-key
---

OWASP cheat sheet covering threat modeling, message authentication, secure boot, and update verification for vehicle ECUs and connected services.

A single-page developer reference in the OWASP Cheat Sheet Series: start from a threat model, then concrete guidance on authenticating vehicle messages (AUTOSAR SecOC with freshness), TLS for external connections, secure boot, Uptane-style signed update verification, per-operation authorization, hardware-backed key protection, and lifecycle testing and logging — cross-referenced throughout to NHTSA best practices, AUTOSAR, NIST, and the Uptane standard.

It is for engineers building ECU or connected-service software who need defensible defaults quickly, and it is unusually honest for the genre: nearly every control is paired with what it does *not* do (SecOC does not encrypt; secure boot does not stop runtime exploitation). It is guidance, not a standard or a compliance checklist — the depth lives in the documents it points to.

## Status and sources

Status: **active** — published and maintained as part of the OWASP Cheat Sheet Series; the page is live and current at https://cheatsheetseries.owasp.org/cheatsheets/Automotive_Security_Cheat_Sheet.html — checked 2026-11-01.

## Related

- [Secure firmware updates](concepts/secure-firmware-updates.md) — the concept behind the cheat sheet's update-verification section
- [UDS seed/key](concepts/uds-seed-key.md) — the diagnostic-access mechanism its access-control guidance assumes
