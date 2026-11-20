#!/usr/bin/env python3
"""Curated navigation taxonomy for this KB.

Three small, hand-maintained vocabularies sit behind the generated indexes:

* ``FACETS`` — cross-cutting topics. A page's ``facets:`` frontmatter is
  backfilled with the matching slugs; the ingester turns them into
  ``wiki/index-facet-*.md`` pages. Facets are deliberately *not* categories:
  their job is to cut across the 17 list sections (e.g. "CAN" appears under
  tools, papers, datasets and hardware).
* ``GLOSSARY`` — acronym/standard expansions, linked to the page that best
  explains them. Source for the generated ``wiki/index-glossary.md``.
* ``CONCEPT_CLUSTERS`` / ``READING_PATHS`` — the shape of the concept layer.
  Source for the generated ``wiki/index-concept-map.md``.

Pure data plus pure functions: no I/O, no wall clock, so generated output
stays byte-deterministic for a given source commit.
"""

from __future__ import annotations

import re
from typing import NamedTuple


class Facet(NamedTuple):
    slug: str
    label: str
    description: str
    patterns: tuple[str, ...]


FACETS: tuple[Facet, ...] = (
    Facet("can", "CAN", "Controller Area Network, CAN FD, CAN XL and SocketCAN.",
          (r"(?-i:\bCAN\b)", r"\bcan[- ]?(?:bus|fd|xl)\b", r"\bcanaly[sz]",
           r"\bcanmatic\b", r"\bsocketcan\b", r"python[- ]can\b",
           r"\bcan frames?\b")),
    Facet("diagnostics", "Diagnostics", "UDS, OBD, KWP, SecurityAccess and diagnostic services.",
          (r"\buds\b", r"iso[\s-]?14229", r"\bobd(?:-ii|-2)?\b", r"diagnos",
           r"\bkwp\b", r"\bsovd\b", r"security\s?access", r"seed[\s/-]?key")),
    Facet("iso-tp", "ISO-TP", "ISO 15765-2 transport, segmentation and flow control.",
          (r"iso[\s-]?tp", r"iso[\s-]?15765", r"multi[\s-]?frame", r"flow[\s-]?control",
           r"can transport protocol")),
    Facet("doip", "DoIP", "Diagnostics over IP and its discovery/routing boundary.",
          (r"\bdoip\b", r"diagnostics over ip")),
    Facet("xcp", "XCP / A2L", "Measurement and calibration, XCP and A2L description files.",
          (r"\bxcp\b", r"\ba2l\b", r"calibrat", r"measurement and calibration")),
    Facet("j1939", "J1939", "Heavy-vehicle J1939 request and transport semantics.",
          (r"\bj1939\b", r"tp\.cm", r"tp\.dt")),
    Facet("lin", "LIN", "The subordinate LIN bus behind gateways.",
          (r"\blin\b(?!ux|usbconverter)", r"local interconnect network")),
    Facet("ethernet", "Automotive Ethernet", "100/1000BASE-T1, MACsec and in-vehicle IP networking.",
          (r"automotive ethernet", r"\b100base-t1\b", r"\bmacsec\b", r"in-vehicle network(?:ing)?",
           r"ethernet")),
    Facet("someip", "SOME/IP", "AUTOSAR service-oriented middleware and service discovery.",
          (r"some/?ip", r"\bsd\b.*servic", r"service discovery")),
    Facet("firmware", "Firmware & updates", "Firmware acquisition, bootloaders, flashing and OTA updates.",
          (r"firmware", r"bootloader", r"\bflash", r"\bota\b", r"over[\s-]?the[\s-]?air",
           r"uptane", r"software update", r"reverse[\s-]?engineer", r"\bghidra\b",
           r"checksum tool")),
    Facet("rf-keys", "RF & keys", "Key fobs, RKE/PKE, rolling codes, TPMS and radio tooling.",
          (r"key[\s-]?fob", r"\brke\b", r"\bpke\b", r"passive keyless",
           r"remote keyless", r"rolling code", r"immobiliz", r"\btpms\b",
           r"\brf\b", r"radio", r"proxmark", r"flipper", r"rtl[\s_-]?433", r"urh\b")),
    Facet("ev-charging", "EV charging", "EVSE, ISO 15118, OCPP, V2G, CCS and PLC.",
          (r"\bevse\b", r"ev[\s-]?charg", r"\bocpp\b", r"iso[\s-]?15118", r"din[\s-]?70121",
           r"\bv2g\b", r"\bccs\b", r"plug.?and.?charge", r"\bplc\b", r"\bev\b")),
    Facet("v2x", "V2X", "Vehicle-to-everything, pseudonym credentials and misbehaviour reporting.",
          (r"\bv2x\b", r"c-v2x", r"\bdsrc\b", r"vanet", r"\bscms\b", r"\bccms\b",
           r"misbehavio", r"pseudonym", r"vehicular communication")),
    Facet("ivi", "IVI", "Infotainment and head-unit runtime and update trust.",
          (r"infotainment", r"\bivi\b", r"head[\s-]?unit", r"\bmmi3g\b", r"\bidrive\b",
           r"\bchimaera\b")),
    Facet("sensors", "Sensors & perception", "LiDAR, camera, radar, GNSS and physical-channel attacks.",
          (r"\blidar\b", r"\bcamera\b", r"\bradar\b", r"\bgps\b", r"\bgnss\b",
           r"perception", r"sensor", r"accelerometer", r"thermal imag", r"navigation")),
    Facet("hardware", "Hardware", "Debug ports, boards, adapters and bench interfaces.",
          (r"\bjtag\b", r"\bdebug\b", r"logic analyzer", r"hardware interface",
           r"development board", r"\bcan[\s-]?tact\b", r"candlelight", r"\bpanda\b")),
    Facet("simulation", "Simulation", "Virtual buses, replay, SIL/HIL and physical miniatures.",
          (r"simulat", r"\bsil\b", r"\bhil\b", r"testbed", r"digital twin", r"\btwin\b",
           r"\breplay\b", r"\bicsim\b", r"\bramn\b", r"virtual ecu")),
    Facet("authentication", "Authentication & keys", "Message authentication, SecOC, key management and shared secrets.",
          (r"authenticat", r"\bsecoc\b", r"message authentication", r"key management",
           r"\bcredential", r"\bsecrets?\b", r"shared secret", r"default secret",
           r"\bcrypto", r"\bmac\b")),
    Facet("ids", "Intrusion detection", "IDS, ECU fingerprinting and anomaly attribution.",
          (r"intrusion detection", r"\bids\b", r"fingerprint", r"anomaly detection",
           r"attack detection", r"detection system")),
    Facet("tara", "TARA", "Threat analysis and risk assessment, ISO/SAE 21434.",
          (r"\btara\b", r"threat (?:analysis|model)", r"risk assessment", r"21434",
           r"threat matrix", r"security requirement")),
    Facet("attack", "Attack techniques", "Exploits, fuzzing, injection, spoofing and bypasses.",
          (r"\battack", r"exploit", r"\bfuzz", r"\bbypass", r"\bhijack", r"\bspoof",
           r"\bjam(?:ming)?\b", r"injection", r"\bbrute", r"\bglitch", r"vulnerab")),
    Facet("defense", "Defense & architecture", "Mitigations, secure design, segmentation and standards compliance.",
          (r"mitigat", r"defen[cs]e", r"secure (?:boot|design|architecture|development)",
           r"segmentation", r"security architecture", r"\bhardening\b", r"best practice")),
    Facet("tools", "Tools & libraries", "Software, toolkits and libraries you can run.",
          (r"\btool(?:kit|s)?\b", r"\blibrary\b", r"\bframework\b", r"\bpython\b",
           r"\butility\b", r"\butilities\b", r"\bsimulator\b", r"github.com/")),
    Facet("research", "Research", "Papers, surveys and conference presentations.", ()),
    Facet("learning", "Learning", "Books, guides, courses and meta-lists.", ()),
    Facet("datasets", "Datasets", "Captures, benchmarks and labelled datasets.", ()),
    Facet("standards", "Standards & specs", "ISO, SAE, AUTOSAR, UNECE and published specifications.",
          (r"iso[\s/]?sae", r"\biso[\s-]?\d", r"\bsae\s?j\d", r"\bautosar\b",
           r"\bunece\b", r"wp\.?29", r"\br155\b", r"specification")),
)

