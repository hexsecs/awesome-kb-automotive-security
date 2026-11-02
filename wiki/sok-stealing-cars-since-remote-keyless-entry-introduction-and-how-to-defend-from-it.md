---
uid: 01a19d3c-afd9-7a4d-869c-6dc9fa43859a
title: "SoK: Stealing Cars Since Remote Keyless Entry Introduction and How to Defend From It"
summary: "Bianchi et al., USENIX VehicleSec 2025. Systematization of RKE and passive keyless entry and start systems, covering their history, the attacks against…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/vehiclesec25/presentation/bianchi"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Bianchi et al., USENIX VehicleSec 2025. Systematization of RKE and passive keyless entry and start systems, covering their history, the attacks against them, and the defences."
sources:
  - url: "https://www.usenix.org/conference/vehiclesec25/presentation/bianchi"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - gone-in-360-seconds-hijacking-with-hitag2
  - dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer
  - lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems
  - fast-furious-and-insecure-passive-keyless-entry-and-start-systems-in-modern-supercars
  - rollback-a-new-time-agnostic-replay-attack-against-the-automotive-remote-keyless-entry-systems
  - key-fob-relay-attacks
  - my-other-car-is-your-car-compromising-the-tesla-model-x-keyless-entry-system
  - rolling-code-failure-classes
---

Bianchi et al., USENIX VehicleSec 2025. Systematization of RKE and passive keyless entry and start systems, covering their history, the attacks against them, and the defences.

## What it is

The first comprehensive systematization of knowledge (SoK) on remote keyless entry (RKE) and passive keyless entry and start (PKES) security (Bianchi, Brighente, Conti, Pavan — Padova/TU Delft). Where the KB's other keyless-entry pages each document one break, this paper assembles the whole field — from the 1981 Lipschutz patent and Renault's 1982 infrared remote to NFC cards, BLE phone keys, UWB digital keys, and cloud APIs — around four research questions: did the technology's evolution actually increase security (Q1); how did attack strategies evolve (Q2); are the published defences deployable and effective (Q3); what would an effective, secure remote entry system require (Q4)? The methodology is a systematization over the four top security venues plus high-practical-impact practitioner work (DEF CON, Black Hat) — more than 35 attacks since 2005 and 13 defences — scoped to what thieves can actually do: fixed-code attacks are excluded as trivial, so the study starts with rolling codes. The analysis rests on public information only, a stated limitation: manufacturers' systems are closed-source, so deployment claims are inferences, not audits.

## What it showed

**The legacy substrate.** RKE began as infrared, moved to RF (ASK/FSK; 315/433.94 MHz North America/Japan, 868 MHz Europe), with an RFID immobilizer as the second factor for starting. Static codes fell to trivial record-and-replay, so manufacturers adopted rolling codes: a synchronized counter at fob and car, a tolerance window for accidental presses; newer designs use a PRNG sequence from a shared seed. The ciphers underneath were proprietary and small: DST40 (40-bit key, 24-bit identifier, truncated 24-bit response), KeeLoq (32-bit block, 64-bit key, 528-round NLFSR, manufacturer key deriving per-device keys), Hitag2 (48-bit stream cipher), Megamos (96-bit secret), DST80 (80-bit successor, mutual authentication). Every one was eventually broken — while the *physical-layer* attacks (relay, jamming, replay) never needed the cryptography to break at all, which is what pushed the industry toward BLE and UWB.

**Cryptanalysis: the key-recovery era.** The taxonomy's first class is key recovery from sniffed exchanges, in five technique families. Exhaustive search: Bono et al. recovered DST40 keys from two challenge–response pairs (2005); Hitag2 fell to an attack needing two sniffed messages and about two hours on COPACOBANA, then to a black-box IV weakness reducing recovery to minutes on a cluster. Guess-and-determine: Bogdanov's KeeLoq recovery (2^50.6, improved form 2^37, at the cost of 2^32 known pairs), extended to Hitag2 with a claimed 500× improvement. Slide and algebraic attacks (SAT-solver formulations) cut KeeLoq to 2^53, then 2^44.5 encryptions. Correlation attacks produced the era's most consequential result — Garcia et al. on the Volkswagen Group: only a few *global* master keys fleet-wide, so one eavesdropped signal sufficed to clone a remote, plus a fast-correlation Hitag2 attack recovering the key from 4–8 signals in about a minute via the counter window (a 28-bit counter of which only 10 bits travel over the air). Power analysis cloned KeeLoq remotes from ten traces, then a *single* trace; a decade later Wouters et al. dismantled DST80-based immobilizers (glitching, side channels) and exposed key-diversification entropy so low at Toyota, Kia, and Hyundai that keys were predictable. Verdult et al.'s Megamos recovery exploited weak keys — in the analysed fleet only ten of 96 key bits were ones — at 2^56 cipher ticks (2^49 encryptions); "Gone in 360 Seconds" turned Hitag2's missing reader authentication and time-seeded LFSR state into a keystream oracle leaking a key bit per four authentications.

