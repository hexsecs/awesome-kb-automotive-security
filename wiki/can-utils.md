---
uid: 01a19d3c-af41-7b3d-89a5-17daea154405
title: "can-utils"
summary: "Linux-CAN SocketCAN userspace utilities including cansniffer, candump, cansend, canplayer, and cangen for CAN bus analysis."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/linux-can/can-utils"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Linux-CAN SocketCAN userspace utilities including cansniffer, candump, cansend, canplayer, and cangen for CAN bus analysis."
related:
  - python-can
  - cannelloni
  - pretty-j1939
  - cangaroo
  - autopi
  - can-injection
  - canarchy
  - canvas-fast-and-inexpensive-automotive-network-mapping
  - car-toolkit
  - carpunk
  - icsim
  - lindwurm
  - piccante
  - savvycan
  - uds-firmware-extraction
  - udsim
  - canalyse
  - iso-tp
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/linux-can/can-utils"
    retrieved: 2026-10-31
facets: [can, tools]
---

Linux-CAN SocketCAN userspace utilities including cansniffer, candump, cansend, canplayer, and cangen for CAN bus analysis.

## What it is

The Linux-CAN project's userspace utilities for SocketCAN — the standard
command-line toolkit that ships with the Linux CAN subsystem, maintained
under the linux-can GitHub organisation.

## How it works

A suite of small single-purpose C programs over the kernel's SocketCAN
sockets, grouped by function:

- **Basic traffic** — candump, cansend, canplayer, cangen, cansequence,
  and cansniffer (which highlights payload differences between successive
  frames);
- **Network access** — canlogserver, bcmserver, socketcand;
- **Gatewaying** — cangw, configuring the in-kernel CAN gateway;
- **Measurement and test** — canbusload, canfdtest, canerrsim, and a
  bit-timing calculator;
- **ISO-TP** — isotpsend, isotprecv, isotpsniffer, isotpdump, isotpserver,
  isotpperf, isotptun;
- **J1939 / ISOBus** — j1939spy, j1939cat, j1939sr, an address-claim
  daemon, and an ISOBus file server;
- **Log conversion** — asc2log, log2asc, log2long; plus slcan
  line-discipline setup.

The [project README](https://github.com/linux-can/can-utils), checked
2026-11-17, distinguishes displaying a frame, recording it, and replaying
it: `candump` filters and logs received traffic, `canplayer` consumes CAN
logfiles, and `cansend` transmits one frame. A useful bench workflow is
therefore to preserve a baseline capture before selecting a small set of
frames for controlled replay. `cansniffer` answers a different question:
which payload contents changed, rather than what those bytes mean.
The compact log representation can be converted to ASC and back; the
human-readable long representation is another output, not a signal database.

At the transport layer, the ISO-TP programs operate on protocol data
units: `isotpsend` sends one PDU and `isotprecv` receives PDUs.
`isotpdump` instead interprets the underlying CAN messages through CAN_RAW;
`isotpsniffer` observes reassembled PDUs. This distinction matters when
debugging a fragmented diagnostic exchange: seeing individual frames is
not the same as obtaining the complete application payload.
J1939 tools add address claiming and J1939-oriented send/receive paths,
while `cangw` configures kernel forwarding rather than acting as a
DBC-aware application gateway.

## Where it fits

Scripted capture, replay, and generation on any Linux bench — and the
candump log format it produces is the interchange format most other tools
in this section consume, including [python-can](python-can.md) pipelines
and [pretty_j1939](pretty-j1939.md) decoding. Remote benches pair it with
[cannelloni](cannelloni.md) tunnels.

## Limits and notes

Linux/SocketCAN only; there is no Windows or macOS path. The README states
no usage-safety guidance. Note that cangen generates random traffic by
design — it is an active-transmit tool, not a passive listener.

The toolkit does not supply vehicle-specific signal meanings, discover a
DBC, or establish that a replayed command is safe. Hardware access still
depends on a working SocketCAN interface and the appropriate kernel
protocol support; having an ISO-TP utility is not a complete UDS client.

## Related

- [python-can](python-can.md) — the library form of the same SocketCAN world.
- [cannelloni](cannelloni.md) — tunnels SocketCAN interfaces over IP networks.
- [pretty_j1939](pretty-j1939.md) — decodes J1939 traffic from candump logs.
- [CANalyse](canalyse.md)

For the conceptual boundary between observing traffic and transmitting
it, see [CAN injection](concepts/can-injection.md). For segmentation and
reassembly above individual frames, see [ISO-TP](concepts/iso-tp.md).
