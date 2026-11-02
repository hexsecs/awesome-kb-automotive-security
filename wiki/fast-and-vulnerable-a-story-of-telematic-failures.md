---
title: "Fast and Vulnerable: A Story of Telematic Failures"
summary: "Foster, Prudhomme, Koscher, and Savage, USENIX WOOT 2015. Shows an aftermarket OBD-II telematics dongle exposing SMS-reachable remote control of vehicle CAN…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/woot15/workshop-program/presentation/foster"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Foster, Prudhomme, Koscher, and Savage, USENIX WOOT 2015. Shows an aftermarket OBD-II telematics dongle exposing SMS-reachable remote control of vehicle CAN traffic."
related: [comprehensive-experimental-analyses-of-automotive-attack-surfaces, remote-exploitation-of-an-unaltered-passenger-vehicle, adventures-in-automotive-networks-and-control-units, experimental-security-analysis-of-a-modern-automobile, can-injection]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://www.usenix.org/system/files/conference/woot15/woot15-paper-foster.pdf"
    retrieved: 2026-11-01
---

Foster, Prudhomme, Koscher, and Savage, USENIX WOOT 2015. Shows an aftermarket OBD-II telematics dongle exposing SMS-reachable remote control of vehicle CAN traffic.

## What it is

A case study by Ian Foster, Andrew Prudhomme, Karl Koscher, and Stefan Savage (UC San Diego), USENIX WOOT '15, August 2015. The open USENIX PDF was read in full for this page. No DOI is confirmed — Crossref queries return no record for this paper (checked 2026-11-01), as with other USENIX papers of this era in this KB.

The subject is one family of aftermarket telematics control units (TCUs): the **C4E** of Mobile Devices Ingenierie, bought on eBay. Its named deployments are the point: the same platform underlies Metromile's per-mile insurance policies (and its Uber driver-partner policies), and the ecosystem section notes that Progressive's Snapshot — over two million customers per 2014 Progressive press materials — is a rebranded Xirgo XT-3000: a small set of common providers sits under many brands. The reference unit: a 500 MHz ARM11, 64 MB RAM, 256 MB flash, GPS, 3D accelerometer/gyroscope, mini-USB, a 2G cellular modem (3G in later models), and a CAN transceiver wired to the OBD-II pins.

