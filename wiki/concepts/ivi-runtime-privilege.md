---
title: "IVI runtime privilege and service exposure"
summary: "The head unit's failures that are not on the update path: declared-but-unenforced permissions, unchecked service callers, and designed-in debug surfaces."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [byd-dolphin-hacking, mmi3g-toolkit, q50-reverse-engineering, ivi-update-trust]
sources:
  - url: "https://github.com/redcat-3/BYD-Dolphin-Hacking"
    retrieved: 2026-11-01
---

The [IVI update-trust](ivi-update-trust.md) page covers how firmware *arrives* at the head unit. This page covers the head unit while it *runs* — because the corpus documents a second IVI failure family that has nothing to do with updates: the platform's runtime privilege boundaries, declared on paper and not enforced in code. An IVI system inherits a general-purpose OS's privilege model (Android or Linux users, permission levels, inter-process service calls), and the failures below share one shape: a boundary the platform *has* — a permission declaration, a caller check, a debug surface meant to be off — turns out to be decorative. Whoever reaches the boundary (an app, a shell, a USB stick) inherits privileges the architecture diagram says they should not have, and from the head unit the vehicle network is one gateway hop away.

## The anchor case: BYD Dolphin's DiLink

The [BYD Dolphin](../byd-dolphin-hacking.md) assessment is the corpus's complete instance, with three boundaries failing in sequence. **Permissions:** vehicle-control permissions are declared at Android's *normal* protection level — grantable without the system signature the platform reserves for dangerous capabilities — so an ordinary app can hold them. **The client-side check:** the permission check that does exist is enforced in client library code, and an override path auto-grants it, making the check advisory to anyone who bypasses the library. **Service caller checks:** thirteen-plus system services running as root accept Binder IPC calls from the **shell UID** without verifying the caller — and ADB shell access on these units is a documented, low-barrier state. A factory **debug application** ships in the same image. Compose them: unprivileged shell → root service → vehicle functions, with CAN injection in reach — not through any update flaw, but through the runtime's own declared model failing at every joint.

## Supporting instances

**Designed-in execution surfaces.** The [MMI 3G](../mmi3g-toolkit.md) page documents Audi's manufacturer-provided SD-card script-execution mechanism: a runtime surface that runs supplied scripts by design, for service use. Like the debug app, it is not a bug — it is a capability whose threat model assumed physical possession equals authorisation, an assumption the rest of the corpus (valet, rental, resale, theft) does not support.

**Privileged parsers of untrusted input.** The [Q50](../q50-reverse-engineering.md) case: a stock USB media-watcher service parses untrusted packages with service privilege — the classic parser-at-privilege pattern, in a head unit. Media parsing is the IVI's largest untrusted-input surface (files, streams, metadata), and the corpus's [Chimaera](../chimaera.md)-class findings on the neighbouring platform show where privileged parser flaws lead.

## The unifying claim

Update trust asks *"is this code authorised to be here?"* Runtime privilege asks *"now that code is here, what can it reach?"* — and the corpus's answer for production IVI is: more than the model says. The three mechanisms recur because they are cheap to ship: declaring a permission is easier than assigning it a protection level correctly; checking a caller in the library is easier than checking it in the service; leaving the debug surface in is easier than maintaining a separate service build. Each is a case of the enforcement living one layer away from the resource it guards. Defence in this family is correspondingly unglamorous: protection levels audited against the resource, caller checks in the service (never the client), debug surfaces absent from production images, and parsers of untrusted media running at the lowest privilege the platform offers.

This page synthesizes the KB's own full entity pages named above and in its frontmatter. Its filing evaluation recorded it as the mining pass's weakest ADD, marked first-to-cut; it is built as scoped because the runtime family is real, distinct from the update path, and anchored by a complete case — but the page's brevity relative to its siblings honestly reflects the corpus's depth here.

## Related

- [BYD Dolphin hacking](../byd-dolphin-hacking.md) — the anchor case: three boundaries failing in sequence
- [MMI3G toolkit](../mmi3g-toolkit.md) — the designed-in script-execution surface
- [Q50 reverse engineering](../q50-reverse-engineering.md) — the privileged media parser
- [IVI update trust](ivi-update-trust.md) — the arrival path; this page is the runtime it arrives into
