# Opt-in Noether workspace

This adapter imports three existing modules from the exact Noether dependency
recorded in `../inventory.json`. It introduces no new mathematical theorem
and does not import the host's `Formalization` library across Lean versions.
Use a recent Python (3.11+) and elan/Lake to reproduce the following steps.

From the repository root:

```sh
python3 -m unittest discover -s classical-commons -p 'test_*.py' -v
python3 classical-commons/check_pilot.py
cd classical-commons/noether
lake update
lake exe cache get
cd ../..
python3 classical-commons/check_pilot.py --resolved
cd classical-commons/noether
lake -KmaxJobs=1 build ClassicalCommonsNoether
# In bash, pipefail preserves Lean's exit status when tee is used.
set -o pipefail
lake env lean --trust=0 -DwarningAsError=true Audit.lean | tee Audit.log
cd ../..
python3 classical-commons/check_pilot.py --axiom-log classical-commons/noether/Audit.log
```

The dedicated GitHub workflow runs this sequence independently of the host
build. Its checkout action, elan bootstrap source, direct dependency commits
and Lean toolchain are pinned. Dependency resolution must match the manifest's exact Git commits;
the three imported source files must also match their recorded Git blobs.

`ClassicalCommonsNoether.lean` imports invariant finite generation (1926),
ideal theory (1921), and generic zeros/transcendence degree (1924).
`Audit.lean` prints the axioms of ten existing imported declarations, not an
empty new namespace. Those reports are accepted only when every target is
present once and uses no axioms beyond `propext`, `Classical.choice` and
`Quot.sound`.

A successful preflight, mock-log test, or historical receipt is not a fresh
Lean build. The log checker alone also cannot authenticate a supplied log;
it is the workflow's preceding successful Lean command and verified input
pins that supply that context. This is a bounded selected-declaration check,
not an independent replay of the entire Noether corpus or all of Mathlib.

The first CI attempt found a setup error in this adapter: the composite Lean
action required an existing `lake-manifest.json`. The workflow now installs
the pinned toolchain explicitly and runs `lake update` before checking the
resolved commits and fetching the cache. That initial setup failure is not a
Noether proof failure, nor does this correction itself establish a successful
Lean build.