FACET_BY_SLUG = {f.slug: f for f in FACETS}

KIND_BY_CATEGORY = {
    "Research Papers": ("research",),
    "Conference Presentations": ("research",),
    "Books": ("learning",),
    "Learning Resources": ("learning",),
    "Related Awesome Lists": ("learning",),
    "Datasets": ("datasets",),
}

# Only these sections are tool-like enough to get `tools` without a keyword.
TOOL_CATEGORIES = {
    "CAN Bus Analysis", "Diagnostic Tools", "Firmware and ECU Reverse Engineering",
    "Automotive Ethernet", "RF and Key Fob Analysis", "Infotainment and IVI",
    "V2X Security", "EV Charging Security", "Hardware Interfaces",
    "Penetration Testing",
}


def assign_facets(text: str, category: str = "") -> tuple[str, ...]:
    """Return the facet slugs matching ``text``, in declared FACETS order.

    ``text`` should be the title + summary + lead paragraph: enough context to
    classify, short enough that incidental mentions in a deep body do not
    create false positives. The two keyword-free kind facets (research,
    learning) and the dataset kind come from the list section instead.
    """
    found = set(KIND_BY_CATEGORY.get(category, ()))
    if category in TOOL_CATEGORIES:
        found.add("tools")
    for facet in FACETS:
        if not facet.patterns:
            continue
        if any(re.search(p, text, re.IGNORECASE) for p in facet.patterns):
            found.add(facet.slug)
    return tuple(f.slug for f in FACETS if f.slug in found)


