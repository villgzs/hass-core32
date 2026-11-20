cat > /tmp/check_sigbus.py << 'EOF'
#!/usr/bin/env python3
"""Home Assistant core – SIGBUS / natív modul gyorsteszt"""

import sys
import traceback

def test(name, fn):
    print(f"=== {name} ... ", end="", flush=True)
    try:
        fn()
        print("OK")
        return True
    except Exception as e:
        print("FAIL")
        traceback.print_exc()
        return False

results = []

# 1. Alap Python
results.append(test("python basics", lambda: (
    list(range(10000)),
    "".join(str(i) for i in range(1000)),
    {i: i*i for i in range(1000)}
)))

# 2. orjson (gyakori crash-forrás musl-en)
def test_orjson():
    import orjson
    data = {"a": list(range(100)), "b": "x" * 1000, "c": True, "d": None}
    for _ in range(500):
        raw = orjson.dumps(data)
        orjson.loads(raw)
results.append(test("orjson", test_orjson))

# 3. stdlib json (összehasonlítás)
def test_json():
    import json
    data = {"a": list(range(100)), "b": "x" * 1000}
    for _ in range(200):
        raw = json.dumps(data)
        json.loads(raw)
results.append(test("stdlib json", test_json))

# 4. aiohttp (C parser)
def test_aiohttp():
    import aiohttp
    # csak import + egyszerű objektum
    aiohttp.ClientTimeout(total=1)
results.append(test("aiohttp import", test_aiohttp))

# 5. multidict / yarl / propcache (aiohttp függőségek)
def test_aiohttp_deps():
    import multidict
    import yarl
    import propcache
    d = multidict.MultiDict([("a", "1"), ("b", "2")])
    u = yarl.URL("http://example.com/path?q=1")
    assert str(u.host) == "example.com"
results.append(test("multidict/yarl/propcache", test_aiohttp_deps))

# 6. cryptography
def test_crypto():
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    h = hashes.Hash(hashes.SHA256(), backend=default_backend())
    h.update(b"test" * 1000)
    h.finalize()
results.append(test("cryptography", test_crypto))

# 7. numpy (ha van)
def test_numpy():
    import numpy as np
    a = np.random.rand(100, 100)
    b = a @ a.T
    assert b.shape == (100, 100)
results.append(test("numpy", test_numpy))

# 8. Rövid memórianyomás + GC
def test_gc_stress():
    import gc
    junk = []
    for i in range(50):
        junk.append([bytearray(1024 * 64) for _ in range(20)])
        if i % 10 == 0:
            gc.collect()
    del junk
    gc.collect()
results.append(test("gc stress", test_gc_stress))

print("\n----- Összesítés -----")
ok = sum(1 for r in results if r)
fail = len(results) - ok
print(f"OK: {ok}  FAIL: {fail}")
if fail:
    sys.exit(1)
print("Minden teszt lefutott.")

import orjson, time
data = {'x': list(range(1000)), 's': 'y'*5000}
t0 = time.time()
while time.time() - t0 < 60:
    orjson.loads(orjson.dumps(data))
print('1 perc orjson OK')


EOF

python3 /tmp/check_sigbus.py
