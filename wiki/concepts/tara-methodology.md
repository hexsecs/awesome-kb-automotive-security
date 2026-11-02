---
title: "TARA methodology: the ISO/SAE 21434 artefact chain"
summary: "How an automotive TARA is actually assembled: the ISO/SAE 21434 artefact chain, the layers the KB's tools occupy, and where automation helps and lies."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [automotive-threat-matrix, automotive-threat-modeling-template, autotara, security-autodesigner, automating-function-level-tara-for-automotive-full-lifecycle-security, avcdl, secure-firmware-updates]
sources:
  - url: "https://github.com/nccgroup/autotara"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.14722/ndss.2026.231408"
    retrieved: 2026-11-01
---

Every other concept in this KB is a mechanism. This one is a *method*: the Threat Analysis and Risk Assessment (TARA) that ISO/SAE 21434 requires and UN R155 audits — the process by which an organisation decides, on paper and in advance, which of the mechanisms in this KB matter for a given vehicle system. The KB's Security Analysis pages each occupy one layer of that process without stating the whole; this page assembles the whole, because the joins between layers are where the method's real behaviour lives. The filing evaluation flagged the risk plainly — a methodology page earns its place only as falsifiable synthesis, not a section tour — so each layer below carries the claim the corpus actually supports about it.

## The artefact chain

A 21434 TARA is a chain of artefacts, each derived from the last:

**Item definition → assets → threat scenarios → attack paths → feasibility → risk → treatment.**

The item (a system, bounded) yields assets (things with cybersecurity properties worth protecting); each asset's damage scenarios yield threat scenarios; threat scenarios decompose into attack paths — ordered steps an attacker must complete; each step carries a **feasibility** rating, and path feasibility composes from its steps (the chain's central mechanic: a path is only as feasible as its hardest step, under the standard's composition rules); feasibility × impact gives risk; risk drives treatment (avoid, reduce, share, retain) and the cybersecurity goals that downstream engineering must satisfy. UN R155's Annex 5 supplies the shared vocabulary — its threat catalogue is the key every layer below maps back to, which is what makes two organisations' TARAs comparable at audit.

## The layers, as the corpus stocks them

- **Adversary and threat taxonomy.** The [Automotive Threat Matrix](../automotive-threat-matrix.md) organises attacker technique for the domain — the enumeration a threat-scenario author draws from. Its function in the chain is coverage discipline: scenarios not in the taxonomy's span are the ones audits miss.
- **System modelling.** The NCC [threat modeling template](../automotive-threat-modeling-template.md) generates the item's data-flow diagram and derives STRIDE-class threats from it — the asset/scenario derivation made semi-mechanical. The model's fidelity bounds everything downstream: an asset absent from the DFD has no scenario, no path, no risk line.
- **Automation, research pole.** [AutoTARA](../autotara.md) builds attack graphs over a Meta Attack Language model of the system and *simulates* them, prioritising by its CTSA/CRRA ratings — feasibility computed from the graph rather than asserted per step. The NDSS 2026 [DefenseWeaver](../automating-function-level-tara-for-automotive-full-lifecycle-security.md) work pushes granularity down: **function-level** TARA instead of vehicle-level, with an LLM split (LoRA-tuned generation, RAG scoring) and pen-test-confirmed paths as its validation claim — and a stated failure case (QNX nodes) where its model of the target ran out.
- **Automation, commercial pole.** [Security AutoDesigner](../security-autodesigner.md) productises the artefact chain for compliance workflows. The spectrum matters more than either pole: manual expert TARA, graph-simulated TARA, and generated TARA disagree about where judgement lives — in the analyst's step ratings, in the model's fidelity, or in the generator's training. The artefact chain is identical; the epistemics are not.
- **Lifecycle embedding.** [AVCDL](../avcdl.md) places the TARA where 21434 actually puts it: one gated work product inside a full development lifecycle, versioned with the item, revisited at change. A TARA that is a document written once for an audit is the degenerate case the lifecycle exists to prevent.

## Where the chain ends, and what it cannot do

A TARA *selects* treatments; it does not contain them. The update-path goal a TARA emits is discharged by something like [Uptane](secure-firmware-updates.md); the chain's authority stops at the requirement. Two failure modes the corpus supports concretely: **granularity mismatch** — vehicle-level TARA rates a path infeasible whose steps, at function level, are each routine (DefenseWeaver's premise); and **model-reality gaps** — every automation pole inherits its system model's omissions, and a generated path set is complete only relative to a model an attacker is not obliged to respect. The method's output is a *prioritised argument*, auditable and revisable — treating it as a proof is the category error its own standard's lifecycle clauses are written against.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source.

## Related

- [Automotive Threat Matrix](../automotive-threat-matrix.md) — the taxonomy layer
- [Automotive threat modeling template](../automotive-threat-modeling-template.md) — the modelling layer
- [AutoTARA](../autotara.md) and [Security AutoDesigner](../security-autodesigner.md) — the automation spectrum's poles
- [Automating Function-Level TARA (DefenseWeaver)](../automating-function-level-tara-for-automotive-full-lifecycle-security.md) — the granularity argument, with pen-test validation
- [AVCDL](../avcdl.md) — the lifecycle the TARA lives inside
