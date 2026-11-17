---
uid: 01a19d3c-af24-7c5a-a39a-cdc4da65c7cd
title: "A Formal Security Analysis of CAN XL"
summary: "Tang et al., USENIX Security 2026. First formal security analysis of the CAN XL standard, showing it retains all known classic CAN MAC sub-layer flaws and…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity26/presentation/tang-zhaozhou"
status: published
last_checked: 2026-11-17
created: 2026-11-02
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: e9533c9
list_summary: "Tang et al., USENIX Security 2026. First formal security analysis of the CAN XL standard, showing it retains all known classic CAN MAC sub-layer flaws and adds seven new vulnerabilities, validated on commercial controllers."
related:
  - canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks
  - error-handling-of-in-vehicle-networks-makes-them-vulnerable
  - on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems
  - can-message-authentication
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-02
  - url: "https://www.usenix.org/conference/usenixsecurity26/presentation/tang-zhaozhou"
    retrieved: 2026-11-17
---

Tang et al., USENIX Security 2026. First formal security analysis of the CAN XL standard, showing it retains all known classic CAN MAC sub-layer flaws and adds seven new vulnerabilities, validated on commercial controllers.

## What it is

A paper by Zhaozhou Tang (Georgia Tech), Khaled Serag (Qatar Computing Research Institute), Z. Berkay Celik (Purdue), Vijay Ganesh, Saman Zonouz and Raheem Beyah (Georgia Tech), published at the 35th USENIX Security Symposium in Baltimore in August 2026, pp. 2227–2246. It is the first security analysis of the CAN XL standard, and it focuses specifically on the MAC sub-layer — the part of the stack that governs frame formats and error handling and has historically enabled most classic CAN (CAN CC) attacks. The question the authors ask is whether CAN XL's new security features are merely add-ons, or whether the standard redesign actually fixes CAN's chronic MAC-layer weakness.

## How it works

The authors build a **bit-precise formal model of CAN XL** and release it for future research, then apply a formal-analysis workflow guided by CAN XL's field-oriented structure to look for vulnerabilities. The published abstract reports the result plainly: CAN XL remains vulnerable to all known CAN CC MAC sub-layer issues and introduces **seven new vulnerabilities**, which the authors describe as arguably making security worse. They validate the findings on commercial CAN XL controllers and demonstrate exploitability with two multi-stage attacks on a testbed simulating real vehicle traffic. Their mitigations include formally verifying revisions of the standard, which would have prevented several of the attacks.

The motivation is the industry transition now underway: modern vehicles add cameras, LiDARs and AI components that strain classic CAN's bandwidth and functionality, so CAN XL is being positioned as the next generation with longer payloads, higher bandwidth and enhanced security. The paper's point is that the security posture of the new MAC sub-layer needs to be understood before widespread deployment, not after.

## Where it fits

This is the formal, standard-level counterpart to the practical MAC-layer work in [CANflict](canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks.md) and to [error handling of in-vehicle networks makes them vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md); both show the same layer being abused from the bench rather than by model checking. [On the real-world applicability of automotive CAN intrusion detection systems](on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems.md) is the detection-side question that follows from a finding that the new standard inherits the old attacks. It also connects to the DLC-field discussion in [abusing CAN bus protocol specification for denial of service](abusing-can-bus-protocol-specification-for-denial-of-service-in-embedded-systems.md): that talk's speaker declined to judge CAN XL until real implementations existed, and this paper is the analysis he was waiting for.

## Limits and safety notes

This page is grounded in the official USENIX abstract and BibTeX record, not the full paper: it reports the count of seven new vulnerabilities and the validation setup, but does not enumerate the individual findings or the two attack chains. For those, read the open-access paper and appendix linked from the USENIX page. The "arguably worsening security" phrasing is the authors' own. The released formal model is a research artifact; using it as a basis for a deployment decision would require reading the paper's assumptions. No CAN XL hardware was exercised for this page.

## Status and sources

Checked 2026-11-17. **Published** — USENIX Security 26, August 2026, open access; paper and appendix available from the conference page.

- [USENIX paper page](https://www.usenix.org/conference/usenixsecurity26/presentation/tang-zhaozhou)

## Related

- [CANflict: exploiting peripheral conflicts for data-link layer attacks on automotive networks](canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks.md)
- [Error handling of in-vehicle networks makes them vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md)
- [On the real-world applicability of automotive CAN intrusion detection systems](on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems.md)
- [CAN message authentication: the retrofit design space](concepts/can-message-authentication.md)
