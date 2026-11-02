---
title: "Experimental Security Analysis of a Modern Automobile"
summary: "Koscher et al., IEEE S&P 2010. The paper that opened the field, demonstrating that an attacker with access to any single ECU can disable the brakes and stop…"
type: entity
category: "Research Papers"
url: "https://www.autosec.org/pubs/cars-oakland2010.pdf"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: deep
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
  - diagnostic-service-abuse
---

Koscher et al., IEEE S&P 2010. The paper that opened the field, demonstrating that an attacker with access to any single ECU can disable the brakes and stop the engine of a moving vehicle.

## What it is

Karl Koscher, Alexei Czeskis, Franziska Roesner, Shwetak Patel, and Tadayoshi Kohno (University of Washington) with Stephen Checkoway, Damon McCoy, Brian Kantor, Danny Anderson, Hovav Shacham, and Stefan Savage (UC San Diego). *IEEE Symposium on Security and Privacy* 2010, pp. 447–462. DOI: [10.1109/SP.2010.34](https://doi.org/10.1109/SP.2010.34) (verified via Crossref). The authors' PDF at autosec.org was read in full for this page.

The paper opens on scale: a typical luxury sedan of the era contains **over 100 MB of binary code spread across 50–70 ECUs** — the claim that motivates treating the car as a network of computers rather than a device. The authors describe the work (§VII) as "**the first experimentally guided study** into the real security risks with a modern automobile." Since 2008, all cars sold in the US have been required to implement CAN (ISO 11898) for diagnostics, which is the authors' basis for arguing the results generalise beyond one model.

**Threat model, explicitly skirted:** the paper asks what an attacker *who can already communicate on the car's internal network* can do. How she gets there — physical access via OBD-II, malicious supply-chain or aftermarket components, the car's digital radio interfaces (the paper counts no fewer than five kinds) — is surveyed but left to future work; the authors note they had in fact developed remote compromises, outside this paper's scope.

## How the experiments were run

**Vehicles.** Two **2009-model-year** automobiles, same make and model, deliberately not identified. Footnote 1 gives the anonymization rationale in the authors' words: they believe the risks "arise from the architecture of the modern automobile and not simply from design decisions made by any single manufacturer," and that other manufacturers and models with similar features "may have similar security properties." The model was chosen because it contained (a) a large number of electronically controlled components, necessitated by complex safety features such as anti-lock brakes and stability control, and (b) a sophisticated telematics system. Two vehicles were purchased **to allow differential testing and to validate that results were not tied to one individual vehicle**: all controlled experiments were initially conducted on one car and then repeated on the second; road tests used the first car only. Individual replacement ECUs were bought via third-party dealers for bench work, and — decisively for the telematics work — **multiple telematics units were obtained via Internet-based used-parts resellers**, which made destructive and reverse-engineering work on that unit practical.

**Three settings.** (1) *Bench:* ECUs physically extracted and interrogated in isolation — Figure 1 shows the brake module (EBCM) hooked to a power supply, a CAN-to-USB converter, and an oscilloscope; the bench is where the EBCM key was exhaustively recovered. (2) *Stationary car:* most in-car experiments, with the car **elevated on jack stands** for experiments requiring it to be "at speed" — defined precisely: throttle applied to bring the **wheel speed to 40 MPH**. The in-car hookup split by bus: a laptop on the OBD-II port running CARSHARK, via an off-the-shelf **CANCapture ECOM** cable for the high-speed bus and an **Olimex AVR-CAN board (Atmel AT90CAN128) with custom firmware** for the low-speed bus. (3) *On the road:* a closed course — the runway of a **decommissioned airport**, long and straight, giving time to respond in an emergency. One researcher drove the test car; three others rode in a chase car on a parallel service road — one driving it, one documenting on video, one **wirelessly controlling the test car over an 802.11 ad hoc connection** to its laptop. Commands went from the chase car to the test car's CAN bus; the driver confirmed effects verbally over walkie-talkies; cancellation packets were then sent. The emergency measure was physical: the driver could **yank a cord attached to the CAN cable and pull the laptop out of the OBD-II port** — preparatory tests verified the car reverted to normal within a few seconds. It was never needed. The driver wore a helmet.

**Why road tests were not redundant:** the authors call them the "gold standard." Brake behaviour could never be completely characterised on jack stands, because **the rear wheels being stationary provided additional input to the EBCM that produced illogical behaviour** — the full effect of the EBCM DeviceControl packets was only observed on the road. Road results are therefore a re-tested subset of the stationary results, not a rerun of all of them.

## The test car's architecture

Two buses: a differentially signalled **high-speed** bus carrying powertrain systems, and a **low-speed** bus (SAE J2411, single-wire) for less-demanding components; the car's CAN variant adds slight framing extensions. CAN is publish-and-subscribe: the CAN ID indicates packet *type*, there are no addresses, every packet is broadcast, and each node decides for itself whether to process it — with **no authenticator fields and not even source identifiers**, so any component can indistinguishably address any other, and the bus is fragile to denial of service (flooding, or a node asserting the dominant state indefinitely).

Table I of the paper lists eleven key ECUs. **High-speed only:** the ECM (engine — fuel, ignition timing), the EBCM (brakes — ABS pump motor and valves), and the TCM (transmission). **Low-speed only:** the RCDLR (key-fob receiver; also receives TPMS data wirelessly), HVAC, the SDM (airbags and pretensioners), the IPC/DIC (instrument cluster), the Radio (which also funnels and generates most in-cabin sounds — beeps, buzzes, chimes), and the TDM (theft deterrent — prevents starting without a legitimate key). **On both buses, exactly two:** the **BCM** (body control — and the designated gateway/firewall between the subnets) and the **telematics module** (remote communication via cellular link). That two-bridge fact is the setup for the subnet-bridging result below.

## CARSHARK and the attack methodology

**CARSHARK** is the team's custom CAN bus analyzer and packet-injection tool, written because no commercial tool sufficed: they needed to process their vendor's **proprietary extensions** to the CAN protocol, and a commercial sniffer plus a manufacturer diagnostic tool still lacked three capabilities their explorations required — **reading out ECU memory, loading custom code into ECUs, and generating fuzz-testing packets**. Its modes: **sniff** (Figure 4 shows recently updated values highlighted), **inject** (crafted or replayed packets), and **fuzz**. The composite attacks below were packaged as CARSHARK demos/modules, not one-off scripts.

Three approaches, in the paper's order. (1) **Packet sniffing and targeted probing** — observing which packets are sent when components activate (e.g. turning on the headlights), then replaying and probing; this yielded control of the radio, the IPC, and a number of BCM functions, but "was less useful in mapping the interface to safety-critical powertrain components." (2) **Fuzzing** — the powertrain workhorse, detailed next. (3) **Reverse engineering** — for a small subset of ECUs, notably the telematics unit, they **dumped code via the CAN ReadMemory service** and analysed it in IDA Pro; the paper states this approach is *essential* for attacks that add new functionality (e.g. bridging the buses) rather than manipulate existing capabilities. The authors state they **omit certain details, such as complete packet payloads, "to prevent would-be attackers from using our results directly"** — and the tables print packet values truncated in any case. This page follows the same line: capabilities, method, and table-level results; no payloads.

## What it showed

### Fuzzing DeviceControl

The paper's own surprise, stated plainly: "significant attacks do not require a complete understanding or reverse-engineering of even a single component of the car." Because the range of valid CAN packets is rather small, simple fuzzing does significant damage; for indiscriminate disruption **fuzzing is an effective attack by itself**, and the team also used it as a reverse-engineering aid (unlike traditional fuzzing, which hunts crashes). The target was the proprietary **DeviceControl** service, accessed RPC-like via CAN messages. DeviceControl takes a **Control Packet Identifier (CPID)** — a *group* of controls to override — with **up to five bytes of parameters** specifying which controls in the group are overridden and how; the paper's worked example is the BCM's external-lights CPID, whose parameter data sets brightness. DeviceControl can also reset some learned internal state. The workflow: **enumerate all supported CPIDs** for an ECU, send **random data as the argument to valid CPIDs**, and **correlate input bits with observed behaviours**. Results are tabulated for the BCM (Table II), ECM (Table III), and EBCM (Table IV), each row recording the action, whether an occupant could **manually override** it, whether it had the **same effect at speed**, whether the module first had to be **unlocked with its DeviceControl key**, and whether it was **re-tested on the runway**. The authors' headline quantification: "**a large fraction of the random packets we sent resulted in changes to the state of our car**" — generalised in §VII to the claim that a fuzzer is likely a *universal* attack for disrupting arbitrary automobiles, analogous to the "crashme" program that fuzzed system calls before syscall interfaces were hardened.

### Body Control Module — everything, ungated

Control split across both buses (low-speed packets reverse-engineered, high-speed packets fuzzed) reached "**essentially all of the BCM's functions**." Table II's qualifier pattern is itself a finding: **all 15 BCM DeviceControl effects worked at speed, and none of the 15 required unlocking the BCM with its DeviceControl key.** The effects: continuously activate the lock relay (jamming the door locks); unlock all doors (also achievable via normal-operation packets, key-fob-equivalent); pop the trunk; release the shift-lock solenoid; **permanently activate the horn** and control its frequency; disable headlights in auto light control; all auxiliary lights off; **all brake/auxiliary lights off**; dome-light and instrument brightness control; windshield wipers on continuously; windshield fluid shooting continuously; wipers forced off while fluid shoots (the one row with a manual escape — the wipers' highest setting cannot be disabled and serves as an override); disable the window and key-lock relays. Manual override exists for only a minority of rows; most were also runway-re-tested (8 of 15).

