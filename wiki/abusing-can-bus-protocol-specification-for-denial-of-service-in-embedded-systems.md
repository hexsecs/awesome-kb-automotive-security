---
uid: 01a1b02c-9900-7f0c-b402-7df5e1636c74
title: "Abusing CAN Bus Protocol Specification for Denial of Service in Embedded Systems"
summary: "Petran, DEF CON 31 Car Hacking Village 2023. Shows how an out-of-range CAN data length code reaches firmware unchecked and overflows a buffer, demonstrated…"
type: entity
category: "Conference Presentations"
url: "https://media.defcon.org/DEF%20CON%2031/DEF%20CON%2031%20villages/DEF%20CON%2031%20villages%20captions/DEF%20CON%2031%20-%20Car%20Hacking%20Village%20-%20Abusing%20CAN%20Bus%20Protocol%20Specification%20for%20Denial%20of%20Service%20in%20Embedded%20Systems%20-%20Martin%20Petran.eng.txt"
status: published
last_checked: 2026-11-17
created: 2026-11-06
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: a25e33d
list_summary: "Petran, DEF CON 31 Car Hacking Village 2023. Shows how an out-of-range CAN data length code reaches firmware unchecked and overflows a buffer, demonstrated on a development board and a Tesla Model 3 ECU."
related:
  - canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks
  - error-handling-of-in-vehicle-networks-makes-them-vulnerable
  - car-hacking-village
  - the-vehicle-may-be-sick-denial-of-diagnostic-services-by-exploiting-the-can-transport-protocol
  - can-availability
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-06
  - url: "https://media.defcon.org/DEF%20CON%2031/DEF%20CON%2031%20villages/DEF%20CON%2031%20villages%20captions/DEF%20CON%2031%20-%20Car%20Hacking%20Village%20-%20Abusing%20CAN%20Bus%20Protocol%20Specification%20for%20Denial%20of%20Service%20in%20Embedded%20Systems%20-%20Martin%20Petran.eng.txt"
    retrieved: 2026-11-17
facets: [can, firmware, hardware, research, standards]
---

Petran, DEF CON 31 Car Hacking Village 2023. Shows how an out-of-range CAN data length code reaches firmware unchecked and overflows a buffer, demonstrated on a development board and a Tesla Model 3 ECU.

## What it is

A DEF CON 31 Car Hacking Village talk by Martin Petran of Accenture's embedded system security team in Prague. The subject is a protocol-metadata bug: the CAN Data Length Code (DLC) is specified as 0–8, but it is a 4-bit field, and most hardware and software pass values up to 0xF straight to application code. If firmware uses DLC as the length of a `memcpy` into an 8-byte buffer, an out-of-range value overflows it. The talk demonstrates this first in a white-box development-board setup, then as a simulated assessment of a real Tesla Model 3 ECU.

## How it works

The CAN frame's DLC says how many data bytes follow. Setting all four bits gives 15, though no more than eight bytes are actually transmitted — such frames are malformed and not really received. The problem is that libraries do not validate the field: the speaker found that the SDKs named in the caption as "Armabed OS", STM32Cube SDK and NXP MCUXpresso SDK pass any value through, while the Linux kernel drivers never return more than 8. A typical vulnerable pattern is an 8-byte destination buffer with `memcpy(buf, can_data, frame.dlc)` because the developer knows CAN carries at most 8 bytes and trusts the framework's length field. The overflow source is not only the frame data: on the NXP board the DLC sits adjacent to the data union in the driver's frame structure, so the bytes copied past the payload include the DLC itself and neighbouring struct members — limited attacker control, but enough to change adjacent variables. The speaker notes that flipping a null check such as an `isAuthenticated` flag from 0 to nonzero is theoretically possible, though real cases ended in denial of service through corrupted pointers.

The white-box demo uses an NXP development board as victim and an Arduino with a button as attacker, sending CAN ID `600A`, DLC `0xF` and payload `ABCDEFGH`. Stepping through in the debugger shows the 15-byte copy overwriting an 8-byte buffer, with the first byte of the overflow being the DLC value itself.

