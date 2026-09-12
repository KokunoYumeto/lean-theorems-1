# Additive update: actual synchronization from the Rees workbench

This update preserves the existing Noether and SplitZero collaboration pilot.
It extends the materialized SplitZero package by one module from the owner's
pending Rees work, section 2.1, rather than adding a parallel scalar library.

The source pin now includes `SplitZeroSynchronization.lean`, the additional
checker and its six tests, and `SYNCHRONIZATION.md` with a complete mathematical
proof. All four structural extension sources and the original core are unchanged.
The existing structural validation record remains valid for its stated scope;
it is not presented as validation of the new synchronization claims.

For every commutative ring A, the new module defines the literal mixed-double
multiplication, the element E=(1,e), and the amplitude map to A[t]/(t²+1).
It proves that multiplication by E is idempotent, preserves amplitude, and
satisfies the exact set-image equality

    r_E(p_D⁻¹(F)) = image(r_E) ∩ p_D⁻¹(F)

for every subset F of the amplitude algebra. In particular this holds at every
level of an amplitude-pullback filtration. It does not assume idempotence or
strictness, choose an amplitude section, or assert that arbitrary comparisons
are strict. The general Rees-module construction and strictness-to-zero-defect
bridge remain separate formalization tasks.

The source `236f0a8370477991e2d0cf334ad1ebfe4f3f8b17` is paired with source
workflow run `34662202595`. Host-side CI additionally rebuilds this exact
materialization and checks both the 28 selected structural reports and all
19 named synchronization declarations, including definitions and supporting
lemmas. Those counts are not counts of new discoveries. Only the three standard
axioms `propext`, `Classical.choice`, `Quot.sound` are allowed.

The declared source/configuration byte pins are checked before execution.
The old SHA-256 pins are retained for unchanged files; verified Git blob IDs
pin the new proof/checker files and changed Lake configuration. The resolved
Mathlib commit is checked independently. A changed integration head needs its
own successful host workflow result before claiming a fresh integration build.

The original research attribution and rights remain unchanged. The old source
README and `VALIDATION.json` describe the structural checkpoint; this addendum,
the source synchronization note, and the exact current workflow links supply
the incremental scope. No host root import or toolchain is changed.
