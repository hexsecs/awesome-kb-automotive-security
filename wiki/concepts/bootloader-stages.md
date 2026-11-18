---
uid: 01a19d3c-af59-7cfe-80f9-3e41adbc3bc1
title: "Bootloader stages and bootstrap entry"
summary: "ECUs boot through layers owned by different parties; the corpus's breaks concentrate at the stage transitions and the weakest stage, not the application."
type: concept
cluster: access
created: 2026-11-01
updated: 2026-11-17
depth: deep
related:
  - simos18-sboot
  - tc1791-can-bsl
  - secoc-key-extractor
  - vw-flash
  - diagnostic-service-abuse
  - secure-firmware-updates
  - firmware-acquisition
  - uds-seed-key
  - shared-and-default-secrets
  - owasp-automotive-emb-60
  - ghidra-tc1797
  - medc17-checksum-tool
  - automotive-flash-bootloaders-exposing-automotive-ecu-updates
sources:
  - url: "https://github.com/0xD006/TC1791_CAN_BSL"
    retrieved: 2026-11-01
  - url: "https://github.com/bri3d/VW_Flash"
    retrieved: 2026-11-01
  - url: "https://raw.githubusercontent.com/bri3d/Simos18_SBOOT/master/README.md"
    retrieved: 2026-11-17
  - url: "https://icanhack.nl/blog/secoc-key-extraction/"
    retrieved: 2026-11-17
  - url: "https://csrc.nist.gov/pubs/sp/800/193/final"
    retrieved: 2026-11-17
facets: [firmware, attack]
---

An ECU's boot path is an authority chain, not merely a list of binaries. Each transition decides which code may execute, which memory protections remain active, and whether earlier validation is still trustworthy. Manufacturing and recovery paths form branches around the normal startup sequence. A signature check in one branch does not secure another branch that can rewrite the checked bytes or the record of their validity.

The concrete anchor is Continental Simos18 on Infineon TriCore, documented by [Simos18 SBOOT](../simos18-sboot.md), [TC1791 CAN BSL](../tc1791-can-bsl.md), and [VW_Flash](../vw-flash.md). The Toyota EPS [SecOC key extractor](../secoc-key-extractor.md) supplies a separate RAM-loader case. These are specific implementations, not evidence that every ECU has the same stages or weaknesses.

## Stage chain and ownership

