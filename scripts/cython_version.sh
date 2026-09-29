#!/bin/bash

# 1. A legfrissebb Cython verzió lekérdezése
LATEST_CYTHON=$(curl -s https://pypi.org/pypi/cython/json | python3 -c "import sys, json; print(json.load(sys.stdin)['info']['version'])")

echo "A legfrissebb Cython verzió a PyPI-on: $LATEST_CYTHON"
echo "----------------------------------------------------------------------"
echo "Verziók ellenőrzése kiadási dátummal (3.2.0-ig):"

# 2. Iteráció, ellenőrzés és dátum-kinyerés
python3 -c '
import urllib.request
import json
import sys

latest_version_str = "'"$LATEST_CYTHON"'"

try:
    major, minor, patch = map(int, latest_version_str.split("."))
except ValueError:
    print(f"Nem szabványos verzióformátum: {latest_version_str}")
    sys.exit(1)

url = "https://pypi.org/pypi/cython/json"
req = urllib.request.urlopen(url)
pypi_data = json.loads(req.read().decode("utf-8"))
existing_releases = pypi_data.get("releases", {})

curr_major, curr_minor, curr_patch = major, minor, patch

while True:
    ver_str = f"{curr_major}.{curr_minor}.{curr_patch}"
    
    if ver_str in existing_releases and len(existing_releases[ver_str]) > 0:
        files = existing_releases[ver_str]
        
        # Több opciót is megpróbálunk a dátum kinyerésére a fájlok közül
        release_date = "Ismeretlen dátum"
        for f in files:
            # Először az upload_time_iso-t keressük, utána az upload_time-ot
            date_val = f.get("upload_time_iso") or f.get("upload_time")
            if date_val:
                # Elővesszük az YYYY-MM-DD részt
                release_date = date_val.split("T")[0].split(" ")[0]
                break
            
        print(f"[LÉTEZIK]   {ver_str:<10} (Kiadás dátuma: {release_date})")
    else:
        print(f"[NINCS]     {ver_str:<10}")

    if curr_major == 3 and curr_minor == 2 and curr_patch == 0:
        break

    if curr_patch > 0:
        curr_patch -= 1
    else:
        curr_minor -= 1
        matching_patches = [
            int(r.split(".")[2]) for r in existing_releases.keys()
            if r.startswith(f"{curr_major}.{curr_minor}.") and r.split(".")[2].isdigit()
        ]
        curr_patch = max(matching_patches) if matching_patches else 0

    if curr_minor < 2 or curr_major < 3:
        break
'