The second demo is a Tesla Model 3 security controller — the NFC card reader between the seats involved in unlocking doors and the drive decision. Unpopulated `STJTAG` pads next to an STMicro SPC560B64 gave a working JTAG interface; a J-Link `savebin` dumped the firmware from `0x0` to `0x17FFFF`. The binary was loaded into IDA as PowerPC using the team's "Firm Loader" plugin to create memory sections and trigger auto-analysis (~1,700 functions). Two ways to find the bug are shown: identify standard functions from the calling convention (R3/R4/R5 and a counter-register loop identify `memcpy`), then review its callers; or combine static and dynamic analysis by searching immediate values for CAN IDs observed on the bus, locating a CAN handler, and decompiling it. The handler for `600A` copies `canData` for `canDLC` bytes into an 8-byte global at `0x1AF0`, with another variable at `0x1AF8` immediately after it. A second plugin, "Wolfie", automates the search by filtering `memcpy` call sites whose length argument is non-constant and which are reachable from the CAN handler; it found six, including one at `0x6F1BA` that overflows a local 8-byte array into an adjacent stack canary. Hitting the canary sends execution to an endless-loop fault handler — the crash that produces the denial of service. The debugger shows the canary (all zeros) overwritten with the CAN ID and DLC-derived values; changing the ID would avoid the handler, so control over the overflow bytes is limited.

## Detection and impact

The crash was originally found by fuzzing with a side channel: an oscilloscope on the CAN bus and an NFC-field probe show CAN traffic stopping at the malicious frame and the NFC field dying about half a second later, because the NFC controller is a separate chip. The talk also notes power-consumption measurement (needs soldering), gaps in periodic CAN messages, reset messages, and — half-joking — a DEF CON badge with an NFC coil as a field detector. CAN FD is not affected because of its DLC translation table; CAN XL was judged likely unaffected on paper, but the speaker reserved judgment until real implementations exist. The affected set is anyone who blindly uses DLC as a copy length; the three named SDKs were reportedly fixed after disclosure.

## Where it fits

This is the protocol-layer counterpart to [CANflict](canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks.md), which attacks data-link behaviour rather than a length field, and to [error handling of in-vehicle networks makes them vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md), which covers the same class of trust-in-metadata problem. [Car Hacking Village](car-hacking-village.md) is the venue; the firmware-analysis workflow connects to [reversing a brake ECU firmware update](reversing-a-brake-ecu-firmware-update.md).

## Limits and safety notes

This is a transcript of a 2023 talk, not a written advisory: there is no CVE, no fixed-version table, and the "should have been fixed" claim is the speaker's from the stage. The exploit is a denial of service against an ECU in a controlled bench setup; the overflow bytes are mostly driver struct fields, so it is not a general arbitrary-write primitive. Reproducing it requires board access, JTAG or a debugger, and for the real ECU, a bench that simulates the rest of the car. No hardware was exercised for this page. As a defensive takeaway, treat protocol metadata as untrusted and check how your framework reports length fields.

## Status and sources

Checked 2026-11-17. **Published** — the talk was given at DEF CON 31 (2023) and the caption transcript is archived by DEF CON.

- [Caption transcript](https://media.defcon.org/DEF%20CON%2031/DEF%20CON%2031%20villages/DEF%20CON%2031%20villages%20captions/DEF%20CON%2031%20-%20Car%20Hacking%20Village%20-%20Abusing%20CAN%20Bus%20Protocol%20Specification%20for%20Denial%20of%20Service%20in%20Embedded%20Systems%20-%20Martin%20Petran.eng.txt)

## Related

- [CANflict: exploiting peripheral conflicts for data-link layer attacks on automotive networks](canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks.md)
- [Error handling of in-vehicle networks makes them vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md)
- [Car Hacking Village](car-hacking-village.md)
- [The Vehicle May Be Sick: Denial of Diagnostic Services by Exploiting the CAN Transport Protocol](the-vehicle-may-be-sick-denial-of-diagnostic-services-by-exploiting-the-can-transport-protocol.md)
- [CAN availability and denial of service](concepts/can-availability.md)