class GlossaryEntry(NamedTuple):
    term: str
    expansion: str
    target: str  # page slug, relative to wiki/ (may be "concepts/<slug>")
    note: str


GLOSSARY: tuple[GlossaryEntry, ...] = (
    GlossaryEntry("CAN", "Controller Area Network", "concepts/can-injection",
                  "The in-vehicle bus whose frames carry no sender identity."),
    GlossaryEntry("CAN FD / CAN XL", "CAN with Flexible Data-rate / extra Long", "a-formal-security-analysis-of-can-xl",
                  "Faster and larger-frame generations of CAN; the security substrate is unchanged."),
    GlossaryEntry("ECU", "Electronic Control Unit", "concepts/bootloader-stages",
                  "A vehicle's embedded computer — the unit whose firmware and boot chain are in scope."),
    GlossaryEntry("UDS", "Unified Diagnostic Services (ISO 14229)", "concepts/uds-seed-key",
                  "The highest-privilege diagnostic service set; 0x27 gates privileged access."),
    GlossaryEntry("SecurityAccess", "UDS service 0x27 (seed/key)", "concepts/uds-seed-key",
                  "The challenge-response gate in front of privileged diagnostics."),
    GlossaryEntry("ISO-TP", "ISO 15765-2 transport protocol", "concepts/iso-tp",
                  "Reassembles multi-frame diagnostic payloads on CAN; its flow control is attackable."),
    GlossaryEntry("DoIP", "Diagnostics over Internet Protocol", "concepts/doip",
                  "Moves diagnostics from the OBD port to a routable endpoint."),
    GlossaryEntry("OBD-II", "On-Board Diagnostics II", "concepts/diagnostic-service-abuse",
                  "The legally mandated diagnostic port and its service set."),
    GlossaryEntry("DBC", "Database CAN", "concepts/dbc-semantic-layer",
                  "The file that names CAN IDs and decodes signals — a human claim, not ground truth."),
    GlossaryEntry("XCP", "Universal Measurement and Calibration Protocol", "concepts/calibration-plane",
                  "Direct memory access into a running ECU, described by an A2L file."),
    GlossaryEntry("A2L", "ASAM MCD-2 MC description file", "concepts/calibration-plane",
                  "Names the memory objects XCP can reach."),
    GlossaryEntry("SOME/IP", "Scalable service-Oriented MiddlewarE over IP", "concepts/someip",
                  "AUTOSAR's service middleware; service discovery is its trust root."),
    GlossaryEntry("J1939", "SAE J1939", "concepts/j1939",
                  "Heavy-vehicle CAN application and transport layer with its own attackable state."),
    GlossaryEntry("LIN", "Local Interconnect Network", "concepts/lin-bus",
                  "A cheap subordinate bus often treated as trusted because it sits behind a gateway."),
    GlossaryEntry("SecOC", "Secure Onboard Communication", "concepts/can-message-authentication",
                  "AUTOSAR's authenticated CAN framing; freshness and key scope still matter."),
    GlossaryEntry("MACsec", "Media Access Control Security", "what-is-automotive-macsec",
                  "Link-layer encryption/authentication for Automotive Ethernet."),
    GlossaryEntry("IDS", "Intrusion Detection System", "concepts/in-vehicle-intrusion-detection",
                  "Detects in-vehicle anomalies via timing, skew, voltage or learned models."),
    GlossaryEntry("IVI", "In-Vehicle Infotainment", "concepts/ivi-runtime-privilege",
                  "The head unit and the apps/services it hosts."),
    GlossaryEntry("OTA", "Over-the-Air update", "concepts/secure-firmware-updates",
                  "Remote software delivery; Uptane is the reference design for securing it."),
    GlossaryEntry("Uptane", "A compromise-resilient update framework", "concepts/secure-firmware-updates",
                  "Two repositories and per-vehicle signed instructions for automotive OTA."),
    GlossaryEntry("TARA", "Threat Analysis and Risk Assessment", "concepts/tara-methodology",
                  "The ISO/SAE 21434 artefact chain from item definition to risk treatment."),
    GlossaryEntry("ISO/SAE 21434", "Road vehicles — Cybersecurity engineering", "concepts/tara-methodology",
                  "The process standard whose artefacts a TARA produces."),
    GlossaryEntry("UNECE R155", "UN regulation on vehicle cybersecurity", "automotive-cybersecurity-an-introduction-to-iso-sae-21434",
                  "Requires a certified CSMS for type approval in many markets."),
    GlossaryEntry("OCPP", "Open Charge Point Protocol", "concepts/ocpp-charging-attacks",
                  "Links chargers to backends; weak transport and shared identities enable fraud."),
    GlossaryEntry("ISO 15118", "Vehicle-to-Grid communication interface", "concepts/charging-trust-chain",
                  "The EV–EVSE protocol behind Plug & Charge."),
    GlossaryEntry("DIN 70121", "German DC charging communication profile", "concepts/charging-trust-chain",
                  "The predecessor profile to ISO 15118 for DC charging."),
    GlossaryEntry("V2G", "Vehicle-to-Grid", "openv2g",
                  "Bidirectional energy and communication between vehicle and charger."),
    GlossaryEntry("CCS", "Combined Charging System", "concepts/charging-trust-chain",
                  "The dominant DC charging connector and communication stack."),
    GlossaryEntry("V2X", "Vehicle-to-Everything", "concepts/v2x-credential-management",
                  "Vehicle communication with other vehicles, infrastructure and pedestrians."),
    GlossaryEntry("SCMS", "Security Credential Management System", "concepts/v2x-credential-management",
                  "The US split-knowledge issuer of pseudonymous V2X tickets."),
    GlossaryEntry("CCMS", "Cooperative Credential Management System", "concepts/v2x-credential-management",
                  "The European equivalent of the SCMS."),
    GlossaryEntry("RKE / PKE", "Remote / Passive Keyless Entry", "concepts/key-fob-relay-attacks",
                  "The fob-to-car link targeted by relay and rolling-code attacks."),
    GlossaryEntry("Rolling code", "A hopping code tied to receiver counter state", "concepts/rolling-code-failure-classes",
                  "Trust lives in the counter's state, so attacks target windows, resync and blocking."),
    GlossaryEntry("TPMS", "Tire Pressure Monitoring System", "security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study",
                  "A wireless sensor network inside the vehicle with its own attack surface."),
    GlossaryEntry("SIL / HIL", "Software-/Hardware-in-the-Loop", "concepts/simulation-and-test-doubles",
                  "Simulation rungs that trade physical fidelity for repeatability."),
    GlossaryEntry("OEM", "Original Equipment Manufacturer", "concepts/ivi-update-trust",
                  "The vehicle maker; Tier-1 suppliers build many of the components."),
)


