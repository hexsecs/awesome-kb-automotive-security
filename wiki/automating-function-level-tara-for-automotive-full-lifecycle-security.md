---
title: "Automating Function-Level TARA for Automotive Full-Lifecycle Security"
summary: "Yang et al., NDSS 2026. DefenseWeaver, a multi-agent LLM system that automates function-level ISO/SAE 21434 threat analysis and risk assessment, reported as…"
type: entity
category: "Research Papers"
url: "https://www.ndss-symposium.org/ndss-paper/automating-function-level-tara-for-automotive-full-lifecycle-security/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Yang et al., NDSS 2026. DefenseWeaver, a multi-agent LLM system that automates function-level ISO/SAE 21434 threat analysis and risk assessment, reported as deployed in four automotive projects."
sources:
  - url: "https://www.ndss-symposium.org/ndss-paper/automating-function-level-tara-for-automotive-full-lifecycle-security/"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.14722/ndss.2026.231408"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - autotara
  - avcdl
  - security-autodesigner
  - tara-methodology
---

Yang et al., NDSS 2026. DefenseWeaver, a multi-agent LLM system that automates function-level ISO/SAE 21434 threat analysis and risk assessment, reported as deployed in four automotive projects.

## What it is

Yuqiao Yang, Yongzhao Zhang (equal contribution), Wenhao Liu, Jun Li, Pengtao Shi, DingYu Zhong, Jie Yang, Ting Chen, Sheng Cao, Yuntao Ren, Yongyue Wu, and Xiaosong Zhang — University of Electronic Science and Technology of China (UESTC) and GoGoByte Technology. *Network and Distributed System Security (NDSS) Symposium 2026*. The paper presents DefenseWeaver, which it claims as the first system to automate *function-level* TARA — threat analysis and risk assessment per component (a body control module, a cockpit domain controller, a keyless-entry system), using that component's actual hardware, software versions, channels, and interfaces — rather than vehicle-level TARA, which reasons about the whole vehicle and assumes internal elements are not directly reachable. The distinction does real work: function-level analysis sees entry points vehicle-level analysis misses (the paper's example is a JTAG port on an internal MCU), scores the same logical path (IVI → gateway → BCM) differently per OEM implementation, and can be re-run as the vehicle changes. The baseline it displaces is twofold: manual TARA (expert-driven, inconsistent, hard to keep current) and datalog-based automation in the MulVal line (including the automotive CarVal), which generates attack paths from a *static threat library* — one that cannot distinguish an old library version from a patched one and needs manual vulnerability annotation. DefenseWeaver replaces the library with LLM inference from component-specific detail. Its pipeline follows ISO/SAE 21434 as the paper lays it out: item definition and assets, threat scenarios, attack-path analysis as attack trees, feasibility rating, impact rating, risk level 1–5, and treatment — under the regulatory frame of UN R155's CSMS and vehicle-type-approval requirements.

## What it showed

The system has three technical pieces. First, a representation: configurations are written in OpenXSAM++, an extension of the ASRG's OpenXSAM format adding Software and Hardware attributes and Channel and Interface elements; all acyclic entry-point-to-endpoint paths are extracted by depth-first search and segmented into *atoms* — one node plus its channels, split per exit channel so every atom carries exactly one local attack objective. Second, a multi-agent framework over a GPT-4 base: a Sub-Tree Constructor infers each atom's attack methods by chain-of-thought (attack-surface inference, local objective, then methods — one operation per method, joined by AND/OR logic); an Attack-Tree Assembler joins sub-trees at their channel-related methods, can send incoherent sub-trees back for regeneration, and enforces user constraints (deployments may exclude, e.g., social engineering or physical destruction, which then cannot appear in trees); a Risk Assessor scores every method on ISO/SAE 21434's five feasibility dimensions (elapsed time, expertise, item knowledge, window of opportunity, equipment), composes path feasibility bottom-up (a path is as hard as its hardest step; a scenario takes its most feasible path), scores impact across safety, financial, operational, and privacy, and maps the pair to a risk level. Third, a deliberately split adaptation strategy: the Constructor is LoRA fine-tuned on expert-curated reports (116 threat scenarios, over 1,000 sub-trees, about 5,000 feasibility entries), because retrieval hurt it — RAG pulled QNX-specific nodes into a Linux analysis — while the Assessor uses RAG over scored historical cases, because scoring standards vary by company and region and must stay current. Threat scenarios themselves (objective, entry points, endpoint) are still supplied by the user; automating them via STRIDE is proposed future work, not part of the system. Validation is the paper's strongest section. Deployed in four real automotive projects (manufacturers anonymized under confidentiality agreements), DefenseWeaver's trees directed penetration testing that confirmed 11 practical attack paths, each rated risk level ≥ 3, all reported and since patched. Two BCMs under the *same* scenario (disable door control via IVI → gateway → BCM) produced different feasible paths from configuration alone: one gateway's OpenSSL 1.1.0a admitted a known buffer-overflow CVE (Medium feasibility, risk 3), the other's exposed UART and a Linux kernel CVE instead (High, risk 4) — both ending in UDS firmware reprogramming after the BCM's SecurityAccess seed-key algorithm was reverse-engineered from a JTAG firmware dump. A cockpit controller's OTA path fell to hardcoded CA certificates and private keys in the telematics box (a cloud-to-vehicle MITM) combined with update logic that proceeded even when the firmware hash check failed (Medium, Serious impact, risk 4). A UWB-hardened passive keyless entry system — secure ranging deployed specifically to stop relay attacks — fell to a combination: jamming UWB ranging while the owner was present so stale proximity data was retained, then relaying the BLE channel after the owner left (High, Serious, risk 5). Cross-domain case studies (a PX4 UAV, a ship's ECDIS) were model-only: the system reproduced the paths reported in prior literature for each and proposed one additional literature-grounded path apiece. Against seven human experts across six scenarios, in a double-blind scoring, DefenseWeaver's trees scored far higher on novelty (+105%), configuration alignment (+43.68%), and detail (+41.46%), marginally higher on logical rationality (+5.79%), and essentially tied on non-redundancy (3.67 vs 3.70), at 0.43 minutes per tree versus 36.12 — the reported 98.8% time reduction. Deployment figures are the authors': integration at UAES and Xiaomi, over 8,200 attack trees generated, some 300 million tokens in three months.