### Engine Control Module — everything, gated, plus one ungated kill

Most engine attacks came from fuzzing DeviceControl requests to the ECM, with the qualifier pattern *inverse* to the BCM's: **all six ECM effects required unlocking with the DeviceControl key**, and all six worked at speed. The effects: initiate crankshaft re-learn and **disturb engine timing** by resetting the learned crankshaft angle sensor error; temporary and idle RPM increases; **disable cylinders** — including **all cylinders simultaneously with the wheels spinning at 40 MPH** on jack stands; **kill the engine so it knocks excessively on restart or cannot be restarted at all**; grind the starter. A normal-operation packet abuse sits beside the fuzzed set: forging a packet with the **"airbag deployed" bit set** disables the engine. And one qualification to the gating pattern: a Kill Engine packet found by observation (Table V) needed **no unlock** — the key-gated pattern holds for the fuzzed DeviceControl set, not for every engine-kill path.

### Electronic Brake Control Module — the safety-critical core

Four fuzzed effects, none manually overridable, all working at speed: **engage the front-left brake** individually; engage the front-right / release the front-left; **unevenly engage the right brakes**; and **release the brakes and prevent braking** altogether. On the runway, DeviceControl packets **released the brakes and prevented the driver from braking at all** — no pedal pressure activated them — and a second packet **locked the brakes instantaneously and unevenly**.