The [VW_Flash architecture document](https://github.com/bri3d/VW_Flash/blob/master/docs/docs.md) names the normal Simos18 path **mask ROM → SBOOT → CBOOT → ASW/CAL**:

| Stage | Owner or provisioning role | Security-relevant responsibility |
| --- | --- | --- |
| Mask ROM and native bootstrap | Infineon silicon | Select direct flash execution or a UART/CAN bootstrap from hardware configuration; establish flash-protection state. |
| SBOOT, supplier bootloader | Continental/Siemens | Initialise hardware, select recovery, inspect customer-loader validity, and promote a staged CBOOT update. |
| OTP protection area | End-of-line provisioning, with customer-supplied cryptographic material | Hold verification keys, flash passwords, device binding, and callable crypto routines. This is supporting data/code, not simply another sequential loader. |
| CBOOT, customer bootloader | VW customer specification/software | Run diagnostic programming, write and verify software blocks, and manage validity flags. |
| ASW and calibration | Application and vehicle integration | Run engine-control logic using the selected calibration; transfer into programming when servicing conditions are met. |

Names alone can mislead. ASW is application software, not the name of a universal "application-stage bootloader." CBOOT is the customer loader in this source. Supplier/customer ownership is a responsibility boundary, not proof of isolation: routines in the OTP area are shared dependencies, and application code can enter a RAM-resident copy of CBOOT for flashing.

SBOOT is flash-resident but described as never remotely updated in service; CBOOT is field-updated. Mask ROM is immutable, while flash protection depends on configured passwords and mode. Consequently, "ROM cannot be patched" does not imply that every access policy on every part is permanently identical. The source does not establish a general silicon-wide lifetime vulnerability.

## Bootstrap entry is not automatically flash access

The [TC1791 loader README](https://github.com/bri3d/TC1791_CAN_BSL) distinguishes two events often collapsed into "boot access." Hardware configuration selects the native serial/CAN bootstrap. It copies incoming code into scratchpad RAM and executes it without an application signature check. **Flash remains locked by the TriCore user passwords in that mode.** The researcher can run a RAM stub without yet being able to read protected firmware.

Thus the unprotected bootstrap upload is a genuine execution entry, but not a demonstrated universal bypass of all storage protection. In the documented Simos18 bench workflow, opening the ECU and accessing configuration/reset points enables the mode switch; password recovery is a separate prerequisite for the protected flash read. The current README's example explicitly distinguishes eight-byte read passwords from eight-byte write passwords. The previous description of one "32-bit boot password" did not represent that evidence.

The security question is which resources the unsigned bootstrap can touch. Accessible RAM may contain data left by an earlier stage, even while flash remains locked. Reset-domain behaviour and memory lifetime are therefore part of the boundary. Merely observing that the CPU boots a tester-supplied stub does not establish persistent modification, vehicle cloning, or access to every protected peripheral.

## Supplier recovery: a designed backdoor plus a software flaw

The [SBOOT writeup](https://github.com/bri3d/Simos18_SBOOT) calls its supplier recovery command processor a manufacturing/repair backdoor. On Simos18, timed signals on two harness pins and follow-on CAN messages select it; invalid CBOOT can also lead to recovery. The documented sequence is not evidence of an unauthenticated, remotely callable UDS RoutineControl that alone escapes the application into SBOOT. Reusing familiar diagnostic CAN identifiers does not make the custom ISO-TP command protocol standard UDS.

Recovery still has gates. Its challenge-response encrypts PRNG output using an RSA public key and expects the decrypted bytes back. The flaw is predictable generation: Mersenne Twister is seeded from a system timer with only 31 variable bits, and repeatable timing narrows the candidate range. Reproducing candidate plaintexts and comparing their encryption defeats this authentication without recovering the RSA private key. [UDS seed/key](uds-seed-key.md) provides the broader challenge-response context, but this supplier protocol should retain its own identity.

After that gate, uploaded code is still subject to RSA signature verification. The author's account explicitly says that direct unsigned-code execution through that signed-loader mechanism was not obtained. Instead, CRC validation happens first and trusts inadequately bounded address ranges. A crafted range makes the checker process protected flash; a controlled reset into native BSL exposes intermediate CRC state in RAM. Repeated observations allow password bytes to be inferred by CRC back-calculation.

This is a composed read-side attack: **recovery entry → predictable challenge response → out-of-range CRC → reset/RAM observation → password recovery → protected flash access**. CRC did not serve as the password comparison, and the signature algorithm was not cryptanalysed. The distinction explains both the successful extraction and the surviving control.

## Checksum-only integrity and cached trust

A CRC detects accidental corruption; an attacker able to alter data can generally recompute its CRC. It does not establish origin. But it would also be wrong to label all Simos18 firmware acceptance checksum-only: CBOOT checks both CRC and RSA signatures when validating downloaded blocks.

The [VW_Flash boot/trust-chain account](https://github.com/bri3d/VW_Flash/blob/master/docs/docs.md) identifies the subtler break. Boot decisions rely on persistent "OK" flags representing past successful checks. Its CBOOT state-machine flaw permits an erase operation on one block followed by writes to another, already-valid block. The second block's old validity record survives while its contents change, subject to the physical write/ECC constraints described by the author.

That is a failure to bind **the checked object, the write transaction, and the validity record**. RSA remains intact, but its successful result is reused for different bytes. The repository separately documents an ASW pivot into a modified RAM CBOOT and promotion of a replacement CBOOT, enabling persistent trust-chain bypass on supported Simos18 variants. That port-flashing chain is distinct from SBOOT password recovery; combining their end states into one universal exploit would obscure their different prerequisites.

## RAM servicing loaders and key extraction

The [Toyota EPS writeup](https://icanhack.nl/blog/secoc-key-extraction/) describes a stand-alone update bootloader on the 2021 RAV4 Prime. It accepts RAM-resident flash routines, then calls them during erase/program operations. Such a design is not intrinsically insecure: flash algorithms often need to execute outside the memory being rewritten. The relevant question is who may supply the executable routine.

Here the payload requires CRC, AES-based CMAC, encryption, and SecurityAccess. The researchers first extracted firmware using voltage fault injection, then recovered the symmetric secrets needed to construct accepted payloads. Their payload reads SecOC keys from memory and transmits them over CAN. This is **not** an unchecked arbitrary upload; it is authentication defeated after the authenticating secret became available.

The link to [shared and default secrets](shared-and-default-secrets.md) is about authority, not an established fleet-wide SecOC key. A shared verification public key does not let its holder sign code; extracted symmetric authentication material does. The source does not establish that one vehicle's recovered SecOC key authenticates on every Toyota. Its newer Corolla Cross discussion distinguishes regained code execution from HSM-protected keys that could not simply be dumped from RAM.

## Extraction, rollback, and what a secure chain requires

[Firmware acquisition](firmware-acquisition.md) covers the output side: a boot-mode dump can expose loader code and device-specific material absent from update packages. Extraction is not equivalent to transplantation. The SBOOT writeup explicitly warns that its Simos18 dumps cannot simply clone another ECU because OTP/device binding and encrypted data flash depend on the particular processor.

Rollback is a separate test. An old, correctly signed vulnerable loader can reopen a repaired path if version policy permits reinstalling it. Signature validity alone cannot distinguish acceptable recovery from a forbidden downgrade. Neither the checked TC1791 README nor the SBOOT account establishes a systematic firmware anti-rollback evaluation across this platform. Toyota's reported freshness-counter concern is not evidence of firmware-version rollback. No demonstrated rollback exploit is inferred here.

The design deductions are correspondingly specific:

- Anchor verification and policy in protected code/data; authenticate every executable handoff, including downloaded RAM helpers and recovery branches.
- Bind verification to exact bytes, target addresses, device compatibility, and transaction state. Invalidate cached approval whenever its object changes.
- Restrict bootstrap/debug capabilities by lifecycle state; contain RAM remnants and reset transitions as well as flash access.
- Separate device secrets from executable firmware and constrain authorised use, not only export. HSM storage alone does not prevent compromised software requesting signatures or MACs.
- Enforce protected version policy across application, loaders, and recovery; design interruption-safe recovery that does not silently waive authenticity.

[NIST SP 800-193](https://csrc.nist.gov/pubs/sp/800/193/final) supplies the broader **protect, detect, recover** framing for platform firmware resiliency. It is general guidance, not an automotive certification or evidence of these ECUs' compliance. [Secure firmware updates](secure-firmware-updates.md) addresses authenticated delivery and rollback policy upstream; boot enforcement must preserve those decisions locally. [Diagnostic-service abuse](diagnostic-service-abuse.md) covers who can invoke the servicing transitions. None substitutes for the others.

## Verification and limits

Checked 2026-11-17: the original `0xD006/TC1791_CAN_BSL` citation returned HTTP 404 and is retained as historical provenance. The bri3d TC1791 README, VW_Flash repository and detailed architecture document, SBOOT README, Toyota author writeup, and NIST publication page were reachable. These are documentary findings, not reproduced hardware experiments. Their scope is the named chips, ECU variants, and source-described workflows; they do not establish current fleet prevalence, universal remote reachability, an HSM-backed Simos18 architecture, or a general break of RSA.
