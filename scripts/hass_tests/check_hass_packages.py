#!/usr/bin/env python3
"""Isolated Home Assistant / hass-* package crash probe (Python 3.11+).
Run using the SAME Python interpreter as Home Assistant. Does not start HA.
"""
import argparse
import importlib
import importlib.metadata as md
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import traceback

CORE = ['homeassistant', 'homeassistant.core', 'homeassistant.config',
        'homeassistant.loader', 'homeassistant.helpers',
        'homeassistant.helpers.template', 'homeassistant.helpers.event',
        'homeassistant.helpers.entity', 'homeassistant.helpers.storage',
        'homeassistant.components.http', 'homeassistant.components.websocket_api',
        'homeassistant.components.frontend', 'homeassistant.components.recorder',
        'homeassistant.components.mqtt', 'homeassistant.components.sensor']

def installed():
    found = {}
    for d in md.distributions():
        name = d.metadata.get('Name', '')
        if name.lower().startswith(('hass-', 'home-assistant-', 'homeassistant-')):
            modules = list(d.read_text('top_level.txt').splitlines()) if d.read_text('top_level.txt') else []
            if not modules:
                modules = [x for x in d.files or [] if len(x.parts) == 2 and x.name == '__init__.py']
                modules = [x.parts[0] for x in modules]
            found[name] = {'version': d.version, 'modules': sorted(set(x for x in modules if x.isidentifier()))}
    return dict(sorted(found.items(), key=lambda x: x[0].lower()))

def child(kind, target):
    try:
        if kind == 'import':
            m = importlib.import_module(target)
            print('IMPORTED', target, getattr(m, '__file__', 'namespace'), flush=True)
        elif kind == 'files':
            m = importlib.import_module(target)
            root = Path(m.__file__).parent
            count = size = 0
            for p in root.rglob('*'):
                if p.is_file():
                    with p.open('rb') as f:
                        while chunk := f.read(1024 * 1024):
                            size += len(chunk)
                    count += 1
            print('READ', count, 'files', size, 'bytes', flush=True)
        elif kind == 'frontend-json':
            import hass_frontend
            root = Path(hass_frontend.__file__).parent
            import json as stdjson
            count = 0
            for p in root.rglob('*.json'):
                with p.open('r', encoding='utf-8') as f:
                    stdjson.load(f)
                count += 1
            print('PARSED', count, 'JSON files', flush=True)
        elif kind == 'ha-config':
            from homeassistant.config import async_hass_config_yaml
            print('HA CONFIG IMPORT OK', async_hass_config_yaml.__name__, flush=True)
        else:
            raise ValueError(kind)
        return 0
    except Exception:
        traceback.print_exc()
        return 1

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--timeout', type=int, default=45)
    p.add_argument('--json', default='hass_package_results.json')
    p.add_argument('--core', action='store_true', help='also import selected Home Assistant core modules')
    p.add_argument('--frontend', action='store_true', help='read all frontend files and parse frontend JSON')
    p.add_argument('--list', action='store_true', help='list detected packages only')
    p.add_argument('--only', help='substring filter for test names')
    p.add_argument('--child', nargs=2, metavar=('KIND', 'TARGET'), help=argparse.SUPPRESS)
    args = p.parse_args()
    if args.child:
        return child(*args.child)
    packages = installed()
    print('Interpreter:', sys.executable, 'Python:', sys.version.split()[0], flush=True)
    print('Detected packages:', json.dumps(packages, indent=2), flush=True)
    if args.list:
        return 0
    tests = []
    for name, info in packages.items():
        for module in info['modules']:
            tests.append(('import', module, f'{name}: {module}'))
        if not info['modules']:
            print('NO IMPORT NAME:', name, '(metadata only; not tested)', flush=True)
    if args.core:
        tests += [('import', x, x) for x in CORE]
        tests.append(('ha-config', '-', 'homeassistant config import'))
    if args.frontend:
        tests += [('files', 'hass_frontend', 'hass_frontend read all files'),
                  ('frontend-json', '-', 'hass_frontend parse JSON')]
    # De-duplicate identical work, preserving names.
    seen = set()
    tests = [x for x in tests if not ((x[0], x[1]) in seen or seen.add((x[0], x[1])))]
    if args.only:
        tests = [x for x in tests if args.only.lower() in x[2].lower()]
    results = []
    for kind, target, name in tests:
        print(f'{name[:52]:52} ', end='', flush=True)
        start = time.monotonic()
        try:
            proc = subprocess.run([sys.executable, '-X', 'faulthandler', os.path.abspath(__file__),
                                   '--child', kind, target], capture_output=True, text=True,
                                  timeout=args.timeout, env={**os.environ, 'PYTHONUNBUFFERED':'1'})
            if proc.returncode == 0:
                status = 'PASS'
            elif proc.returncode < 0:
                num = -proc.returncode
                status = signal.Signals(num).name if num in signal.Signals._value2member_map_ else f'SIGNAL {num}'
            else:
                status = f'FAIL ({proc.returncode})'
            out, err = proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as exc:
            status, out, err = 'TIMEOUT', (exc.stdout or b''), (exc.stderr or b'')
            if isinstance(out, bytes): out = out.decode(errors='replace')
            if isinstance(err, bytes): err = err.decode(errors='replace')
        duration = round(time.monotonic() - start, 2)
        print(f'{status} ({duration}s)', flush=True)
        if status != 'PASS':
            if out: print(out.rstrip(), flush=True)
            if err: print(err.rstrip(), flush=True)
        results.append(dict(test=name, kind=kind, target=target, status=status,
                            seconds=duration, stdout=out, stderr=err))
    summary = {s: sum(x['status'] == s for x in results) for s in sorted(set(x['status'] for x in results))}
    print('SUMMARY:', summary, flush=True)
    if args.json:
        with open(args.json, 'w') as f:
            json.dump(dict(interpreter=sys.executable, python=sys.version, packages=packages,
                           results=results, summary=summary), f, indent=2)
        print('JSON:', args.json, flush=True)
    return int(any(x['status'] != 'PASS' for x in results))

if __name__ == '__main__':
    sys.exit(main())
