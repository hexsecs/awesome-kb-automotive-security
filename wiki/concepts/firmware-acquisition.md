---
title: "Firmware acquisition: the read-side channels"
summary: "Before analysis comes acquisition: the channels the corpus documents for getting an ECU's image out — by bus, by bootstrap, by bench, by log, by package."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [tc1791-can-bsl, pq-flasher, conescan, uds-firmware-extraction, vw-flash, secoc-key-extractor, reversing-a-brake-ecu-firmware-update, secure-firmware-updates, bootloader-stages]
sources:
  - url: "https://github.com/bri3d/CCM19XX-CCP-Flashing"
    retrieved: 2026-11-01
  - url: "https://github.com/abrignoni/UDSFirmwareExtraction"
    retrieved: 2026-11-01
---

Every analysis in this KB's firmware corpus starts from an artifact someone first had to *get*: an ECU's flash image, a calibration block, an update package's plaintext. The update-trust concepts ([secure firmware updates](secure-firmware-updates.md), [IVI update trust](ivi-update-trust.md)) cover the delivery direction — what a vehicle accepts. This page covers the read direction: the acquisition channels the corpus documents, organised by where the acquirer has to be (on the bus, at a bench, holding a log, holding a package) and by what each channel yields and what gate it must pass. The channel choice is usually forced by the research question — a differential patch analysis needs both sides of a change; a key-recovery project needs the bytes the keys live in — and each channel's preconditions quietly determine which ECUs are researchable at all.

## Diagnostic transfer (on the bus)

The front door: UDS/CCP read services against a live ECU. [pq-flasher](../pq-flasher.md) dumps engine-ECU flash and calibration areas over the CCP diagnostic protocol; [ConeScan](../conescan.md) reads and dumps via a J2534 PassThru device. Preconditions: bus access and whatever the read path is gated by — seed/key where the manufacturer locked reads (the [uds-seed-key](uds-seed-key.md) page's subject), a diagnostic session, sometimes a specific attachment point behind a gateway. Yield: what the diagnostic surface chooses to expose — often the application and calibration regions, rarely the bootloader, and always at the ECU's chosen granularity rather than the flash chip's.

## Factory bootstrap loaders (bus or bench pins)

Microcontrollers ship with a ROM bootstrap loader for factory programming, and it reads as well as writes when its password gate allows. The [TC1791 CAN BSL](../tc1791-can-bsl.md) page documents the canonical case: the TriCore bootstrap speaks over CAN, and its 32-bit boot password is the whole gate — unprotected parts yield their flash to a bus-attached tool, protected ones refuse until the password is recovered or the part is reached another way. This channel's yield is the full flash as the silicon sees it, boot region included — which is precisely the region diagnostic transfer withholds.

## Bench extraction (physical access)

When no logical channel opens, the acquirer goes to the board: debug and background-debug interfaces, chip-off reads, test pads. The corpus's fullest worked example is [Reversing a Brake ECU Firmware Update](../reversing-a-brake-ecu-firmware-update.md): the production image came from a **BDM dump** of the S12X — possible because read-out protection, though supported by the part, was **not enabled** — and the BDM channel doubled as a live runtime-state probe and, in reverse, a back-flash path. The precondition is the most expensive in the set (physical possession, board skill, sometimes destructive work), and the yield is the most complete: raw flash with no diagnostic-surface curation. [secoc-key-extractor](../secoc-key-extractor.md) is the pattern in miniature: bench acquisition as the enabling prior step, extracting the SecOC keys that make later bus work possible.

## Captured-session reassembly (a log, no vehicle)

The channel with the strangest preconditions: [uds-firmware-extraction](../uds-firmware-extraction.md) reconstructs a firmware image by parsing a **captured flashing session** from a CAN log — TransferData blocks reassembled into the image they carried. No live vehicle is required at analysis time; the precondition is having (or being given) a log of someone else's update. Its yield has a characteristic blind spot, named by the brake-ECU work: a capture contains only the blocks the updater actually wrote — regions the update skipped (typically the bootloader and vector areas) are absent, so capture and dump are complementary channels with opposite coverage, and the differential work in that paper needed both, each from a different channel.

## Update-package decryption (a file, no vehicle)

The last channel never touches hardware at analysis time: the manufacturer has already shipped the firmware, encrypted or containerised, in an update package. [VW_Flash](../vw-flash.md) ships an ODX extractor that unpacks Volkswagen's update containers to plaintext. Preconditions: obtaining the package (dealer channels, update servers, a prior capture) and the container's keys or format — which is why this channel pairs with the update-trust concepts: the same package whose *installation* the trust concepts audit is, once decrypted, an *acquisition* artifact. Yield: exactly what the update contains — application images, rarely bootloaders, never per-vehicle data.

## The pattern across channels

Three observations the individual pages support jointly. **Gates concentrate on the cheap channels:** the bus and bootstrap channels carry the authentication (seed/key, boot passwords); the log and package channels carry none — their precondition is possession of the artifact, which shifts the security question from the ECU to the distribution chain. **Yield and precondition trade off:** the most complete image (bench dump) costs physical access; the cheapest channels (log, package) yield partial images with structurally missing regions. **Acquisition is the corpus's silent dependency:** Beneath the Bonnet's extracted ciphers, the SecOC key work, the brake-ECU differential — each downstream result names its acquisition channel only in passing, yet the channel determined what could be concluded. Reading any firmware result in this KB, the first question is which channel produced the image, because the channel is the result's sampling frame.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source.

## Related

- [TC1791 CAN BSL](../tc1791-can-bsl.md) — the factory bootstrap channel and its password gate
- [pq-flasher](../pq-flasher.md) and [ConeScan](../conescan.md) — diagnostic-transfer dumping
- [UDS firmware extraction](../uds-firmware-extraction.md) — reassembly from a captured session
- [VW_Flash](../vw-flash.md) — the update-package channel
- [Reversing a Brake ECU Firmware Update](../reversing-a-brake-ecu-firmware-update.md) — capture and BDM as complementary channels
- [Secure firmware updates](secure-firmware-updates.md) — the delivery direction this page mirrors
