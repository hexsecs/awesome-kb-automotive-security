---
title: "Secure firmware updates (Uptane)"
summary: "How Uptane secures vehicle software updates: two repositories, per-vehicle signed instructions, and compromise resilience when servers or keys fall."
type: concept
updated: 2026-11-01
related: [uptane, uptane-securing-software-updates-for-automobiles, simos18-sboot, tc1791-can-bsl, medc17-checksum-tool, uds-seed-key]
sources:
  - url: "https://uptane.org/docs/latest/standard/uptane-standard"
    retrieved: 2026-11-01
  - url: "https://uptane.org/papers/kuppusamy_escar_16.pdf"
    retrieved: 2026-11-01
  - url: "https://theupdateframework.github.io/specification/latest/"
    retrieved: 2026-11-01
  - url: "https://uptane.org/learn-more/design"
    retrieved: 2026-11-01
  - url: "https://uptane.org/learn-more/adoptions"
    retrieved: 2026-11-01
  - url: "https://uptane.org/docs/latest/all-versions"
    retrieved: 2026-11-01
---

A vehicle that receives software over the air has a second attack
surface beside the software itself: the delivery system. Whoever
controls what an ECU installs controls the ECU, so the update
mechanism has to survive compromise of its own servers and keys.
[Uptane](../uptane.md) is the automotive adaptation of The Update
Framework (TUF) built for that assumption: no single compromised
repository, key, or ECU suffices to push software to a vehicle.

## Threat model

The Standard's attacker is strong and specific: a man-in-the-middle on
traffic outside the vehicle and on its buses, able to compromise
*either* the Director *or* the Image repository — and *either* a
Primary *or* a Secondary ECU — but not both of a pair. Breaching the
mechanism should require compromising two or more modules. The
Standard names the attacks the design must defeat:

- **Rollback** — install a previously valid but older image with known
  vulnerabilities. Countered by monotonic version checks at every
  metadata layer and a per-image release counter that must never
  decrease, which holds even if the Director is compromised.
- **Freeze** — keep serving a properly signed but old bundle while
  newer updates exist. ECUs lack reliable clocks, so the design gives
  them a secure source of time and makes expiry checks mandatory.
- **Mix-and-match** — combine individually valid images into a bundle
  whose parts do not interoperate. Countered by the Snapshot role
  pinning one consistent set of metadata, and by full verification.
- **Partial bundle installation** — install a valid bundle, then block
  selected updates inside it. The same end state can happen by power
  loss mid-update; the vehicle version manifest detects it either way.

The boundary is stated plainly: Uptane secures *delivery*, not package
content. Malware in a legitimately signed package and build-system
compromise are explicitly out of scope; what the OEM gets against a
*faulty* release is control — the Director can blacklist a bad version
immediately and resolves dependencies before instructing a vehicle.
One mirror scenario is also out of scope (substituting packages with
matching version numbers), so "defeats malicious mirrors" is more
than the Standard claims.

## The design

Uptane keeps TUF's four metadata roles, on each of two repositories.
**Root** is the repository's certificate authority, its keys kept
offline. **Targets** signs metadata *about* images — hashes and sizes,
not the images themselves — and can delegate signing for a subset of
images to their supplier. **Snapshot** signs the version numbers of
all Targets metadata, pinning one consistent set (the 2016 paper calls
this role "release"). **Timestamp**, the one online role, periodically
signs a hash of Snapshot so replayed metadata is detected. Thresholds
apply throughout: roles can require several keys to sign.

The two-repository split is Uptane's main structural addition. The
**Image repository** is the authoritative inventory of every deployed
image, run at human pace with **offline keys**; suppliers upload there
under delegation. The **Director repository** is the per-vehicle
instructor: automated, with **online keys**, it consults a private
inventory database of vehicles, ECUs, and installed revisions, and
generates fresh Targets metadata for one vehicle at a time — each
image tagged with the ECU that should install it, no delegations
permitted. The Director decides *what this vehicle installs now*; the
Image repository attests *what legitimately exists*.

