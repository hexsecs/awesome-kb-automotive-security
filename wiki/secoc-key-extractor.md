---
title: "SecOC Key Extractor"
summary: "Scripts to extract SecOC (Secure On-Board Communication) keys from Toyota vehicles using comma.ai panda hardware."
type: entity
category: "Penetration Testing"
url: "https://github.com/i-can-hack/secoc"
status: maintenance
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Scripts to extract SecOC (Secure On-Board Communication) keys from Toyota vehicles using comma.ai panda hardware."
related: [panda, uds-seed-key, uds-firmware-extraction, firmware-acquisition]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/i-can-hack/secoc"
    retrieved: 2026-11-01
  - url: "https://icanhack.nl/blog/secoc-key-extraction/"
    retrieved: 2026-11-01
---

Scripts to extract SecOC (Secure On-Board Communication) keys from Toyota vehicles using comma.ai panda hardware.

## What it is

Scripts that extract the AUTOSAR SecOC keys — and the ECU master key — from certain Toyota vehicles, defeating the message-authentication scheme that would otherwise keep third-party devices off the CAN bus. The attack runs against the electric power steering (EPS) ECU: its bootloader's firmware update path is used to upload a shellcode payload that executes on the ECU and dumps the keys from RAM. The author's stated goal was running openpilot on a 2021 RAV4 Prime, and the linked blog post is the full writeup. Per the README, users have confirmed it working on 2021–2023 RAV4 Prime and 2021 Sienna LE.

## How it works

Host side: `extract_keys.py`, run with the vehicle in "IGNITION ON" (power button pressed twice, engine not READY), communicating over CAN via a comma.ai panda running the latest panda Python library. The sequence, from the README's captured run and the author's blog: read application software identification; pass UDS SecurityAccess (0x27) seed/key; write data by identifier (0x2E) to DIDs carrying the AES key and IV used to derive the payload encryption key; then Request Download (0x34) and Transfer Data (0x36) upload the payload in blocks, and a Routine Control (0x31) verifies and triggers it. The output is the dumped key store (448 entries in the sample run) and the printed `ECU_MASTER_KEY` and SecOC key. It works because the EPS ECU (Renesas RH850/P1M-E) implements SecOC in software — no HSM — so the keys live in RAM, and its bootloader can upload data into a RAM region that is later called during flash operations: the code-execution hook. The uploaded blob must be encrypted with correct CRC and CMAC, which the researchers could produce because all key material came from firmware extracted earlier, via voltage fault injection (per the blog's linked prior post). A prebuilt `payload.bin` is included, so extraction needs no build; rebuilding it additionally needs a firmware secret the README deliberately leaves "as an exercise to the reader".

## Where it fits

The section's clearest worked example of a production cryptographic control failing at its implementation seams: SecOC itself — AES-CMAC with freshness values — was not broken; the keys were reachable because one ECU did the crypto in software and its bootloader offered a RAM-upload path. It leans on [panda](panda.md) hardware, its security-access step is the legitimate side of [UDS seed/key](concepts/uds-seed-key.md), and it is the offensive counterpart to the KB's firmware-extraction material ([uds-firmware-extraction](uds-firmware-extraction.md)): the firmware had to come out before the keys could.

## Limits and safety notes

The README's warnings are unusually blunt and are part of the artefact: "THIS IS AT YOUR OWN RISK — This may brick your EPS. Only attempt this if you're willing to replace the EPS or steering rack if needed." The target is a safety-critical steering ECU. Vehicle scope is narrow and evidence-based: only the two models the README lists as user-confirmed; anything else is untested by the source. The procedure needs physical access, a panda, and the specific ignition state. The repository has no licence file, so the code's reuse terms are unstated.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived; created 2024-03-02, it has 17 commits with the latest on 2025-03-04 and repository activity into mid-2025; there are no releases. A finished research tool that has not been formally closed. Documentation claims above come from the following primary sources; no vehicle was modified for this page.

- [Upstream repository](https://github.com/i-can-hack/secoc)
- [Author's writeup](https://icanhack.nl/blog/secoc-key-extraction/)

## Related

- [panda](panda.md)
- [UDS seed/key](concepts/uds-seed-key.md)
- [uds-firmware-extraction](uds-firmware-extraction.md)
