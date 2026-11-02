---
title: "CANalyse"
summary: "Vehicle network analysis tool with SQL-like queries on CAN data, smart signal scanning, and Telegram bot integration."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/canalyse/CANalyse-2.0"
status: archived
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Vehicle network analysis tool with SQL-like queries on CAN data, smart signal scanning, and Telegram bot integration."
related: [can-utils, savvycan, canarchy]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/canalyse/CANalyse-2.0"
    retrieved: 2026-10-31
---

Vehicle network analysis tool with SQL-like queries on CAN data, smart signal scanning, and Telegram bot integration.

## What it is

A Python tool (Python 3.8+, installed from PyPI as `canalyse`) for
analysing vehicle CAN networks. **The GitHub repository is archived** —
treat it as unmaintained unless a successor is identified; this page's
`status: archived` records that.

## How it works

An interactive menu/REPL interface — also drivable through a Telegram bot —
that treats captures as dataframes. It scans and logs on a SocketCAN
channel, reads and writes logs in ASC, BLF, TRC, MF4, SQLite, CSV, and LOG
formats, and runs SQL-like queries over the capture via pandasql (for
example, selecting frames by ID with a `WHERE` clause). A "smart scan"
separates signal-bearing messages from noise, and it can replay captures,
export/import sessions, and fuzz by randomly modifying data bytes of
captured messages.

## Where it fits

Offline, query-driven exploration of captures: slicing large logs by ID or
field with SQL instead of writing parser code, and generating quick fuzz
variants from a captured dataframe. Maintained alternatives for the same
bench are [CANarchy](canarchy.md) for scripted analysis and
[SavvyCAN](savvycan.md) for GUI work.

## Limits and notes

The README states the tool is "made available for research purposes only"
and that users are solely responsible for legal compliance and obtaining
permission. It needs real CAN hardware (e.g. USBtin) or a virtual CAN
interface, and the archived repository means no fixes should be expected.

## Related

- [can-utils](can-utils.md) — produces and consumes the same log formats.
- [SavvyCAN](savvycan.md) — maintained GUI alternative for capture analysis.
- [CANarchy](canarchy.md) — maintained, script-first analysis toolkit.
