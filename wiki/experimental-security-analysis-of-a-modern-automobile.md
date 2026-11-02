---
title: "Experimental Security Analysis of a Modern Automobile"
summary: "Koscher et al., IEEE S&P 2010. The paper that opened the field, demonstrating that an attacker with access to any single ECU can disable the brakes and stop…"
type: entity
category: "Research Papers"
url: "https://www.autosec.org/pubs/cars-oakland2010.pdf"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Koscher et al., IEEE S&P 2010. The paper that opened the field, demonstrating that an attacker with access to any single ECU can disable the brakes and stop the engine of a moving vehicle."
sources:
  - url: "https://www.autosec.org/pubs/cars-oakland2010.pdf"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1109/SP.2010.34"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - security-in-automotive-bus-systems
  - comprehensive-experimental-analyses-of-automotive-attack-surfaces
  - uds-seed-key
  - can-injection
---

Koscher et al., IEEE S&P 2010. The paper that opened the field, demonstrating that an attacker with access to any single ECU can disable the brakes and stop the engine of a moving vehicle.

## What it is

Karl Koscher, Alexei Czeskis, Franziska Roesner, Shwetak Patel, and Tadayoshi Kohno (University of Washington) with Stephen Checkoway, Damon McCoy, Brian Kantor, Danny Anderson, Hovav Shacham, and Stefan Savage (UC San Diego). *IEEE Symposium on Security and Privacy* 2010, pp. 447–462. DOI: [10.1109/SP.2010.34](https://doi.org/10.1109/SP.2010.34) (verified via Crossref). The authors' PDF at autosec.org was read in full for this page.

## What it showed

**Method:** two 2009-model-year cars of the same make and model (deliberately anonymized — see Limits), plus spare ECUs bought from third-party dealers. Experiments in three settings: bench (extracted ECUs), stationary car on jack stands, and live road tests on a decommissioned airport runway with a chase car. Tooling: **CARSHARK**, their custom CAN analyzer and injection tool, via the OBD-II port.

**Threat model, explicitly skirted:** the paper asks what an attacker *who can already communicate on the car's internal network* can do. How she gets there — physical access via OBD-II, malicious supply-chain or aftermarket components, the car's digital radio interfaces — is surveyed but left to future work; the authors note they had in fact developed remote compromises, outside this paper's scope.

**The network substrate:** CAN is broadcast with **no authenticator fields and not even source identifiers** — any component can indistinguishably address any other — and CAN is fragile to denial of service (flooding, or a node asserting the dominant state indefinitely). The diagnostic access control that does exist — two challenge–response (seed/key) pairs guarding reflash and memory access and the powerful DeviceControl service — uses **16-bit seeds and 16-bit keys**, with a key attempt allowed every 10 seconds: roughly 7.5 days to brute-force one ECU online, 3.5 days with power-cycling on the bench. The team recovered the brake module's (EBCM) key exhaustively in about 1.5 days. Many seed/key algorithms were already known to the car-tuning community.

**Standards deviations, verified experimentally:** ECUs accepted the disable-communications command while the car was moving (the standard says reject when unsafe); the engine and transmission modules entered reflashing mode with the engine running and at speed, stopping the engine; and the telematics unit used a **hardcoded challenge and response common to all units of the part number** — against the standard's explicit rule that units with the same part number shall *not* share a security seed — and never actually checked the protocol's result, so the team loaded their own code onto it with no authentication at all.

**Component control:** systematic fuzzing plus reverse engineering of the proprietary DeviceControl service gave control over the engine, brakes, heating and cooling, lights, instrument panel (including arbitrary displayed messages and false speedometer readings), radio, and door locks — in the authors' words, a large fraction of random fuzzed packets changed the car's state.

**Road tests (up to 40 MPH):** DeviceControl packets to the EBCM **released the brakes and prevented the driver from braking at all** — no pedal pressure activated them — and a second packet **locked the brakes instantaneously and unevenly**; the same family killed the engine, prevented restart, and disabled all of the car's lights at 40 MPH or more. Few DeviceControl functions were actually disabled at speed, despite the standard's intent.

**Composite attacks:** a falsified-speedometer attack (intercept genuine speed updates, inject crafted ones); a "self-destruct" demo (a 60-second dashboard countdown with clicks and horn, ending in engine kill and door locking) in fewer than 200 lines of code; and **subnet bridging** — the car's two CAN buses are nominally separated by the Body Control Module gateway, but the telematics unit sits on both and could be reprogrammed *from the low-speed bus*, turning it into a bridge relaying packets onto the high-speed bus: 1,184 bytes of uploaded code (291 instructions) sufficed, bypassing the gateway entirely. Code hosted in the telematics unit (a QNX environment with GPS, audio, and cellular interfaces) could additionally erase itself — a reboot wipes the RAM-resident attack — defeating post-incident forensics.

## Where it fits

The empirical turn of the field, and the counterpart to [Wolf 2004](security-in-automotive-bus-systems.md) in this batch: Wolf analysed what bus architecture *permits*; Koscher et al. showed what production cars *actually allowed*, on the road. It is the direct predecessor of [Checkoway et al. 2011](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md), which took up this paper's deferred attack-surface question, and of the Miller & Valasek line. Its 16-bit seed/key findings are the experimental root of the KB's [UDS seed/key](concepts/uds-seed-key.md) concept page, and its injection methodology anchors the [CAN injection](concepts/can-injection.md) concept.

## Limits and safety notes

Scope as the paper states it: two vehicles of one (anonymized) make and model, chosen for their ECU count and telematics; the authors argue the risks are architectural, not manufacturer-specific, but every concrete result is from that one platform. The anonymization is deliberate and stated in the paper — this page does not name or guess the vehicle. Every attack presupposes an attacker already on the internal network; remote entry is asserted to exist but is *not* demonstrated here. Time at the test facility ran out before all attacks were re-verified while driving; road results are a re-tested subset (the EBCM also needed unlocking above 5 MPH while driving — a minor caveat, since attached hardware can recover the credentials). The authors withheld some packet payload details to prevent direct reuse; this page follows the same line — capabilities and method, no payloads.

## Status and sources

Status: **unknown** — a finished 2010 publication; CARSHARK was the team's internal tool, not a maintained release. Sources: the paper (open author copy, autosec.org), read in full 2026-11-01; the DOI record; the list.

## Related

- [Security in Automotive Bus Systems](security-in-automotive-bus-systems.md)
- [Comprehensive Experimental Analyses of Automotive Attack Surfaces](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md)
- [UDS seed/key](concepts/uds-seed-key.md)
- [CAN injection](concepts/can-injection.md)
