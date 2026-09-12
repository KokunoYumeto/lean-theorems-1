#!/usr/bin/env python3
"""Materialize the exact SplitZero source workspace and verify declared byte pins.

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
    sha_pins = spec['sha256']
    blob_pins = spec.get('git_blob', {})
    required = {
        'SplitZeroExtension.lean', 'SplitZeroFibres.lean', 'SplitZeroPresentation.lean',
        'SplitZeroMaps.lean', 'SplitZeroSynchronization.lean', 'Audit.lean',
        'check_axioms.py', 'prepare.py', 'check_synchronization.py',
        'test_synchronization_checker.py', 'lakefile.toml', 'lean-toolchain',
    }
    if not required <= set(sha_pins) | set(blob_pins):
        raise ValueError('Required proof/configuration file is missing a byte pin')
    if not required <= set(spec['files']):
        raise ValueError('Required proof/configuration file is missing from the materialization list')
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
        expected = sha_pins.get(name)
        actual = hashlib.sha256(data).hexdigest()
        if expected is not None and actual != expected:
            raise ValueError(f'Verified source SHA-256 mismatch: {name}')
        expected_blob = blob_pins.get(name)
        actual_blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if expected_blob is not None and actual_blob != expected_blob:
            raise ValueError(f'Verified source Git blob mismatch: {name}')
        dest = target / name
        if dest.exists() and dest.read_bytes() != data:
            raise ValueError(f'Refusing to overwrite conflicting file: {dest}')
        dest.write_bytes(data)
    subprocess.run([sys.executable, 'prepare.py'], cwd=target, check=True)
    actual = hashlib.sha256((target / 'SplitZero.lean').read_bytes()).hexdigest()
    if actual != spec['original_core_sha256']:
        raise ValueError('Original SplitZero core SHA-256 mismatch')
    print(f"Verified {len(set(sha_pins) | set(blob_pins))} pinned code/config files and the original core")
    print(f"Workspace: {target}")

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f'SplitZero materialization failed: {exc}') from exc
