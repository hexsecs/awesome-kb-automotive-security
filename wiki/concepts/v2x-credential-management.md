---
title: "V2X credential management"
summary: "How vehicles get pseudonymous credentials: split-knowledge issuance in the ETSI CCMS and US SCMS, so linking a ticket to an identity takes a quorum."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [vanetza, v2verifier, van3twin, f2md, misbehavior-detection, securing-vehicular-ad-hoc-networks, secure-vehicular-communication-systems-design-and-architecture, pseudonym-schemes-in-vehicular-networks-a-survey]
sources:
  - url: "https://www.etsi.org/deliver/etsi_TS/102900_102999/102941/02.01.01_60/ts_102941v020101p.pdf"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1109/TITS.2018.2797529"
    retrieved: 2026-11-01
  - url: "https://github.com/vanetza/vanetza"
    retrieved: 2026-11-01
---

A V2X station never speaks under its own name. It holds a long-term enrolment credential that it shows only to the credential system, and spends short-lived pseudonymous certificates — Authorization Tickets in the ETSI system, pseudonym certificates in the US one — on the air. Both systems (ETSI's CCMS: TS 102 940 architecture, TS 102 941 protocols, TS 103 097 formats; the US SCMS of Brecht et al., IEEE T-ITS 2018) resolve one contradiction: messages must be authenticatable, yet the certificate in them must let no observer track the vehicle; a misbehaving device must be identifiable *to the system* and cut off, yet no single authority may be able to identify it. The threat model includes the authorities themselves — the SCMS is "designed such that at least two of its components need to collude to gain meaningful information for tracking a device". The structural answer both converged on is split knowledge: what is needed to link a pseudonym to an identity is divided across independent authorities, so linking is possible only as a quorum act (investigation, revocation), never a unilateral one (tracking).

## Two credentials

The **enrolment credential** (ETSI EC; the SCMS's enrollment certificate, "like a passport") binds a station's enrolment key to its registered identity. In ETSI form it carries a unique name and permissions only to sign certificate requests — it talks to the PKI, never to other vehicles — and runs to three years under the EU Certificate Policy. The **short-term credential** (ETSI Authorization Ticket; SCMS pseudonym certificate) binds a fresh key to service permissions and nothing else: the ticket's certificate `id` is literally *none* — it is nameless. EU policy caps ticket validity at one week, preloading at three months, and parallel tickets at 60 per vehicle, that last figure an explicit Sybil bound; the ETSI specifications set no lifetimes themselves — every number is policy. The SCMS design lands in the same place: one-week validity, at least 20 certificates valid simultaneously, one to three years of supply — simultaneity deliberate, since a concurrently valid batch lets each device choose its own change pattern instead of wearing a linkable time slot. (The 2018 design's parameters; operation today runs under IEEE 1609.2.1-2022 as profiled by the SCMS Manager.)

## Who knows what

ETSI splits the credentials' *issuance*: the **Enrolment Authority** authenticates the station and issues its enrolment credential; the **Authorization Authority** issues its tickets. TS 102 941 states the reason as a knowledge rule — privacy is "provided by the separation of the duties": the EA knows who the station is but not which tickets it holds; the AA issues tickets without learning who asked. One operator may run both roles, but then it "shall guarantee privacy… to avoid re-identification of pseudonym certificates". Stations without privacy requirements (roadside units) get an explicit no-privacy profile instead. The SCMS splits *issuance knowledge* over more parties: the **Registration Authority** validates requests against the enrollment certificate and knows which device asked, but never sees the finished certificates; the **Pseudonym CA** signs the certificates but receives requests shuffled, one at a time, from many devices, and never learns whose they are; two **Linkage Authorities** each contribute half of every certificate's linkage value, so neither can link anything alone. A Location Obscurer Proxy strips network identifiers from requests — split cryptography over a stable IP address would be theatre.

## Asking without naming yourself

The ETSI authorization protocol is the split made mechanical. The station generates fresh keys, computes a `keyTag` — an HMAC over the new public keys under a random key — and signs the shared part of the request (EA identity, keyTag, requested permissions) with its enrolment key, that signature then *encrypted to the EA*. The AA receives the keys and the sealed signature: via the HMAC it can verify the keys it is asked to certify are the keys the request was signed over, but it cannot open the proof of who asked. It forwards only the shared part and the sealed signature to the EA, which validates the station's status and profile *without seeing the ticket keys* — "the EA is not able to draw conclusions on the keys requested by the ITS-S" — and returns the confirmed attributes the AA must issue within. The station must also change its network-layer identifiers before each request. The SCMS reaches the same shape with butterfly key expansion: the device uploads one seed key pair per batch; the RA expands it into per-certificate *cocoon* keys; the PCA blinds each with its own random value before signing, and the device reconstructs the final private keys — the blinding being what stops the RA recognising its own expansions on the air. ETSI specifies a butterfly variant of its own, run through the EA.

## Trust lists, and revocation that respects the split

Stations learn whom to trust from signed lists, bootstrapped from anchors provisioned at manufacture. The ETSI model has two Certificate Trust Lists, not interchangeable: the Trust List Manager's (in Europe, the ECTL) lists the domain's trusted **Root CAs**, admitted only after audit and policy approval; each Root CA's own CTL lists its Enrolment and Authorization Authorities. A Root CA's CRL covers **CA certificates only** — no end-entity credential ever appears on a published list. Revocation of stations is asymmetric by design, in three tiers. Tickets are **never revoked**: short life plus passive revocation — a compromised station is "evicted from the ITS network by not reissuing them" new tickets. Enrolment credentials are revoked on the EA's internal blacklist, which is **never published**; the EA consults it at ticket-validation time, so blacklisting silently cuts off the ticket supply. Only the authority tier gets public revocation, via CRL and trust-list removal. The SCMS mirrors the split: future certificates stop at the RA's internal blacklist, while issued pseudonym certificates are killed through linkage values — each carries lv = plv1 ⊕ plv2, from each Linkage Authority's secret hash chain, and the CRL publishes only the device's current-period seeds, from which receivers derive its current and *future* linkage values. Earlier periods cannot be derived from published seeds: revocation is forward-only, and a revoked device's past stays unlinkable. This is where [misbehavior detection](misbehavior-detection.md) lands: its revocation outcomes can only bite through these channels.

## Pseudonym change strategies

Holding short-lived tickets is only half the privacy design; the other half is *when and how* a station switches pseudonyms — the subject of the [pseudonym schemes survey](../pseudonym-schemes-in-vehicular-networks-a-survey.md) (Petit et al., COMST 2015). An observer links successive pseudonyms by timing, position, and trajectory continuity, so a strategy is a bet about which signal the change breaks:

- **Fixed-interval / periodic** — change on a schedule. Predictable is the flaw: an observer who knows the period still correlates by kinematics.
- **Random / distance-based** — change at randomised intervals or distances, decorrelating the change moment from any shared clock.
- **Silent periods** — stop transmitting briefly around the change, so no beacons bridge old and new identifiers. The strongest simple unlinkability lever — and a safety trade: a silent vehicle is invisible, for that interval, to the applications pseudonyms exist to serve.
- **Vehicle-centric / context-aware** — change when the local situation favours confusion (manoeuvres, intersections, speed changes), spending changes where they buy most.
- **Density-based / cooperative** — change *with* neighbours: simultaneous changes create a crowd to hide in; **mix-zones** (declared regions where all stations change) formalise the crowd. The dual limit: in sparse traffic there is no crowd, and a lone change is linkable almost by definition.

Two consequences bind this to the rest of the page. Strategies consume the credential supply at different rates — a density-hungry strategy burns tickets faster — an issuance input, not a detail. And change policy is [misbehavior detection](misbehavior-detection.md)'s starvation problem from the other side: F2MD's experiment (a periodical policy starving its report counts) is the taxonomy meeting the authority loop. Issuance, change strategy, and detection are one system in three documents that rarely cite each other.

## Who implements what

Across this KB's V2X entries, credential management exists only as an assumption. [Vanetza](../vanetza.md) implements the TS 103 097 message-security layer and a `certify` tool that fabricates certificates and tickets locally; its own gap list states there is no support "to request authorization tickets from an authorization authority or to do an enrolment", and no CRL checks. [V2Verifier](../v2verifier.md) verifies 1609.2 certificates over real radios; issuance is out of its scope. [VaN3Twin](../van3twin.md) models certificate-shaped containers, no authority behind them. [F2MD](../f2md.md) has no PKI at all — synthetic-integer pseudonyms — which is complementary rather than approximate: it studies what pseudonym change does to detection by abstracting the credential system away. The machinery on this page is, relative to the KB, specification without an implementation.

This page synthesizes ETSI TS 102 941 V2.1.1 (read firsthand; a V2.2.1 exists, undiffed), the EU C-ITS Certificate Policy Release 1 (its ticket numbers are Release 1 values, two marked TBD in the document itself), Brecht et al.'s SCMS design paper, and SCMS Manager's public documents.

## Related

- [Vanetza](../vanetza.md)
- [V2Verifier](../v2verifier.md)
- [VaN3Twin](../van3twin.md)
- [F2MD](../f2md.md)
- [Misbehavior detection in V2X](misbehavior-detection.md)
