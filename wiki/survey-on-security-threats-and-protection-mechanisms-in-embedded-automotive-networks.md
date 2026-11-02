---
title: "Survey on Security Threats and Protection Mechanisms in Embedded Automotive Networks"
summary: "Studnia et al., DSN Workshops 2013. Widely cited survey mapping in-vehicle protocols, the threats against them, and candidate countermeasures."
type: entity
category: "Research Papers"
url: "https://ieeexplore.ieee.org/document/6615528/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Studnia et al., DSN Workshops 2013. Widely cited survey mapping in-vehicle protocols, the threats against them, and candidate countermeasures."
related: [security-in-automotive-bus-systems, experimental-security-analysis-of-a-modern-automobile, comprehensive-experimental-analyses-of-automotive-attack-surfaces]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://hal.science/hal-01176042"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1109/DSNW.2013.6615528"
    retrieved: 2026-11-01
---

Studnia et al., DSN Workshops 2013. Widely cited survey mapping in-vehicle protocols, the threats against them, and candidate countermeasures.

## What it is

Ivan Studnia and Youssef Laarouchi (Renault S.A.S.) with Vincent Nicomette, Eric Alata, Yves Deswarte, and Mohamed Kaâniche (LAAS-CNRS / University of Toulouse). *2nd Workshop on Open Resilient Human-aware Cyber-Physical Systems* (WORCS-2013), co-located with the 43rd IEEE/IFIP International Conference on Dependable Systems and Networks (DSN-2013), Budapest, June 2013; published in the DSN Workshops proceedings, pp. 1–12. DOI: [10.1109/DSNW.2013.6615528](https://doi.org/10.1109/DSNW.2013.6615528) (verified via api.crossref.org). The open author manuscript (HAL hal-01176042) was read in full for this page. It is a survey, not an experiment: its contribution is organisation — a protocol inventory, a threat taxonomy, and a classification of the countermeasures then being devised — built largely on the experimental results of [Koscher et al. 2010](experimental-security-analysis-of-a-modern-automobile.md) and Checkoway et al. 2011, which it cites throughout as its evidence base. The work was partly supported by an ANRT CIFRE arrangement (a Renault-linked doctoral programme).

## What it showed

**The baseline (§II).** A modern car of the survey's moment carries 30–70 ECUs on several subnetworks joined by gateway ECUs. The protocol inventory: CAN (up to 1 Mb/s, CSMA/CD with identifier arbitration; the most used protocol, and the focus of most studies), LIN (master–slave, up to 20 kb/s, comfort functions), FlexRay (up to 10 Mb/s, intended to enable X-by-wire, its adoption hindered by cost), MOST (optical multimedia, up to 24 Mb/s), and Ethernet — "the use of Ethernet in the automotive context is being considered in a near future," a sentence that dates the survey precisely. Protocols are tabulated against the SAE class A–D scheme, and the car's external connections (USB, Bluetooth, WiFi, 3G/4G, future V2V/V2I) are mapped in a figure taken from Checkoway et al. 2011.

**Attack goals (§III-A).** Six motivations: *theft*; *electronic tuning* — the attacker is the owner (lowering mileage, engine tuning, unapproved programs, or bypassing authentication to fit cheap aftermarket ECUs), whose consequences the authors note can still reach safety; *sabotage*, from a locked air conditioner to non-responding brakes; *intellectual property theft* (bus eavesdropping to map frame semantics, ECU source recovery, counterfeit ECUs); *privacy breach* (phone directories, call history, GPS history); and *intellectual challenge*. Attacker profiling is borrowed from Brooks et al. 2009 and from Wolf et al. 2007; Verendel et al.'s proposal to run honeypots in in-vehicle networks is noted.

**CAN's five missing properties (§III-B1).** The survey's most-quoted analytical move: CAN by itself cannot guarantee *confidentiality* (every frame is broadcast), *authenticity* (a frame carries no field identifying its sender), *availability* (arbitration makes flooding denial of service easy), *integrity* (the CRC detects transmission errors but is trivially forged for a fake message), or *non-repudiation* (no way to prove a node did not send a message).

**Local attacks (§III-B2).** The OBD port as a plug-in entry point (dongles legally bought by anyone); black-box learning of frame meanings; replay and masquerade; reflashing ECUs through the network; Nilsson and Larson's "automotive virus" triggered by a chosen frame. The cross-segment problem — the target ECU may not sit on the attacker's bus — was solved by Koscher et al., who reprogrammed gateway ECUs so a node on a low-speed, non-critical bus could send frames on the safety-critical high-speed bus. The survey's conclusion: controlling a single node can yield control of any ECU. It also records the standing objection fairly: these attacks presuppose physical access, and quicker non-electronic routes to the same damage may exist.

**Remote attacks (§III-C)**, sorted by range, following Checkoway et al.'s own organisation. *Indirect physical:* the compromised PassThru device, which emitted malicious packets into every car it serviced and could spread to identical devices on the same WiFi network; the CD player's firmware-update trick and WMA exploit; USB scenarios (devised, not yet reported). *Short range:* Bluetooth pairing and stack exploitation; car-to-car communications risk; TPMS eavesdropping from up to 40 metres plus spoofed warnings (Rouf et al. 2010); KeeLoq breaks; and the PKES relay attack (Francillon et al. 2011 — ten car models, keys 50 metres away). *Long-range direct:* telematics-unit code execution over the 3G network (Checkoway et al.); in-car web browsing as a prospective surface. *Long-range indirect:* a trojaned app from a manufacturer app store, and RDS "side channel triggers" activating backdoors across a fleet of previously infected vehicles — a scenario the survey takes from Checkoway et al. and labels hypothetical.

**Constraints first (§IV-A).** Before mechanisms, the survey lists the design constraints it attributes to Wolf et al. 2007: limited ECU hardware against an unconstrained attacker; real-time deadlines; autonomy (the driver must not be the security operator); physical environment; a vehicle lifecycle of about twenty years, so mechanisms must be updatable to avoid obsolescence; and compatibility — retrocompatibility with deployed technology plus interoperability between models.

**Protection mechanisms (§IV).** For external communications, many surveyed attacks trace to poor implementation or non-compliance with existing specifications; the large European projects SEVECOM, PRESERVE, EVITA, and OVERSEE are named as the industrial-academic response. Internal protections fall into **three categories** — the classification this survey fixed in the literature:

1. *Cryptographic solutions* — authenticate or encrypt bus traffic. The cost is computation against real-time limits; the EVITA project's Hardware Security Module (three variants matched to ECU requirements) is presented as the offload answer, with an HSM-based key-exchange and encryption design as the worked example.
2. *Anomaly detection* — from a module that mutes an ECU emitting frames too fast, to Müter et al.'s scheme binding each frame identifier to its one legitimate sender (a node that hears its own identifier emitted by someone else raises a high-priority alert frame), to binary tainting that tracks the origin of malicious instructions (noted as resource-consuming). Intrusion detection is split signature-based — Müter et al.'s eight CAN sensors (Formality, Location, Range, Frequency, Correlation, Protocol, Plausibility, Consistency) — versus anomaly-based, exemplified by entropy-deviation detection. The survey's IDS verdict is deliberately hedged: "still early proofs of concept," and a car cannot refresh a signature base as often as a computer, while automatic handling of a false positive could itself endanger passengers.
3. *ECU software integrity* — secure-boot analogues anchored in a trusted base (EVITA HSM or a TPM), and the OVERSEE design: a hypervisor isolating the multimedia ECU's critical software (allowed to write on the buses) from untrusted communication interfaces in separate virtual machines, so a wireless exploit does not become bus access.

The conclusion restates the three aspects — encryption of communications, anomaly detection, integrity of the embedded software — and closes on intensity, not resolution: manufacturer and academic work is "really intense," with "still many work to do."

## Where it fits

The organisational complement to the KB's two founding CAN-era pages. [Wolf et al. 2004](security-in-automotive-bus-systems.md) analysed what bus architecture permits on paper; [Koscher et al. 2010](experimental-security-analysis-of-a-modern-automobile.md) showed what production cars actually allowed. Studnia et al. 2013 is the moment the young field got its map: it cites Wolf 2004 for the bus vulnerabilities and takes Koscher 2010 and Checkoway 2011 as the demonstrated-attack record, then organises both into goals, vectors, and a three-family countermeasure scheme (cryptography / anomaly detection / software integrity) that the KB's later pages keep instantiating — message authentication, the CAN-IDS line, and secure-update work respectively. Its CAN property list is the survey-form of the same substrate facts the Koscher deep page establishes experimentally.

## Limits and safety notes

A survey of other people's work: no new experiments, and its attack narrative leans heavily on one research group's pair of papers. The authors disclaim comprehensiveness in the text ("this survey makes no claim of comprehensiveness"), pointing readers to Kleberger et al. and Wolf et al. 2007 for more. Countermeasures are sketched from the cited works, never benchmarked or evaluated against the survey's own attack catalogue. Every claim is 2013 state of the art and must be read as such: Ethernet is a near-future consideration, V2V is "in a few years probably," MOST and FlexRay are live contenders, and automotive IDS is explicitly proof-of-concept. Read it as the field's self-portrait at that date, not as present fact.

## Status and sources

Status: **published** — a finished 2013 workshop publication; no living artefact. Sources: the paper (open author manuscript, HAL hal-01176042), read in full 2026-11-01; the DOI record (Crossref); the list.

## Related

- [Security in Automotive Bus Systems](security-in-automotive-bus-systems.md)
- [Experimental Security Analysis of a Modern Automobile](experimental-security-analysis-of-a-modern-automobile.md)
- [Comprehensive Experimental Analyses of Automotive Attack Surfaces](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md)
