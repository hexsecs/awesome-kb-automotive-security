---
title: "Uptane: Securing Software Updates for Automobiles"
summary: "Kuppusamy et al., escar Europe 2016. Extends TUF with a director role, supplier-delegated image signing, and ECU-signed vehicle version manifests, so that a…"
type: entity
category: "Research Papers"
url: "https://uptane.org/papers/kuppusamy_escar_16.pdf"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Kuppusamy et al., escar Europe 2016. Extends TUF with a director role, supplier-delegated image signing, and ECU-signed vehicle version manifests, so that a partial compromise of the update system does not by itself let an attacker push malicious firmware to every ECU."
related: [secure-firmware-updates, uptane]
sources:
  - url: "https://uptane.org/papers/kuppusamy_escar_16.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
---

Kuppusamy et al., escar Europe 2016. Extends TUF with a director role, supplier-delegated image signing, and ECU-signed vehicle version manifests, so that a partial compromise of the update system does not by itself let an attacker push malicious firmware to every ECU.

## What it is

The original Uptane design paper: Trishank Karthik Kuppusamy, Akan Brown, Sebastien Awwad, Damon McCoy, and Justin Cappos (NYU Tandon); Russ Bielawski and Sam Lauzon (University of Michigan); Cameron Mott (Southwest Research Institute); and André Weimerskirch (Michigan / Lear Corporation). Presented at the 14th escar Europe, 2016, supported by US Department of Homeland Security grants and developed in consultation with US automotive industry stakeholders. The artefact it became — the versioned Uptane Standard and its governance — has its own entity page at [Uptane](uptane.md), and the design as standardised is treated on the [secure firmware updates](concepts/secure-firmware-updates.md) concept page; where the paper and the later standard differ, the differences are flagged below rather than smoothed over.

## What it showed

Earlier update security — signatures plus an HSM — prices in no compromise at all. The threat model names four attacker goals (read updates, deny updates, deny functionality, control the vehicle) and ten attacks: eavesdrop, drop-request, slow retrieval, freeze, partial bundle installation, rollback, endless data, mixed-bundles, mix-and-match, and arbitrary software installation. (Availability against drop-request attacks is explicitly not guaranteed.) The method: take TUF (root / timestamp / release / targets roles, threshold signatures, key revocation, offline keys), build a "strawman" straightforward automotive adaptation, show by capability tables that it still fails — a man-in-the-middle inside the vehicle who has compromised *no keys at all* can still break it, with no secure recovery — then add the features that close the gaps.

**What the strawman already adds to TUF.** A **director role**: a server-side role acting like a package manager for one vehicle at a time. The vehicle identifies itself by VIN; the director consults an inventory server for the vehicle's ECUs and freshly signs instructions binding each ECU's unique serial number to the filename and hash of the image it must install — so instructions cannot be replayed to a different vehicle, and a faulty version can be blacklisted instantly. And **delegation**: the targets role delegates signing for suppliers' images, in three patterns — the OEM signs on a supplier's behalf, the supplier signs its own images, or the supplier sub-delegates to developer roles it can re-staff without the OEM changing anything. ECUs are split into one **primary** (downloads, verifies, distributes) and **secondaries**, with two verification tiers: **full verification** (all TUF-role metadata plus the director's; the image hash must match in *both* — neither role alone can push an image) and **partial verification** (director metadata only). By default the director cannot instruct an ECU to replace its image with an older version number; overriding that is left to a separate deployment document. ECUs that can perform neither tier, the conclusion insists, should not be remotely updated at all.

**The four Uptane features (the paper's §5.3).** (1) *Additional storage* — A/B images, or at least room for a delta — so an endless data attack cannot leave an ECU with no bootable image. (2) *Broadcast metadata* — the primary must deliver the same metadata to all secondaries at the same time, defeating mixed-bundles attacks. (3) *Vehicle version manifest* — after installing, every ECU attests what it has installed by signing the hash of its installed image with a symmetric key provisioned by the OEM at manufacture, once per ignition cycle; the primary aggregates these into a manifest for the director, so the director can *detect* ("detected, if not prevented") partial bundle installations instead of trusting the primary's summary. (4) *Time server* — because ECUs lack reliable clocks, each ECU periodically refreshes its time: nonces go via the primary to an external time server, which signs the current time against each nonce; the bootloader verifies the signature once per ignition cycle, making metadata-expiry checks meaningful and bounding freeze attacks by metadata expiry.

**The compromise ladder (§5.4, the design team's own analysis).** With all features in place: a man-in-the-middle with no keys gets eavesdropping (only if the channel is unencrypted) and drop-request, nothing more. Director keys alone buy mix-and-match of *valid, signed* images — not arbitrary software, which still needs targets-side signatures. Adding timestamp/release/director keys allows arbitrary combination of targets metadata, bounded by expiry. Adding a *supplier's* keys enables rollback and arbitrary software, but only for ECUs whose images that supplier signs. Root keys buy an indefinitely long freeze, not code execution. The sharpest asymmetry: if the *primary* is compromised together with the director keys, rollback and arbitrary software reach **all partial-verification secondaries on all vehicles**, while full-verification secondaries still require the relevant supplier's keys.

## Where it fits

This is the design paper behind the KB's [Uptane](uptane.md) entity page: same project, earlier stratum. Read against the [secure firmware updates](concepts/secure-firmware-updates.md) concept page (the design as standardised), the 2016 paper differs in specific ways. *Roles:* the paper's "release" role is what the standard calls **Snapshot**. *Structure:* in the 2016 text the director is an added **role** working with an inventory server; the standard's split into two repositories — a per-vehicle **Director repository** (online keys) and an authoritative **Image repository** (offline keys) — is the later framing, not the paper's diagram. *Time and manifest:* the paper's dedicated nonce-based time-server protocol is not a named element of the standard as the concept page describes it, and its symmetric-key (OEM-provisioned) manifest is the ancestor of the standard's per-ECU signed manifest, not a contradiction. The version line belongs entirely to the later artefact: **IEEE-ISTO 6100.1.0.0 (2019)** is Uptane Standard v1.0.0 — the 6100 number attaches to that 2019 edition only, and the 2016 paper predates every standard edition (current: v2.1.0, 2023).

## Limits and safety notes

As the paper presents itself: this is a design and analysis paper — no implementation, no performance measurements, and no deployment are reported; the security claims rest on the authors' own capability/attack tables (§§4.5, 5.4), not on external evaluation. The four §5.3 features are formally optional — "an OEM is free to choose and apply some and not all of these features" — with the authors strongly recommending all of them; a partial adoption does not inherit the full ladder. Several defences are detection or time-bounding rather than prevention (manifest detection; expiry-bounded freeze; drop-request attacks cannot be prevented at all). And the paper's own scope line, which the concept page repeats for the standard: Uptane secures *delivery*, not package content — a malicious but legitimately signed image, and build-system compromise, are out of scope by design.

## Status and sources

Status: **unknown** — a finished 2016 conference paper; the artefact is tracked on the [Uptane](uptane.md) page (maintenance). Bibliographic record: 14th escar Europe 2016 (venue stated in the paper's own footnote). **DOI: none** — no Crossref record exists for the escar paper (checked 2026-11-01); DOI 10.1109/MVT.2017.2778751 belongs to a different, later (2018) publication by overlapping authors and must not be attached. Full text at uptane.org; read in full 2026-11-01.

## Related

- [Uptane](uptane.md)
- [Secure firmware updates](concepts/secure-firmware-updates.md)
