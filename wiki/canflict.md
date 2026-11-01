---
title: "CANflict"
summary: "C library that manipulates the CAN bus at the data link layer from an unmodified microcontroller, abusing pin conflicts between peripherals to craft…"
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/necst/CANflict"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "C library that manipulates the CAN bus at the data link layer from an unmodified microcontroller, abusing pin conflicts between peripherals to craft polyglot frames; the implementation behind the CCS 2022 paper."
related: [canter, canalyzat0r, caringcaribou]
license: GPL-3.0
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/necst/CANflict"
    retrieved: 2026-10-31
---

C library that manipulates the CAN bus at the data link layer from an unmodified microcontroller, abusing pin conflicts between peripherals to craft polyglot frames; the implementation behind the CCS 2022 paper.

## What it is

A C library for reading and writing arbitrary bits on a CAN bus at the
data-link layer from an *unmodified* microcontroller — only a CAN
transceiver is needed. By de Faveri Tron, Longari, Carminati, Polino, and
Zanero (Politecnico di Milano's NECST lab and Vrije Universiteit
Amsterdam); it is the implementation behind the ACM CCS 2022 paper. GPL-3.0.

## How it works

CANflict exploits a *pin conflict*: when a target MCU's CANRX/CANTX pin is
shared with another peripheral's signal, that peripheral (SPI, UART, I2C,
ADC) — or plain timer/busy-wait bitbanging — is driven to craft or
suppress bits the CAN controller itself would never emit. The code is
layered: techniques in `senders/` and `receivers/` over an abstract
peripheral interface, with platform-specific code underneath. This is the
mechanism class behind the [CAN injection](concepts/can-injection.md)
attack at the data-link layer: frames the bus accepts but no legitimate
controller sent.

## Where it fits

Research into data-link-layer attacks — the repository's tests include
targeted denial of service and full-frame spoofing experiments — and
evaluation of intrusion detection. [CANter](canter.md) was built
specifically to detect this attack class.

## Limits and notes

The technique requires a suitable pin conflict to exist on the target —
no conflict, no technique. Only two platforms are implemented: the AURIX
TC399XP starter kit and the LPCXpresso LPC11C24, and experiments need
vendor libraries (Infineon iLLD / MCUXpresso) and vendor flashing tools.
The UART and I2C techniques impose constraints on real CAN data; the repo
ships a compatibility analysis against the ReCAN dataset.

## Related

- [CANter](canter.md) — the IDS built to detect drop-and-spoof attacks like this.
- [CANalyzat0r](canalyzat0r.md) — GUI analysis for the buses CANflict targets.
- [CaringCaribou](caringcaribou.md) — higher-layer exploration, for contrast.