class Cluster(NamedTuple):
    slug: str
    label: str
    description: str
    concepts: tuple[str, ...]


CONCEPT_CLUSTERS: tuple[Cluster, ...] = (
    Cluster("bus", "The bus and its protocols",
            "What the in-vehicle networks say, and how their assumptions fail.",
            ("can-injection", "can-availability", "dbc-semantic-layer", "can-message-authentication",
             "in-vehicle-intrusion-detection", "lin-bus", "j1939", "iso-tp")),
    Cluster("access", "Access, diagnostics and updates",
            "The privileged paths into an ECU, and where their gates break.",
            ("diagnostic-service-abuse", "uds-seed-key", "diagnostic-fuzzing",
             "calibration-plane", "firmware-acquisition", "bootloader-stages",
             "secure-firmware-updates", "ivi-update-trust", "ivi-runtime-privilege")),
    Cluster("boundary", "The external boundary",
            "Where the vehicle meets the radio, the charger and the road.",
            ("external-attack-surface", "key-fob-relay-attacks", "rolling-code-failure-classes",
             "shared-and-default-secrets", "charging-trust-chain", "ocpp-charging-attacks",
             "v2x-credential-management", "misbehavior-detection", "physical-channel-sensor-attacks",
             "someip", "doip")),
    Cluster("method", "Method and evidence",
            "How the work is modelled, simulated and reasoned about.",
            ("tara-methodology", "simulation-and-test-doubles")),
)


class ReadingPath(NamedTuple):
    title: str
    description: str
    steps: tuple[str, ...]


READING_PATHS: tuple[ReadingPath, ...] = (
    ReadingPath("Steal the car without the key",
                "From physical access to a forged status claim, then the defences proposed against it.",
                ("can-injection", "rolling-code-failure-classes", "key-fob-relay-attacks",
                 "can-message-authentication", "in-vehicle-intrusion-detection")),
    ReadingPath("Own the ECU",
                "The privileged path: get access, get the image, understand the boot chain, break the update.",
                ("diagnostic-service-abuse", "uds-seed-key", "firmware-acquisition",
                 "bootloader-stages", "secure-firmware-updates", "ivi-update-trust")),
    ReadingPath("Plug in and pivot",
                "Charging and V2X as trust chains rather than single protocols.",
                ("charging-trust-chain", "ocpp-charging-attacks", "v2x-credential-management",
                 "misbehavior-detection", "external-attack-surface")),
    ReadingPath("Speak the protocol",
                "The semantic layers that turn bytes and timing into meaning — and into attack surface.",
                ("dbc-semantic-layer", "iso-tp", "j1939", "lin-bus", "someip", "calibration-plane")),
)