Before an update cycle the Primary collects a **vehicle version
manifest**: one report per ECU, each signed with that ECU's own key
and carrying its identifier, the hash of its installed image, an
attack-detected indicator, and a nonce. The Director cross-checks the
manifest against its inventory database, so it learns what is
*actually* installed — detecting partial installations and attack
aftermath — rather than trusting the Primary's summary.

Verification is tiered to what ECUs can run. A Primary **shall**
perform **full verification**: the Director's Targets metadata for an
image must match the Image repository's, including shall-match fields
such as hardware identifier and release counter — so a compromised
Director cannot order an ECU to install incompatible firmware. A
Secondary that cannot manage that **shall** at least perform
**partial verification**: check the time, then verify the Director's
Targets signature. The floor is sharp: an ECU that performs no
verification cannot be updated over the air at all.

## Compromise resilience

The 2016 paper prices in compromise rather than assuming it away; this
ladder is the design team's own analysis, reported here as such.
Director keys alone expose a vehicle to mix-and-match of *valid,
signed* images — not arbitrary software, which still needs
Image-repository signatures. Adding Timestamp and Snapshot keys allows
arbitrary combination of Targets metadata. Adding a *supplier's* keys
enables rollback and arbitrary software, but only for ECUs whose
images that supplier signs. Even Root keys buy only an indefinite
freeze, not code execution. Each rung is scoped; none is total.

## Deployment reality

Uptane was first published as IEEE-ISTO 6100.1.0.0 in 2019; the
current version is 2.1.0 (2023), maintained under the Linux
Foundation's Joint Development Foundation — the 6100 designation
belongs to the 2019 edition only. The project's Adoptions page names
Automotive Grade Linux (via aktualizr), HERE OTA Connect, Airbiquity's
OTAmatic, Foundries.io (partial — its client removes Uptane checks),
and Torizon. That record is thin at the OEM level: it names **no
automaker, vehicle model, or production deployment**, and its
"millions of vehicles" line is forward-looking phrasing, not a count.

UNECE Regulation No. 156 obliges manufacturers to run an auditable
software update management system (SUMS) and to keep type-approved
software identifiable via RXSWIN. Uptane fits only the
delivery-protection layer of that regime: it is not an RXSWIN system,
discharges none of R156's organisational obligations, and no source
consulted states it is required or endorsed under R156.
Complementary, not equivalent.

## The failure side

This KB's Firmware section documents what happens when boot security
is built from weaker parts. On [Simos18](../simos18-sboot.md), the
supplier boot stage that verifies signed firmware was defeated without
breaking any signature — a by-design PWM backdoor, a Mersenne
Twister-class seed/key challenge, and a CRC bounds-check flaw. A boot
chain is only as strong as its least-protected stage: the HSM-backed
application bootloader held; the stage beneath it, guarded by a CRC
and a weak PRNG instead of real cryptography, did not. The
[medc17-checksum-tool](../medc17-checksum-tool.md) page makes the
companion point: firmware checksums are algebraically recomputable,
so a modified image can always be made internally consistent again.
Checksums detect corruption; they cannot authenticate origin.
Authenticity needs a secret the attacker does not hold — signatures
over hashes, with keys distributed, thresholded, and revocable under
a framework. That is the gap Uptane's metadata roles exist to fill.

## Pages in this KB

- [Uptane](../uptane.md) — the framework's entity page (Security Analysis).
- [Uptane: Securing Software Updates for Automobiles](../uptane-securing-software-updates-for-automobiles.md) — the 2016 escar design paper (Research Papers).
- [Simos18_SBOOT](../simos18-sboot.md) — the failure case: a production signed boot chain failing link by link.
- [TC1791_CAN_BSL](../tc1791-can-bsl.md) — the loader that turns the Simos18 chain's access into flash read/write.
- [medc17-checksum-tool](../medc17-checksum-tool.md) — the checksum-versus-signature boundary, concretely.
- [UDS seed/key](uds-seed-key.md) — the challenge-response weakness class inside the Simos18 chain.
