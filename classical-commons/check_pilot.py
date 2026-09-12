#!/usr/bin/env python3
"""Fail-closed structural, resolved-source, and selected-axiom checks.

Preflight/self-tests are NOT Lean verification. Resolved-source checks need
Lake's fetched dependencies; the axiom check needs output from a successful
`lake env lean --trust=0 -DwarningAsError=true Audit.lean` command.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib

HERE = Path(__file__).resolve().parent
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def preflight(base: Path = HERE) -> dict:
    data = json.loads((base / "inventory.json").read_text(encoding="utf-8"))
    spec = data["noether"]
    pilot = base / "noether"
    require((pilot / "lean-toolchain").read_text().strip() == spec["lean_toolchain"],
            "Pilot toolchain does not match inventory")
    config = tomllib.loads((pilot / "lakefile.toml").read_text(encoding="utf-8"))
    dependencies = {entry["name"]: entry for entry in config["require"]}
    require(set(dependencies) == {"mathlib", spec["package"]}, "Unexpected dependencies")
    require(dependencies["mathlib"]["rev"] == spec["mathlib_commit"], "Mathlib pin mismatch")
    require(dependencies[spec["package"]]["rev"] == spec["commit"], "Noether pin mismatch")
    require(dependencies["mathlib"]["git"] == "https://github.com/leanprover-community/mathlib4.git",
            "Unexpected Mathlib origin")
    require(dependencies[spec["package"]]["git"] == f'https://github.com/{spec["repository"]}.git',
            "Unexpected Noether origin")
    for revision in (spec["commit"], spec["mathlib_commit"]):
        require(re.fullmatch(r"[0-9a-f]{40}", revision) is not None, "Non-immutable dependency ref")
    source = (pilot / "ClassicalCommonsNoether.lean").read_text(encoding="utf-8")
    imports = re.findall(r"^import\s+(\S+)\s*$", source, flags=re.MULTILINE)
    require(imports == [m["module"] for m in spec["selected_modules"]], "Import inventory mismatch")
    audit_source = (pilot / "Audit.lean").read_text(encoding="utf-8")
    targets = re.findall(r"^#print axioms\s+(\S+)\s*$", audit_source, flags=re.MULTILINE)
    require(targets == spec["axiom_audit_targets"], "Axiom target inventory mismatch")
    require(len(targets) == len(set(targets)) and len(targets) > 0, "Empty or duplicate audit targets")
    require(set(spec["allowed_axioms"]) == STANDARD_AXIOMS, "Nonstandard axiom allowlist")
    for path in (pilot / "ClassicalCommonsNoether.lean", pilot / "Audit.lean"):
        text = path.read_text(encoding="utf-8")
        require(re.search(r"\b(sorry|admit|sorryAx|native_decide|axiom)\b", text) is None,
                f"Unexpected proof escape in {path.name}")
    return data


def git_head(directory: Path) -> str:
    require((directory / ".git").exists(), f"Missing fetched Git package: {directory}")
    return subprocess.check_output(
        ["git", "-C", str(directory), "rev-parse", "HEAD"], text=True
    ).strip()


def resolved_sources(data: dict, base: Path = HERE) -> None:
    spec = data["noether"]
    packages = base / "noether" / ".lake" / "packages"
    noether = packages / spec["package"]
    require(git_head(noether) == spec["commit"], "Resolved Noether commit mismatch")
    require(git_head(packages / "mathlib") == spec["mathlib_commit"], "Resolved Mathlib commit mismatch")
    for module in spec["selected_modules"]:
        raw = (noether / module["path"]).read_bytes()
        blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        require(blob == module["git_blob_sha"], f'Source blob mismatch: {module["path"]}')


def audit_axiom_log(text: str, targets: list[str]) -> dict[str, list[str]]:
    require(re.search(r"\b(sorryAx|Lean\.ofReduceBool|Lean\.ofReduceNat)\b", text) is None,
            "Unapproved proof escape in Lean output")
    reports: dict[str, list[list[str]]] = {}
    pattern = r"'([^']+)'\s+depends on axioms:\s*\[([^\]]*)\]"
    for match in re.finditer(pattern, text, flags=re.MULTILINE):
        name, body = match.groups()
        axioms = [a.strip() for a in body.split(",") if a.strip()]
        reports.setdefault(name, []).append(axioms)
    for match in re.finditer(r"'([^']+)'\s+does not depend on any axioms", text):
        reports.setdefault(match.group(1), []).append([])
    result: dict[str, list[str]] = {}
    for target in targets:
        require(target in reports, f"Missing axiom report: {target}")
        require(len(reports[target]) == 1, f"Duplicate axiom report: {target}")
        axioms = reports[target][0]
        require(set(axioms) <= STANDARD_AXIOMS, f"Nonstandard axiom for {target}: {axioms}")
        result[target] = axioms
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resolved", action="store_true", help="Check fetched commits and source blobs")
    parser.add_argument("--axiom-log", type=Path, help="Check successful Lean Audit.lean output")
    args = parser.parse_args()
    try:
        data = preflight()
        report = {"preflight": "pass", "fresh_lean_build": "not_asserted_by_this_script"}
        if args.resolved:
            resolved_sources(data)
            report["resolved_source_pins"] = "pass"
        if args.axiom_log:
            results = audit_axiom_log(args.axiom_log.read_text(encoding="utf-8"),
                                      data["noether"]["axiom_audit_targets"])
            report["selected_axiom_reports"] = results
        print(json.dumps(report, indent=2))
        return 0
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError, tomllib.TOMLDecodeError) as exc:
        print(f"PILOT CHECK FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
