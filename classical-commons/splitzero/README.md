# SplitZero — opt-in verified research component

This component connects the owner's SplitZero research construction to the source-linked formalization collection. It is **not** presented as a classical theorem, a claim of globally new mathematics, or a completed Zeta programme. Source construction and manuscript results retain their existing attribution and rights.

The mathematical implementation lives in [Zeta PR #4](https://github.com/KokunoYumeto/zeta-function-research-reader/pull/4), pinned here to `9c47f76b4e3336ee065b691344271b2d150d75ff`. Its proof code is byte-identical to successful [run 34660929635](https://github.com/KokunoYumeto/zeta-function-research-reader/actions/runs/34660929635/job/103463090151) at `8196e4f4d4f09a8cfc8a4e8ce8683ded359adbf6`.

## The completed unit

Four modules establish universal ring reflection, unique Boolean support, faithful amplitude/support coordinates, the exact correspondence between split-to-split semiring maps and ring maps, intrinsic support fibres with actual module structures, coherent linear transports, fibre-map naturality, reconstruction of addition, and complete ideal classification. The presentation module supplies a Boolean countermodel and the corrected generator-level semiring-lift property.

The source's ordinary monoid-semiring presentation needs `[tau]=0`; its printed relations alone permit every generator to evaluate to one in the Boolean semiring. The ideal-order isomorphism targets non-bottom ideals, so the ambient empty join is not preserved. Both qualifications have complete proofs in the source package.

The original 7,366-byte SplitZero core is unchanged and has freshly rebuilt. The four extension files passed separate `--trust=0 -DwarningAsError=true` checks. All 28 selected transitive axiom reports use only standard axioms. This does not certify the abstract reverse diagram construction, a fully bundled categorical equivalence, the free congruence quotient, or the later analytic/Rees programme.

## Reproduce independently of the host build

```sh
python3 classical-commons/splitzero/materialize.py
cd classical-commons/splitzero/.workspace
lake update
lake exe cache get
lake -KmaxJobs=1 build
lake env lean --trust=0 SplitZero.lean
for f in SplitZeroExtension.lean SplitZeroFibres.lean SplitZeroPresentation.lean SplitZeroMaps.lean; do
  lake env lean --trust=0 -DwarningAsError=true "$f"
done
lake env lean --trust=0 -DwarningAsError=true Audit.lean > Audit.log
python3 check_axioms.py Audit.log
python3 test_axioms.py -v
```

Python 3.11+ and elan are required. The dedicated workflow executes these checks. `source.json` pins the source commit and verifies the successful proof/configuration hashes. The materializer refuses conflicting local files. Source is retrieved without changing its licensing, namespaces or contents.

The host remains Lean 4.34.0-rc1. This workspace remains Lean 4.31.0 with Mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`. This is a federated integration with independent builds, **not** a claim that both projects are already ported to one Lean version. No host theorem, root import, Lake configuration, existing CI workflow, or source edition is modified.
