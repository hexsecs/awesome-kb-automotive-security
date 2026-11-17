---
uid: 01a1ba7a-e331-70bc-8880-11c08f5e6dc8
title: "idrive7-8-ssh-root"
summary: "Enable root SSH on BMW iDrive 7/8 MGU head units over ENET via debug image flash and persistent SSH without B7F8E5 DTC, for head unit reverse engineering."
type: entity
category: "Infotainment and IVI"
url: "https://github.com/cauliflowermossgrape/idrive7-8-ssh-root"
status: active
last_checked: 2026-11-17
created: 2026-11-08
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 825c8e5
list_summary: "Enable root SSH on BMW iDrive 7/8 MGU head units over ENET via debug image flash and persistent SSH without B7F8E5 DTC, for head unit reverse engineering."
related:
  - mmi3g-toolkit
  - byd-dolphin-hacking
  - vw-flash
  - gen5fw
  - automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps
  - bypassing-debug-password-protection-on-the-rh850-family
  - ivi-runtime-privilege
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-08
  - url: "https://github.com/cauliflowermossgrape/idrive7-8-ssh-root"
    retrieved: 2026-11-17
  - url: "https://raw.githubusercontent.com/cauliflowermossgrape/idrive7-8-ssh-root/main/README.md"
    retrieved: 2026-11-17
  - url: "https://api.github.com/repos/cauliflowermossgrape/idrive7-8-ssh-root"
    retrieved: 2026-11-17
---

Enable root SSH on BMW iDrive 7/8 MGU head units over ENET via debug image flash and persistent SSH without B7F8E5 DTC, for head unit reverse engineering.

## What it is

A tool for enabling persistent root SSH on BMW MGU head units (iDrive 7 / MGU ID7, ID8-BDC3 and ID8-BCP) purely over the car's ENET diagnostic interface — an ENET cable and a laptop, nothing wireless. It flashes a small debug package built for the unit's VIN, enrolls an SSH identity through BMW diagnostic routines, and then makes SSH survive with debug mode switched off so the `B7F8E5` "debugging active" DTC clears. It ships as a Python CLI, a Tkinter GUI and a standalone Windows `.exe`, and is released into the public domain under The Unlicense.

## How it works

The one-time `flash` writes a roughly 131 KB debug package (a development CA certificate plus debug-mode binaries) and then enrolls the identity using four diagnostic routines over ENET — a `31 01 A6 71` challenge, generated certificate, `31 01 A0 FD` install and `22 17 2A` readback, repeated five times before the SSH daemon comes up. Everything talks to a gateway at `169.254.254.36:6801` discovered by UDP broadcast; the head unit is later reached on a link-local `169.254.x.x` address, which is why a wired ENET connection is required both to flash and to connect. Status is read-only: software version, head-unit IP, the debug DTC and a probe of port 22.

The key handling is unusual and worth understanding before use. SSH authorisation is against one fixed key baked into the flashed debug image; enrollment installs a separate PMO-CA-signed certificate that is only the access gate for the A671/A0FD handshake, not a login key. The tool therefore writes out the baked key in OpenSSH, PEM, PPK and public formats under `data/enrollments/<VIN>/`. An optional, off-by-default per-car unique key is installed by logging in with the baked key, remounting the read-only rootfs briefly to write the real `AuthorizedKeysFile` (`/usr/share/sshd/authorized_keys.root`, not `~/.ssh/authorized_keys`), verifying, then removing the shared key — a one-way operation the README warns can lock you out.

Persistence addresses three separate stock gates: `sshd.socket` is only wanted by `debug.target`, has `PartOf=debug.target`, and port 22 is only accepted by a firewalld rule added while debug mode is on. An `/etc`-only override adds the other boot targets, drops the `PartOf` binding, and a keeper service holds a `tcp dport 22 accept` rule at the top of the nft input chains, rechecked every 15 s. If persistence fails, the tool deliberately leaves debug mode on rather than losing access.

## Where it fits

This is the practical entry point to MGU head-unit research — the kind of shell access that makes [MMI3G toolkit](mmi3g-toolkit.md), [BYD Dolphin hacking](byd-dolphin-hacking.md), [VW flash](vw-flash.md) and [Gen5FW](gen5fw.md) style work possible on BMW hardware. It is the IVI analogue of [bypassing debug password protection on the RH850 family](bypassing-debug-password-protection-on-the-rh850-family.md): both turn a vendor debug mechanism into a durable research foothold. For the wider traffic-capture workflow see [automated reverse engineering of CAN bus commands from mobile apps](automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps.md).

## Limits and safety notes

**Flashing is destructive.** The upstream README documents, on a real car, that flashing wipes the head unit's coding/CAFD definitions, deletes BMW Digital Key pairings (issue #13), and can brick the module; a full coding backup with BimmerCode or ISTA/E-Sys is required before the first run, and E-Sys recoding may be needed if a BimmerCode restore only partially succeeds. Only `flash` and `fix-key` carry this risk; `enable`, `persist`, `close`, `disable` and `status` do not reprogram. Run `flash` once — reflashing "to be safe" wipes coding again for no benefit; `enable` is the repair path when SSH merely stops answering. On some software levels port 22 opens but login is refused because `authorized_keys.root` holds a different key; `fix-key` reflashes the one unsigned region with this tool's key. NBT/EVO (iDrive 6 and older) is refused outright. Everything here is from the upstream README; no vehicle was flashed for this page, and this is a modification tool with real bricking risk, not a passive analysis tool.

## Status and sources

Checked 2026-11-17. **Active** at this check: public, not archived, Unlicense, 556 stars / 105 forks / 12 open issues, default branch last pushed 2026-11-13. Popularity is not a support guarantee.

- [Upstream README](https://raw.githubusercontent.com/cauliflowermossgrape/idrive7-8-ssh-root/main/README.md)
- [Repository metadata](https://api.github.com/repos/cauliflowermossgrape/idrive7-8-ssh-root)

## Related

- [MMI3G toolkit](mmi3g-toolkit.md)
- [BYD Dolphin hacking](byd-dolphin-hacking.md)
- [VW flash](vw-flash.md)
- [Gen5FW](gen5fw.md)
- [Automated cross-platform reverse engineering of CAN bus commands from mobile apps](automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps.md)
- [Bypassing debug password protection on the RH850 family](bypassing-debug-password-protection-on-the-rh850-family.md)
- [IVI runtime privilege and service exposure](concepts/ivi-runtime-privilege.md)