Two details the tables compress. First, the stuck brake: one random packet not only engaged the front-left brake but **locked it resistant to manual override even through a power cycle and battery removal**; the team had to resort to *continued fuzzing* to find a packet that reversed the effect — the paper's clearest illustration that fuzzing writes state the car's own power cycle does not clear. Second, the unlock nuance: on jack stands the EBCM did **not** need its DeviceControl key; on the runway the team discovered the EBCM required unlocking at speed (above 5 MPH) — a minor caveat in practice, since the key is recoverable (below) by attached hardware.

### Radio, instrument cluster, and the rest

**Radio:** complete control of the radio and its display, including **disabling user control**; consistently increase the volume and **prevent the user from resetting it**; arbitrary messages displayed. Because the radio generates the car's sounds, they could produce **turn-signal clicks and seat-belt chimes at arbitrary frequencies, durations, and intervals**. **IPC/DIC:** full control — arbitrary messages, **falsified fuel level and speedometer reading**, illumination adjustment (Figure 6 shows a false speedometer reading with the car in Park). **HVAC:** DeviceControl functions found by the same fuzzing, though the paper gives it no results table. The SDM, RCDLR, and TDM were not individually attacked through fuzzing; the RCDLR reappears in the access-control findings below. Generic denial of service rounds out the component results: silencing an ECU's communications has system-level effects — with the ECM muted the speedometer reads 0; with the BCM muted the IPC froze and the car could not be restarted — while the wired-OR ignition logic means the car **keeps running with the key removed** once started.

### Composite attacks

Three packaged composites show what the primitives compose into. **Falsified speedometer:** intercept genuine speed updates and inject crafted ones — 105 lines of AVR-CAN C, verified against a radar gun, halving the displayed speed at up to 20 MPH. **Lights Out:** all lights — headlights, brake lights, panel illumination — extinguished at **40 MPH or more**, preconditioned on the auto light control being engaged. **Self-destruct:** a 60-second dashboard countdown with clicks and horn, ending in engine kill and door locking — in fewer than 200 lines of code.

## The access-control layer: seed/key, and where the car deviated from its own standards

