#!/bin/bash

echo "=== Telepített Python csomagok armv7l kompatibilitási ellenőrzése ==="
echo

pip list --format=freeze | while IFS='==' read -r pkg version; do
    location=$(python -c "
import importlib.util, sys
try:
    spec = importlib.util.find_spec('$pkg')
    print(spec.origin if spec and spec.origin else '')
except:
    print('')
" 2>/dev/null)

    [ -z "$location" ] && continue

    pkg_dir=$(dirname "$location")
    so_files=$(find "$pkg_dir" -name "*.so" -o -name "*.so.*" 2>/dev/null)

    [ -z "$so_files" ] && continue   # tiszta Python → OK

    echo "Csomag: $pkg==$version"

    for so in $so_files; do
        # 1. Fájlnév alapú gyors ellenőrzés (legmegbízhatóbb ennél a környezetnél)
        if echo "$so" | grep -qE 'arm-linux-musleabihf|armv7l|armhf'; then
            echo "  ✓ OK (fájlnév alapján): $(basename "$so")"
        else
            # 2. Ha van readelf, azzal is megnézzük
            if command -v readelf >/dev/null 2>&1; then
                arch=$(readelf -h "$so" 2>/dev/null | grep -E 'Machine:|Class:')
                if echo "$arch" | grep -qiE 'ARM|32-bit'; then
                    echo "  ✓ OK (readelf): $(basename "$so")"
                else
                    echo "  ✗ HIBA: $(basename "$so") → $arch"
                fi
            else
                echo "  ? Ismeretlen: $(basename "$so") (nincs file/readelf)"
            fi
        fi
    done
    echo
done

echo "=== Ellenőrzés kész ==="
