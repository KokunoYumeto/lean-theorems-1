# Source-linked mathematics in Lean — collaboration pilot

This proposed collection connects the host's classical-theorem suites with the source-linked [Lean of the Mathematical Commons](https://github.com/KokunoYumeto/lean-mathematical-commons) and a separate, explicitly research-originated SplitZero component. It does not presume agreement to merge repositories or maintainership, and does not call original research a classical theorem.

## Working components and fresh evidence

The opt-in [Noether workspace](noether/README.md) imports three existing source-linked modules. [Run 34657761864](https://github.com/KokunoYumeto/lean-theorems-1/actions/runs/34657761864/job/103453744068) passed at `526f777c95ce56fc7093e333c85f58d7054efcd0`: dependency pins, all three source blobs, compilation, and ten selected transitive axiom reports. The generic-zero dependency emitted an existing style advisory, so this is not a blanket zero-warning claim.

The opt-in [SplitZero component](splitzero/README.md) materializes the verified package from [Zeta PR #4](https://github.com/KokunoYumeto/zeta-function-research-reader/pull/4) without copying it into the host namespace or relicensing it. Its four extension modules and unchanged core passed [run 34660929635](https://github.com/KokunoYumeto/zeta-function-research-reader/actions/runs/34660929635/job/103463090151), including separate `--trust=0` checks and 28 selected axiom reports. The dedicated host-side workflow independently reproduces the checks. The latest exact run is required before claiming validation of a changed integration revision.

These are bounded, executable components, not certification of the entirety of either repository.

## Recovered inventory and audit boundaries

[inventory.json](inventory.json) preserves the original inventory snapshot. Its historical SplitZero status is superseded by `splitzero/source.json` and the verified source package; it is retained as history, not as the current validation status.

| Collection | Recovered scope | Treatment |
| --- | --- | --- |
| Noether library | 55 direct imports, historical 57-target graph; 43 works with 21 partial audits and no complete paper audit. | Three source-read modules imported separately; not a new full-graph certification. |
| Noether claim ledger | 343 claim rows: 154 available/completed, including 95 Mathlib exact/modern and 59 locally completed-content rows; 189 open. | Historical classifications, not counts of new mathematical discoveries. |
| Hentzelt–Noether | Substantial coordinate, regular-division, localization, saturation, Smith and annihilator/product code; reported 576 declarations in base plus 38 supports. | Inventory only. Historical norm/resultant and canonicity gaps remain explicit. |
| Older classical candidates | AffineGroup, JordanPrimitiveRoots, Steinitz and Weber; three duplicate blobs elsewhere. | No duplicate counting; recheck before importing. |
| SplitZero | Original core plus four freshly verified structural extension modules. | Opt-in research component: exact maps, support fibres, ideals and corrected presentation. Not a full scheme/analytic development. |
| ClassicalBatch2 | Recorded failed build, stale API and `sorryAx`. | Excluded from promotion. |
| SGA and adjacent editions | Extensive reader/TeX sources, including SGA 4½. | Sources for later exact statement mapping, not an existing SGA Lean library. |
| Host and suites II/III | Classical suites with differing scaffold status; upstream PR #5 already accepted. | No blanket recertification or duplicate credit. |

The Noether [coverage snapshot](https://github.com/KokunoYumeto/lean-mathematical-commons/blob/8cdaca4421fd1fb3864b0d7b4ae6662065eeb194/artifacts/coordination/noether-coverage-snapshot-20260829.json) counts claim packages, not necessarily single declarations. Whole-corpus percentages are planning estimates. The search for scattered files was bounded and does not rule out unuploaded code, unindexed branches or archived snippets.

## Mathematical connection

Noether's `ModularInvariants1926` proves characteristic-free finite generation of fixed algebras, and of intermediate subalgebras containing the fixed algebra, by integrality followed by Artin–Tate. `Idealtheorie1921` packages primary ideals, associated primes and positive-power statements, partly using existing Mathlib. `EliminationIdealTheorySurvey1924` constructs generic zeros in fraction fields of prime coordinate rings, proves the exact evaluation kernel and field-generation statements, and correctly qualifies the strict transcendence-degree bound by nonzero primality.

SplitZero is the owner's research construction. Its ring reflection necessarily erases the distinction between supported and absent zero, whereas amplitude and Boolean support jointly retain it. Its semimodules carry support fibres that are genuine modules over the original ring, with coherent linear transports. The new package proves these structures rather than assuming them, and corrects the missing `[tau]=0` relation and ambient empty-join qualification. Classical analogues and any potential novelty require a separate priority comparison.

## Integration boundary

The host remains Lean 4.34.0-rc1. Both optional components use independent Lean 4.31.0 workspaces and exact Mathlib/source pins. They are not a monolithic common-version library. The existing host Lake configuration, root imports, CI workflow, and theorem declarations are untouched. Noether retains Apache-2.0; SplitZero retains its source rights and attribution. This proposal does not relicense external sources under the host's license.

A shared programme should distinguish existing Mathlib coverage, new packaging, completed formalization, conditional support and open targets. Each promotion needs a source locator, exact statement and hypotheses, successful build, and transitive axiom evidence. Complete bounded work should be integrated without treating the unfinished remainder as either a certificate or a reason to discard it.
