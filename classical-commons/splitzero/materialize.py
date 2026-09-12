#!/usr/bin/env python3
"""Materialize the exact, independently verified SplitZero source workspace.

Existing conflicting files are never overwritten. No host Lean configuration is changed.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent

def main() -> None:
    spec = json.loads((ROOT / 'source.json').read_text(encoding='utf-8'))
    if not re.fullmatch(r'[0-9a-f]{40}', spec['commit']):
        raise ValueError('The source commit must be an immutable Git SHA')
    if spec['repository'] != 'KokunoYumeto/zeta-function-research-reader':
        raise ValueError('Unexpected source repository')
    target = ROOT / '.workspace'
    target.mkdir(exist_ok=True)
    for name in spec['files']:
        if Path(name).name != name or name in {'.', '..'}:
            raise ValueError(f'Unsafe source path: {name}')
        url = (f"https://raw.githubusercontent.com/{spec['repository']}/"
               f"{spec['commit']}/{spec['subdirectory']}/{name}")
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
        data.decode('utf-8')
        expected = spec['sha256'].get(name)
        actual = hashlib.sha256(data).hexdigest()
        if expected is not None and actual != expected:
            raise ValueError(f'Verified source hash mismatch: {name}')
        dest = target / name
        if dest.exists() and dest.read_bytes() != data:
            raise ValueError(f'Refusing to overwrite conflicting file: {dest}')
        dest.write_bytes(data)
    subprocess.run([sys.executable, 'prepare.py'], cwd=target, check=True)
    actual = hashlib.sha256((target / 'SplitZero.lean').read_bytes()).hexdigest()
    if actual != spec['original_core_sha256']:
        raise ValueError('Original SplitZero core SHA-256 mismatch')
    print(f"Verified {len(spec['sha256'])} pinned code/config files and the original core")
    print(f"Workspace: {target}")

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f'SplitZero materialization failed: {exc}') from exc