**The attacks that never went away.** Relay (Francillon et al., 2011: ten cars, relaying only the LF/UHF legs, up to 2 m from the car unamplified and 8 m amplified, 60 m on the key side) works because PKES verifies *that* the right key answered, never *where* it is. Jamming-and-replay works because rolling codes protect the code, not the counter's history: RollJam (Kamkar, 2015) jams and records a first press, replays it on the second, and banks the unused second code; RollingPwn showed Honda's resynchronization accepting previous-cycle codes (ten popular models, 2012–2022); RollBack needs no jamming — replaying two *consecutive* recorded signals rolls the receiver back through its resynchronization procedure to an earlier counter state (Kia and Mazda confirmed). New channels inherited the old classes: an NFC relay against Tesla's card key (four-digit PIN-to-drive the only backstop), NCC Group's link-layer BLE relay inside normal GATT timing variation, a Model X break chaining unsigned fob firmware over BLE with a pairing protocol that never sends certificates, and Ghost Peak's UWB HRP distance reduction (12 m measured as 0 m; 4% success, argued sufficient against single-measurement systems). The web era added a fifth class wholesale: API and third-party-app flaws (a remote starter's default credentials and SQL injection to admin; connected-service flaws exposing Honda/Nissan/Infiniti/Acura; a third-party Tesla logger's API) that unlock cars without touching the radio.

**The answers (Q1–Q4).** A1: systems *are* generally more secure — modern cryptography is harder to break — but relay and replay persist against even the newest systems, cars on the road still integrate legacy (even fixed-code) technology, and new channels enlarge the surface. A2: attack *types* have not changed in fifteen years; effort migrated from cryptanalysis to the physical layer and then to software, because relay is cheap, easy, and still works. A3 is the bleakest finding: **none of the thirteen published defences is implemented in a real system** — most are simulation-only, lack cost evaluation, or need special hardware and setup phases (PUF enrolment, QKD channels) OEMs have not adopted; ISO/SAE 21434 states requirements without prescribing an RKE design, so nothing forces convergence. A4: progress requires abandoning security by obscurity — open specifications, researcher cooperation, audit culture (Pwn2Own Automotive is the cited model) — plus standards that say *how*, not only *what*.

## Where it fits

The KB's key-fob pages are this SoK's primary sources; its value to the KB is the connective tissue between them. Its five-class taxonomy (cryptanalysis, relay, jamming-and-replay, new-technology, web) is a superset of the key-fob-relay-attacks concept's two-way split: that concept's relay-vs-cloning line is preserved exactly (relay forwards a genuine exchange and breaks no cryptography; cloning recovers key material), and the SoK adds the third family the concept does not cover — attacks on the counter machinery itself — plus the web/API class neither the concept nor the cipher pages reach. Against the individual pages: the Hitag2, Megamos, and Lock It numbers all check out against the SoK's retelling, and the SoK contributes the surrounding programme the pages omit — KeeLoq's full cryptanalysis history, DST80's dismantling, the power-analysis line. One divergence must not be silently harmonised: the SoK describes Wouters et al.'s Tesla Model S PKES break as reversing "the DST80 cipher … revealing only 40 bits" of system, while the KB's own Fast, Furious and Insecure page — written from that paper's full text — records the Pektron system as running **DST40, not DST80**. The SoK's phrasing reads as loose naming for a DST-family system at 40-bit strength; this page follows the TCHES paper. The SoK's §5.3 is also the clearest secondary source for the RollBack paper (batch 11): two consecutive signals, resynchronization semantics, Kia/Mazda confirmation.

## Limits and safety notes

First, the deployment verdict (A3) is an inference from public information about closed-source systems — the authors say so — so "no published defence is deployed" means none is *publicly known* to be deployed. Second, the survey's cryptanalysis is necessarily compressed: per-cipher detail lives in the KB's entity pages, and at least one compression (the DST80/DST40 naming above) loses a distinction the primary paper is careful about. The attack catalogue is a taxonomy with enabling conditions, not a procedure set; the KB records which systems fell and why the counter, ranging, and API designs allowed it, without reproducing tooling or exploitation steps. Theft relevance is present-tense: relay and RollJam-class thefts are booming again in the wild.

## Status and sources

Status: **published**. 3rd USENIX Symposium on Vehicle Security and Privacy (VehicleSec '25), 11–12 August 2025, Seattle, WA, USA; proceedings pp. 161–178; ISBN 978-1-939133-49-6. **No DOI**: USENIX VehicleSec papers carry no DOI, and a Crossref title query for this paper returned no record when checked for this page — consistent with the KB's other USENIX papers of the era.

## Related

- [Gone in 360 Seconds: Hijacking with Hitag2](gone-in-360-seconds-hijacking-with-hitag2.md)
- [Dismantling Megamos Crypto](dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md)
- [Lock It and Still Lose It](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md)
- [Fast, Furious and Insecure](fast-furious-and-insecure-passive-keyless-entry-and-start-systems-in-modern-supercars.md)
- [RollBack](rollback-a-new-time-agnostic-replay-attack-against-the-automotive-remote-keyless-entry-systems.md)
- [Key-fob relay attacks (concept)](concepts/key-fob-relay-attacks.md)
