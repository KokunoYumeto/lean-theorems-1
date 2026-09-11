# Classical Mathematics in Lean — collaboration pilot

This is a proposed connection between the classical-theorem suites in this
repository and the source-linked [Lean of the Mathematical Commons](https://github.com/KokunoYumeto/lean-mathematical-commons).
It contributes a public inventory and an opt-in Noether workspace, not a
wholesale repository merger, a new governance arrangement, or a claim that
all listed mathematics is formalized. The maintainers can adopt the small
pilot independently of the broader proposal.

**Status:** the three selected source files were read and the Python preflight
and ten synthetic checker tests passed during preparation. The authoring
environment did not have Lean. The dedicated Noether workflow must provide
fresh compilation and selected-declaration axiom evidence before this pilot
is represented as build-verified. Historical receipts are not a substitute.

## Recovered inventory and audit boundaries

The machine-readable inventory is [inventory.json](inventory.json). Its
Noether source is pinned to commit
`8cdaca4421fd1fb3864b0d7b4ae6662065eeb194`.

| Collection | Evidence recovered | Treatment in this pilot |
| --- | --- | --- |
| Noether library | A 55-import umbrella and a historical 57-target graph receipt, on Lean 4.31.0. The coverage snapshot inventories 43 works, with 21 partial audits and no complete paper audit. | Import three source-read modules in an isolated workspace. |
| Noether claim ledger | 343 inventoried claim rows: 154 available/completed, including 95 Mathlib exact/modern rows and 59 newly completed local-content rows; 189 remain open. | Historical classifications, not freshly recomputed theorem counts or whole-corpus coverage. |
| Hentzelt–Noether polynomial ideals/resultants | Substantial coordinate, regular-division, localization, saturation, Smith-module and annihilator/product developments. The README reports 576 declarations across its base and 38 support modules. | Inventory only. Helpers and conditional constructions do not establish the missing historical resultant/norm identifications or the complete paper. |
| Older classical candidates | AffineGroup, JordanPrimitiveRoots, Steinitz and Weber have recorded successful historical checks. Three also occur as identical blobs in the older sidecar directory. | Do not count duplicates twice. Recheck statements, dependency axioms and reuse terms before importing. |
| SplitZero | Concrete split-zero semiring, ring-reflection and fixed-locus source. Its historical manifest records a successful recheck but no printed-axiom audit. | Not imported; pending fresh compilation, axiom audit and reuse review. Not a completed scheme-theoretic development. |
| ClassicalBatch2 | The historical manifest explicitly records a failed build, stale API and `sorryAx`. | Excluded, not promoted because it is preserved in the archive. |
| SGA and adjacent editions | Reader/TeX source assets, including SGA 4½, are indexed publicly. | Source collection for future statement-level work, not an existing SGA Lean formalization. No source scans or translations are copied here. |
| This repository and suites II/III | Existing classical suites and differing levels of scaffold completion. The earlier contribution in PR #5 is already merged here. | No recertification or duplicate credit. No bulk imports from the other suites. |

The [coverage snapshot](https://github.com/KokunoYumeto/lean-mathematical-commons/blob/8cdaca4421fd1fb3864b0d7b4ae6662065eeb194/artifacts/coordination/noether-coverage-snapshot-20260829.json)
counts claim packages, not necessarily individual Lean declarations. Its
whole-corpus percentages are planning estimates; they are not a measured
percentage of Noether's mathematics proved. The repository's
[latest historical graph receipt](https://github.com/KokunoYumeto/lean-mathematical-commons/blob/8cdaca4421fd1fb3864b0d7b4ae6662065eeb194/artifacts/build/module-graph-checkpoint-20260829T2327308948138-d815b8e6.json)
reports 57 targets. Earlier README checkpoint headings should not override
that more specific receipt.

The older-file classifications come from the
[classical-candidate manifest](https://github.com/KokunoYumeto/modern-latex-manuscripts/blob/f7ff59b176c7dc3941babd4cb9272dffc653070d/formalization/lean/classical_candidates_20260626/FORMALIZATION_MANIFEST.json).
SGA assets are indexed in the
[publication manifest](https://github.com/KokunoYumeto/modern-latex-manuscripts/blob/f7ff59b176c7dc3941babd4cb9272dffc653070d/sources/sga/SGA2_CURRENT_PUBLICATION.json).
The search was bounded: it does not establish the absence of code in every
branch, archive, or unuploaded working session.

## Why these three modules

`ModularInvariants1926` proves finite generation of fixed subalgebras for
finite group actions on finite-type commutative algebras over Noetherian
bases, without a characteristic-zero hypothesis. More generally, every
intermediate subalgebra containing the fixed subalgebra is finite type. This
is a substantive integrality-to-Artin–Tate combination, not merely the
statement that invariants are integral. It is a natural algebraic connection
to finite-group invariant theory, but does not construct a particular
icosahedral action, explicit generators, a Molien series, or a spectral law.

`Idealtheorie1921` combines primary-ideal, associated-prime and positive-power
statements. Some results are source-shaped wrappers around Mathlib; their
historical correspondence is useful, but should not be presented as newly
proved mathematics or a wholly new formalization of primary decomposition.

`EliminationIdealTheorySurvey1924` constructs the generic point in the
fraction field of a prime coordinate ring: evaluation has precisely the
specified prime kernel, and the coordinate images generate the field. It
proves transcendence degree at most the number of variables; the strict
inequality explicitly requires a nonzero prime ideal. This is reusable
algebraic-geometry groundwork, not the formalization of SGA.

## Integration without a forced version migration

The host remains on Lean `4.34.0-rc1`. The separate
[Noether workspace](noether/README.md) uses Lean `4.31.0`, exact Mathlib commit
`fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, and the immutable Noether commit
above. There are no changes to the host Lake configuration, root imports,
existing CI, or theorem declarations. Noether remains a fetched dependency;
its Apache-2.0 license and attribution remain in its own repository.

The new workflow checks resolved Git commits and the selected source blobs,
builds the three imports, and checks the transitive axiom reports of ten
explicitly named declarations. Only `propext`, `Classical.choice` and
`Quot.sound` are accepted. Missing reports fail. The ten Python tests exercise
this checker; they do not compile Lean or prove the mathematics. Nor does
checking these ten declarations certify every declaration in either library.

## Suggested shared program

A useful common project would keep one source-to-statement inventory while
retaining independent, pinned builds until compatibility is demonstrated.
Each addition should carry the original source locator, exact Lean statement,
hypotheses, attribution, dependency pin, successful build, transitive axiom
report and an honest category: existing Mathlib, new packaging, completed
formalization, conditional support, or open target.

After the pilot is checked, small ports of invariant-theory and
coordinate-ring results would be more reviewable than copying the full
Noether development. The next P22 work is the missing mathematical
identification/invariance layer, not relabeling existing determinant helpers
as a resultant. SGA can supply precisely selected targets only after checking
its source statements and present Mathlib coverage. Combining libraries
should preserve those boundaries rather than turn translations or
scaffolds into completion claims.
