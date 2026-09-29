#!/usr/bin/env python3
"""Home Assistant native dependency crash diagnostic. Python 3.11+."""
import argparse
import importlib.util
import json
import os
import signal
import subprocess
import sys
import time
import traceback

TESTS = {
    'python-basics': '''a=list(range(10000)); b={i:i*i for i in a}; assert b[9999]==9999**2''',
    'orjson': '''import orjson; d={'a':list(range(100)),'b':'x'*1000};\nfor i in range(300):\n raw=orjson.dumps(d); assert orjson.loads(raw)==d''',
    'json': '''import json; d={'a':list(range(100))};\nfor i in range(200):\n assert json.loads(json.dumps(d))==d''',
    'aiohttp': '''import asyncio, aiohttp
async def run():
 async def handle(reader, writer):
  await reader.readuntil(b'\\r\\n\\r\\n')
  writer.write(b'HTTP/1.1 200 OK\\r\\nContent-Length: 2\\r\\nConnection: close\\r\\n\\r\\nOK')
  await writer.drain()
  writer.close()
  await writer.wait_closed()
 server = await asyncio.start_server(handle, '127.0.0.1', 0)
 try:
  port = server.sockets[0].getsockname()[1]
  async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
   for _ in range(30):
    async with session.get(f'http://127.0.0.1:{port}/') as response:
     assert response.status == 200
     assert await response.text() == 'OK'
 finally:
  server.close()
  await server.wait_closed()
asyncio.run(run())''',
    'multidict': '''from multidict import MultiDict; d=MultiDict([('a','1'),('a','2')]); assert d.getall('a')==['1','2']''',
    'yarl': '''from yarl import URL; u=URL('https://example.com/a?q=1'); assert u.host=='example.com' and u.query['q']=='1' ''',
    'propcache': '''from propcache import cached_property;\nclass A:\n @cached_property\n def x(self): return 42\na=A(); assert a.x==42''',
    'cryptography': '''from cryptography.hazmat.primitives import hashes; from cryptography.hazmat.primitives.ciphers.aead import AESGCM; h=hashes.Hash(hashes.SHA256()); h.update(b'test'); assert len(h.finalize())==32; a=AESGCM(b'0'*16); ct=a.encrypt(b'1'*12,b'data',None); assert a.decrypt(b'1'*12,ct,None)==b'data' ''',
    'numpy': '''import numpy as np; a=np.arange(10000,dtype=np.float64).reshape(100,100); b=a@a.T; assert b.shape==(100,100) and np.isfinite(b).all()''',
    'yaml': '''import yaml; d={'x':[1,2,3]}; assert yaml.safe_load(yaml.safe_dump(d))==d; assert getattr(yaml,'__with_libyaml__',False)''',
    'ciso8601': '''import ciso8601; d=ciso8601.parse_datetime('2026-09-27T12:34:56+02:00'); assert d.year==2026''',
    'lru': '''from lru import LRU; d=LRU(2); d['a']=1; d['b']=2; assert d['a']==1''',
    'zlib_ng': '''from zlib_ng import zlib_ng; d=b'abc'*10000; assert zlib_ng.decompress(zlib_ng.compress(d))==d''',
    'brotli': '''import brotli; d=b'abc'*10000; assert brotli.decompress(brotli.compress(d))==d''',
    'msgpack': '''import msgpack; d={'x':list(range(100))}; assert msgpack.unpackb(msgpack.packb(d))==d''',
    'PIL': '''from PIL import Image; import io; im=Image.new('RGB',(64,64),'red'); b=io.BytesIO(); im.save(b,format='PNG'); b.seek(0); assert Image.open(b).size==(64,64)''',
    'sqlite3': '''import sqlite3; c=sqlite3.connect(':memory:'); c.execute('create table t (x integer)'); c.executemany('insert into t values (?)',[(i,) for i in range(1000)]); assert c.execute('select sum(x) from t').fetchone()[0]==499500; c.close()''',
    'ssl': '''import ssl; assert ssl.OPENSSL_VERSION; ssl.create_default_context()''',
    'gc-stress': '''import gc; a=[];\nfor i in range(40):\n a.append(bytearray(65536));\n if i%10==0: gc.collect()\ndel a; gc.collect()''',
}

# Import name, pip distribution name may differ. Missing optional packages are SKIP.
OPTIONAL = {'numpy','ciso8601','lru','zlib_ng','brotli','msgpack','PIL'}

def child(name):
    import faulthandler
    faulthandler.enable(all_threads=True)
    print('Python:', sys.version.split()[0], 'Test:', name, flush=True)
    try:
        exec(compile(TESTS[name], '<test:'+name+'>', 'exec'), {})
    except Exception:
        traceback.print_exc()
        return 1
    print('PASS', flush=True)
    return 0

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--timeout',type=int,default=30,help='seconds per test (default: 30)')
    p.add_argument('--json',dest='json_path',help='write structured results')
    p.add_argument('--only',nargs='+',choices=list(TESTS),help='run selected tests')
    p.add_argument('--include-optional',action='store_true',help='include optional packages')
    p.add_argument('--child',choices=list(TESTS),help=argparse.SUPPRESS)
    args=p.parse_args()
    if args.child: return child(args.child)
    names=args.only or list(TESTS)
    results=[]
    print('Interpreter:',sys.executable, '\nPython:',sys.version.split()[0],flush=True)
    for name in names:
        if name in OPTIONAL and not args.include_optional and args.only is None:
            continue
        if name in OPTIONAL and importlib.util.find_spec(name) is None:
            print(f'{name:18} SKIP (not installed)',flush=True)
            results.append({'test':name,'status':'SKIP','reason':'not installed'})
            continue
        print(f'{name:18} ',end='',flush=True)
        start=time.monotonic()
        try:
            r=subprocess.run([sys.executable,os.path.abspath(__file__),'--child',name],capture_output=True,text=True,timeout=args.timeout,env={**os.environ,'PYTHONFAULTHANDLER':'1'})
            elapsed=round(time.monotonic()-start,2)
            if r.returncode==0: status='PASS'
            elif r.returncode<0:
                sig=-r.returncode
                status='SIG'+signal.Signals(sig).name.removeprefix('SIG') if sig in [x.value for x in signal.Signals] else f'SIGNAL {sig}'
            else: status=f'FAIL ({r.returncode})'
            results.append({'test':name,'status':status,'returncode':r.returncode,'seconds':elapsed,'stdout':r.stdout,'stderr':r.stderr})
            print(f'{status} ({elapsed}s)',flush=True)
            if status!='PASS':
                if r.stdout: print(r.stdout.rstrip())
                if r.stderr: print(r.stderr.rstrip())
        except subprocess.TimeoutExpired as exc:
            print('TIMEOUT',flush=True)
            results.append({'test':name,'status':'TIMEOUT','seconds':args.timeout})
    print('\nSUMMARY:', ' '.join(f'{s}={sum(x["status"]==s for x in results)}' for s in sorted({x['status'] for x in results})))
    if args.json_path:
        with open(args.json_path,'w') as f: json.dump({'interpreter':sys.executable,'results':results},f,indent=2)
        print('JSON:',args.json_path)
    return int(any(x['status'] not in ('PASS','SKIP') for x in results))

if __name__=='__main__': sys.exit(main())