The framing contrast is OEM versus aftermarket. Built-in TCUs (OnStar and its peers) are tightly coupled to the vehicle and the OEM's service channel — earlier built-in compromises, including the authors' own, could be "updated during scheduled vehicle service and mitigated through changes in the OEM-operated service." Aftermarket dongles are bought by consumers or supplied by insurers and fleets, loosely coupled, and maintained independently of any automotive service channel — so the problem "cannot be well addressed by automobile manufacturers themselves." Threat models: *local* (brief physical access — shipping interception, a valet) and *remote* (no physical access; the device sits in a victim's car, location unknown).

## What it showed

**Local surface.** The mini-USB port emulates a network adapter. With the debug console enabled, web (port 80) and telnet (port 23) listen without authentication, exposing privacy-sensitive data (current GPS location) and full configuration read/write — plus an SMS-sending feature that conveniently reveals the device's own SIM number. A console-authentication option buried in the filesystem was enabled on no tested device and "could be trivially bypassed by modifying the URL visited" — "we believe that the console authentication feature was never completed."

**The NAND dump and the fleet key.** Removing the NAND flash and replicating it (nandsim, UBIFS) gave a mountable copy of the device, including the main Java framework — and "a number of public and private cryptographic keys and certificates." The root SSH private key recovered this way authenticated to *other* TCUs from the same manufacturer, "including in production contexts" — the "default (and potentially singular) key for all such devices." Devices also shared common root/user passwords, SSH accepted password logins, and /etc/shadow used MD5 — the salted user password (eight characters, vowels and sequential numbers only) fell to a modest wordlist in under ten seconds.

**The services face the Internet.** Web, telnet, and SSH are bound to *all* interfaces, including the cellular modem — not just USB. The tested devices were shielded only by carrier NAT, "entirely a property of the carrier," not of the device.

**Finding devices at scale.** Every unit presents the same SSH host key, so a Shodan search for that fingerprint yielded about 1,500 candidate devices; the telnet welcome banner matched about 3,000 unique IPs, the majority from Spanish ISPs (a carrier without NAT). By phone number: the numbers "were not random" — many are sequentially assigned in the 566 area code, so one known number makes its neighbours likely TCUs, and an SMS `status` command confirms one: a "war dialer" for enumerating devices is "relatively straightforward."

**The SMS update chain — the core break.** An SMS administration interface, documented online, was enabled on all tested devices (property get/set, sensor status, remote-update initiation). The update procedure, reconstructed from logs: an SMS `rupd,USER,HOST,PORT,DIR` instructs the TCU to SCP into an arbitrary server, fetch a manifest of files with paths and hashes, install matching files, and execute any console commands embedded in the manifest. The design failures, in the paper's order: "updates are not cryptographically signed in any way"; "the device does not authenticate the server" (while the server authenticates the device, with a keypair all devices share); the interface "allows an arbitrary update server to be chosen." The proof: a rogue server whose payload replaces the console binary with a script that preserves the original as backup, opens a reverse shell and SSH tunnel, SMSes the attacker its success, and runs the original console to clear the logs. The procedure was also triggerable from the web and telnet consoles.

**Arbitrary CAN, in both firmware generations.** Newer firmware ships SocketCAN and can-utils, so a compromised TCU sends and receives arbitrary CAN packets with stock tools. Older firmware interposes a PIC microcontroller between the ARM CPU and the CAN controller; the team reverse-engineered the ARM↔PIC serial protocol, used the TCU's own PIC-flashing utility to dump that firmware, patched out its accessory-mode/ignition checks, and reflashed their "bypass" version — packets then sendable irrespective of vehicle state.

**The end-to-end demonstration.** A two-stage payload: stage one arrives by the SMS update (about a minute over 2G) and installs a hook that starts a reverse shell on a later SMS command, which then takes seconds. With a volunteer driver at low speed, the team remotely controlled body functions (windshield wipers) and brakes — "selectively applying brakes and selectively disabling brakes." Conducted at close distance for safety; "not limited by proximity and could have been carried out at arbitrary distance." The vehicle payload took a few days on an unfamiliar car, from past experience and public CAN "recipes."

**Prescriptions (§5):** sign updates and verify the update server; strengthen SMS authentication (whitelists are not authentication — numbers are spoofable; disable remote SMS admin or add real authentication); fix key management (public keys on devices, not the root private key; per-device unique keys); least-privilege passwords, no root SSH; disable WAN administration; unbypassable per-device console authentication; and maintain the update server — the default update domain in the console was found **unregistered and available**, a potential fleet-takeover vector the authors deliberately did not register.

**Disclosure (§6)** is part of the result: to Mobile Devices, Metromile, Uber, and DHS/US-CERT — all supportive; Metromile planned to disable SMS access on its branded devices. But the vendor's claims — fixed in later software; consoles only in "developer mode"; production SIMs not SMS-capable — did not match the evidence: fixes were absent from recent production devices tested, and the vulnerable configuration was found in production devices directly, "to say nothing of the several thousand we identified online." The structural conclusion: vendors of remotely exposed, safety-connected devices need short-notice update rollout across a fragmented legacy fleet — exactly the channel aftermarket devices lack.

## Where it fits

The aftermarket counterpart to this KB's built-in telematics results. [Checkoway et al. 2011](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md) compromised an OEM telematics unit over Bluetooth and cellular; Miller and Valasek's 2015 Jeep work (cited here via the Wired report, contemporaneous with WOOT) did the same to Uconnect. Foster et al. show the identical pattern — wireless entry, arbitrary CAN — in a device class where no OEM service relationship exists to deliver the fix, and where one extracted key is every device's key. Its unsigned, server-unauthenticated SMS update chain is the dongle-form of the update-path trust failures this KB tracks in IVI systems. And where [Koscher et al. 2010](experimental-security-analysis-of-a-modern-automobile.md) and [Miller and Valasek 2013](adventures-in-automotive-networks-and-control-units.md) required physical CAN access, this dongle's entire purpose is to sit on that port with a cellular radio attached.

## Limits and safety notes

One device family, purchased second-hand; the claim that the vulnerabilities span its deployments rests on the shared SSH key (verified against other units, including production ones), the ~1,500–3,000 Internet-visible devices, and the authors' statement that the C4E family's software is "substantially similar" across configurations — the vendor disputes parts of the production picture, and the paper prints that dispute unresolved. Braking was demonstrated at low speed with a volunteer driver. The paper withholds the update manifest's true filename "to filter out potential low-level war dialing attacks" while fixes were pending; this page likewise stays at mechanism, not procedure.

## Status and sources

Status: **published** — a finished 2015 workshop publication; no DOI (Crossref checked, above). Sources: the paper (USENIX open PDF), read in full 2026-11-01; the list.

## Related

- [Comprehensive Experimental Analyses of Automotive Attack Surfaces](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md)
- [Remote Exploitation of an Unaltered Passenger Vehicle](remote-exploitation-of-an-unaltered-passenger-vehicle.md)
- [Adventures in Automotive Networks and Control Units](adventures-in-automotive-networks-and-control-units.md)
- [Experimental Security Analysis of a Modern Automobile](experimental-security-analysis-of-a-modern-automobile.md)
- [CAN injection](concepts/can-injection.md)