## Where it fits

The third pole of this KB's TARA automation picture, and the one that changes what the automation *knows from*. [AutoTARA](autotara.md) simulates attack graphs in the Meta Attack Language and prioritizes with MITRE CTSA/CRRA over seeded ATT&CK and UN R155 Annex 5 data — a formal model with a fixed knowledge base, open-source and self-described as a prototype. DefenseWeaver has no attack language and no fixed library: it infers methods per atom from component attributes with an LLM, and its knowledge base is a corpus of prior TARA reports split between fine-tuning and retrieval. [Security AutoDesigner](security-autodesigner.md) is the commercial pole as the KB has it — proprietary, vendor-claimed, thinly documented; DefenseWeaver is also commercially deployed, but documented to NDSS standard, with its format, agent roles, scoring composition, and LoRA-versus-RAG choices all inspectable. Against [AVCDL](avcdl.md), "lifecycle" needs care: AVCDL is a full development lifecycle inside which a TARA is one gated work product; DefenseWeaver's "full-lifecycle" claim is narrower — a function-level TARA cheap enough to re-run on every OTA update, hardware swap, or patch. It automates a step of AVCDL's lifecycle; it is not a lifecycle. Its findings land inside existing KB mechanisms: both BCM paths terminate at the UDS SecurityAccess service whose seed-key design space the KB covers, and the PKES case is a relay attack that succeeds *despite* the UWB countermeasure — by attacking the ranging process's freshness rather than the ranging measurement.

## Limits and safety notes

The automation boundary is easy to overstate, so it is stated exactly: DefenseWeaver does not generate threat scenarios, does not verify its own trees formally (the Discussion concedes attack-tree correctness formalization is an open problem; prompt-injection defences and schema checks are the implemented safeguards), and only analyses systems that discretize into its node-and-channel graph — the paper's own out-of-scope example is a quantum key distribution network. The human comparison, while double-blind, rests on seven reviewers scoring on 1–4 scales; the penetration-test confirmations are the harder evidence, and they validate the paths *surfaced in these four projects*, not a recall rate over all real paths. Deployment and token figures are operator-reported and attributed, not independently verified. The code is not fully open: proprietary licensing, a promised community version and open expert-report database, and a linked project repository whose contents were not audited for this page. The four vehicle projects are anonymized (Cars A–D) under confidentiality agreements; this page names no manufacturer, model, or supplier for them, and the worked paths are summarized without reproducing exploit steps. All 11 paths were, per the paper, responsibly disclosed and patched.

## Status and sources

Status: **published**: *Proceedings of the 2026 Network and Distributed System Security Symposium (NDSS 2026)*, San Diego, 23–27 February 2026. **DOI 10.14722/ndss.2026.231408 — verified two ways**: it is printed in the paper itself and the fetched Crossref record matches on title, venue, and year (the record carries no page range; NDSS does not paginate conventionally). The stub's summary claim — "reported as deployed in four automotive projects" — is the paper's own account and is carried here with that attribution.

## Related

- [AutoTARA](autotara.md)
- [AVCDL](avcdl.md)
- [Security AutoDesigner](security-autodesigner.md)
