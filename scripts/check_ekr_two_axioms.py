#!/usr/bin/env python3
"""Require every named EKR extension to report only standard axioms."""
import re
import sys
from pathlib import Path
names = [
    'two_uniform_center_unique', 'two_uniform_large_intersecting_isStar',
    'uniform_star_eq_full_of_card_eq', 'erdos_ko_rado_uniqueness_two',
    'erdos_ko_rado_equality_two', 'ekr_four_point_boundary_counterexample',
]
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
text = Path(sys.argv[1]).read_text(encoding='utf-8')
reports = {}
for name, content in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", text, re.S):
    if name in reports:
        raise SystemExit('duplicate axiom report: ' + name)
    reports[name] = {x.strip() for x in content.split(',') if x.strip()}
for name in re.findall(r"'([^']+)' does not depend on any axioms", text):
    if name in reports:
        raise SystemExit('duplicate axiom report: ' + name)
    reports[name] = set()
for name in names:
    if name not in reports:
        raise SystemExit('missing axiom report: ' + name)
    if reports[name] - allowed:
        raise SystemExit('unexpected axioms: ' + name + ': ' + str(reports[name] - allowed))
print('PASS: all six EKR declarations have only allowed transitive axioms')