The diagnostic access control that does exist — two challenge–response (seed/key) pairs guarding reflash and memory access and the powerful DeviceControl service — uses **16-bit seeds and 16-bit keys**, with a key attempt allowed every 10 seconds: **a little over 7½ days to brute-force one ECU online, ~3½ days with power-cycling on the bench** (power-cycling every two attempts to dodge the attempt timing). The team recovered the EBCM's key exhaustively in **about 1½ days**. Many seed/key algorithms were already known to the car-tuning community. The governing standard's own language, quoted by the paper, is that "under no circumstances shall the encryption algorithm ever reside in the node" — the algorithms were in the nodes.

Against that baseline, the paper verifies a five-item cluster of deviations from the standards the car was built to (§IV-C and §VII):

1. **Disable-communications accepted while moving** — ECUs accepted the command to silence communications while the car was in motion; the standard says reject when unsafe.
2. **Reflash at speed** — the ECM and TCM entered reflashing mode with the engine running and the car at speed, stopping the engine.
3. **The telematics unit's seed/key was doubly void** — it used a **hardcoded challenge and response common to all units of the part number**, against the standard's explicit rule that units sharing a part number shall not share a security seed — *and* it never actually checked the protocol's result, so the team loaded their own code onto it with no authentication at all. Two distinct defects, either one sufficient.
4. **Keys extractable without authentication** — the BCM's reflash keys sat bare in memory; the ECM/TCM DeviceControl keys were reachable via the reflash key; the telematics unit's full memory was readable. The gate's keys were behind no gate.
5. **The RCDLR was also loadable without authentication** — named in §VII alongside the telematics unit as accepting code loading unauthenticated.

Few DeviceControl functions were actually disabled at speed, despite the standard's intent — the at-speed qualifier columns of Tables II–IV are the systematic form of that finding.

## Subnet bridging

The car's two buses are nominally separated by the BCM gateway. But the telematics unit sits on both — and could be reprogrammed *from the low-speed bus*, turning it into a bridge relaying packets onto the high-speed bus: **1,184 bytes of uploaded code (291 instructions) sufficed**, bypassing the BCM gateway entirely. The paper details two code-hosting variants for the bridge (§VI-C). Code hosted in the telematics unit — a QNX environment with GPS, audio, and cellular interfaces — could additionally **erase itself**: the attack code is RAM-resident, a reboot wipes it, and the team verified the self-wipe on the runway (triggered at 20 MPH) — defeating post-incident forensics.

## Where it fits

The empirical turn of the field, and the counterpart to [Wolf 2004](security-in-automotive-bus-systems.md): Wolf analysed what bus architecture *permits*; Koscher et al. showed what production cars *actually allowed*, on the road. It is the direct predecessor of [Checkoway et al. 2011](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md), which took up this paper's deferred attack-surface question, and of the Miller & Valasek line. Its 16-bit seed/key findings are the experimental root of the KB's [UDS seed/key](concepts/uds-seed-key.md) concept page, and its injection methodology anchors the [CAN injection](concepts/can-injection.md) concept. The DeviceControl results are the founding evidence for a gap the concept layer has since named separately: the diagnostic services themselves, as distinct from the lock in front of them.

## Limits and safety notes

Scope as the paper states it: two vehicles of one (anonymized) make and model, chosen for their ECU count and telematics; the authors argue the risks are architectural, not manufacturer-specific, but every concrete result is from that one platform. The anonymization is deliberate and stated in the paper — this page does not name or guess the vehicle. Every attack presupposes an attacker already on the internal network; remote entry is asserted to exist but is *not* demonstrated here. Time at the test facility ran out before all attacks were re-verified while driving; road results are a re-tested subset. The paper prints no measured attempt rate for the EBCM key recovery — the ~1½ days is the reported outcome, not a rate — and offers no signature-verification verdict for the ECM/EBCM/TCM reflash path beyond the deviations listed above. The authors withheld some packet payload details to prevent direct reuse; this page follows the same line — capabilities and method, no payloads.

## Status and sources

Status: **published** — a finished 2010 publication; CARSHARK was the team's internal tool, not a maintained release. Sources: the paper (open author copy, autosec.org), read in full 2026-11-01 (and re-read end-to-end for this deep revision); the DOI record; the list. This page is the KB's first `deep` page (OpenShelf SPEC §4.5) — the pilot for the tier.

## Related

- [Security in Automotive Bus Systems](security-in-automotive-bus-systems.md)
- [Comprehensive Experimental Analyses of Automotive Attack Surfaces](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md)
- [UDS seed/key](concepts/uds-seed-key.md)
- [CAN injection](concepts/can-injection.md)
