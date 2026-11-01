---
title: "Misbehavior detection in V2X"
summary: "Why V2X needs a layer beyond signatures: detecting false content from validly credentialed stations, reporting it, and the authority that decides."
type: concept
updated: 2026-11-01
related: [f2md, vanetza, v2verifier, artery, veins, van3twin, v2x-credential-management]
sources:
  - url: "https://github.com/josephkamel/F2MD"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1109/TVT.2020.2984878"
    retrieved: 2026-11-01
  - url: "https://www.etsi.org/deliver/etsi_tr/103400_103499/103460/02.01.01_60/tr_103460v020101p.pdf"
    retrieved: 2026-11-01
  - url: "https://www.etsi.org/deliver/etsi_ts/103700_103799/103759/02.02.01_60/ts_103759v020201p.pdf"
    retrieved: 2026-11-01
---

V2X message security proves who sent a message and that it arrived intact. Misbehavior detection asks a different question: whether what the message says is true. The two are separate layers by definition — ETSI TS 103 759 defines a misbehaving entity as a station "sending false or misleading messages **using valid certificates**", faulty stations included alongside attackers. The standards split the work accordingly: detection mechanisms are the subject of ETSI TR 103 460, a pre-standardization study, while TS 103 759 — the *Misbehaviour Reporting* service — standardizes reporting and the authority architecture, not the detectors.

## Three layers, three questions

**Message security** answers "who sent this, and is it intact?" Signing and verification under the V2X PKI (TS 103 097 in [Vanetza](../vanetza.md), IEEE 1609.2 in [V2Verifier](../v2verifier.md)) establish authenticity, nothing about content.

**Detection** answers "is the content consistent with the world?" ETSI's study is blunt: "PKI based security would not be able to prevent such data semantic level attacks" (TR 103 460). Local detectors check messages against the receiver's perception of ground truth (TS 103 759) — a credentialed station with a failed sensor produces perfectly signed falsehoods that only plausibility checking can catch.

**Reporting and the authority** answer "what happens to that sender?" A local suspicion is not a verdict: TS 103 759's reporting service exists "for the reporting of local misbehaviour detections to a central authority (Misbehaviour Authority), which collects reports from different ITS stations for global analysis and reaction". Detection is local and immediate; judgement is central and slow — and most of this page's open problems live in that separation.

## The chain, as implemented once

[F2MD](../f2md.md) is, to this KB's knowledge, the only artefact implementing the whole chain. **Checks** are data-centric and per beacon: each beacon scores plausibility factors rather than passing or failing — binary in the legacy check set, error-tolerant scores in [0,1] from the value ± its advertised confidence in the CaTCh set (IEEE WCNC 2019). The families: range, position and speed plausibility; position, speed, position–speed and heading consistency; beacon frequency; intersection (two stations claiming one place); sudden appearance; Kalman tracking. **Investigation** turns factors into a report decision per sender pseudonym: threshold and aggregation rules, a behavioural variant keeping per-pseudonym trust state, and a machine-learning variant shipping check factors to a Python model server. **Reports** follow the three-container design (header, source, evidence) of the authors' VNC 2018 reporting protocol, in four forms of increasing weight — check results only; the single offending beacon; an evidence history of up to 30 beacons; the protocol form pairing beacons with their checks — throttled to one report per pseudonym per behaviour window. **The authority**, in F2MD, is where honesty is required: the shipped server decides by report count (a pseudonym is predicted a local attacker past five reports; reaction levels escalate through warning, ticket, passive revocation, active revocation), and the anchoring paper (Kamel et al., IEEE TVT 2020) calls its own method "a simple non intelligent method that has a threshold on the number of reports". The DARE dataset (IEEE VTC 2020) exists because the real authority problem is open: it publishes F2MD-generated reports as shared evaluation data for global detection.

## The authority in the two credential systems

In the ETSI architecture (TS 103 759), the backend Misbehaviour Authority determines the response — revocation of a certificate is the named example — with optional pre-processing for reporters' privacy and a separate Remediation component for non-revocation responses. Reports must carry evidence the authority can verify independently: the original received message and the indications of the detectors that fired, the message arriving with its Authorization Ticket, so a report indicts a credential rather than telling a story. And a normative constraint shapes everything: the design shall be such that "the MA is unable to link the short term and the long-term identities of the reported ITS-S and of the reporting ITS-S".

The US SCMS makes the same component central: its Misbehavior Authority contains Global Misbehavior Detection and the CRL Generator, deciding revocation over collected reports. The rationale for a global stage is stated by ETSI's study: "local detection only provides limited information in time and space", which "may be insufficient to identify an attack or an attacker in a reliable manner". The privacy constraint is met institutionally: linkage values are split across two Linkage Authorities, so linking a pseudonym certificate to its enrolment certificate — the act revocation requires — needs several SCMS components to collaborate; no single one can do it alone.

## Who implements what

Of this KB's V2X entries, only [F2MD](../f2md.md) implements detection at all. [Vanetza](../vanetza.md) is message security only — it signs and verifies, has no opinion on whether a message is true, and by its own stated gaps does not even check revocation lists. [V2Verifier](../v2verifier.md) verifies 1609.2 signatures over real radios — authenticity, not plausibility. [Artery](../artery.md) ships no detection tooling (detectors in Artery studies are the studies' own), [VaN3Twin](../van3twin.md) states that nothing in it performs misbehavior detection, and [Veins](../veins.md) core has no security layer — it is the testbed on whose fork F2MD's chain is built. The split is what their own scopes describe.

## Open problems the sources name

**False positives are structural.** TR 103 460: "Denigration of benign ITS stations cannot be circumvented (risk of false positive)" — and the downstream act is revocation of a vehicle's credentials, so the same study assigns the authority the job to "distinguish between false positive and genuine reports". The reporting channel itself can be attacked: an IEEE ICC 2021 paper anchored at V2Verifier targets discreditation — the reporting process used against a victim.

**Privacy and revocation pull against each other.** Revocation is impossible without some link between pseudonyms and long-term identity; privacy requires that no single party hold it. Both systems answer with split trust (the MA-unlinkability rule above; the SCMS's split linkage authorities), making the authority a multi-party institution rather than a server.

**The loop is slow on purpose.** Reports are store-and-forward: "A vehicle does not wait for a decision response about the reported ITS-S from the MA" (TS 103 759), and the standard's delivery envelope runs to workshop visits. Detection plus revocation is therefore a fleet-hygiene loop — evict bad credential holders eventually — not a collision-avoidance input; a receiver's immediate safety decision can only rest on its own local plausibility judgement.

**Pseudonymity starves naive detection.** Every layer of F2MD's chain keys on the pseudonym — check history, behavioural trust, report counts — and its own experiment shows the consequence: with a periodical pseudonym-change policy, "the MA does not receive enough reports with the same reported ID, certainly affecting the detection quality". The paper's conclusion is that evidence-bearing reports make count-based global detection obsolete; the authority that replaces it is the field's open problem.

This page synthesizes the KB's V2X entity pages and the primary sources in its frontmatter, including a firsthand read of the F2MD code and its anchoring paper's full text.

## Related

- [F2MD](../f2md.md)
- [Vanetza](../vanetza.md)
- [V2Verifier](../v2verifier.md)
- [Artery](../artery.md)
- [Veins](../veins.md)
- [VaN3Twin](../van3twin.md)
- [V2X credential management](v2x-credential-management.md)
