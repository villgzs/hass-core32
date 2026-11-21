#!/bin/bash

echo "=== Telepített Python csomagok armv7l kompatibilitási ellenőrzése ==="
echo

apk add file

pip list --format=freeze | while IFS='==' read -r pkg version; do
    location=$(python -c "
import importlib.util
try:
    spec = importlib.util.find_spec('$pkg')
    print(spec.origin if spec and spec.origin else '')
except Exception:
    print('')
" 2>/dev/null)

    [ -z "$location" ] && continue
    pkg_dir=$(dirname "$location")

    # Csak a Python extensionöket nézzük, a bundled libeket kihagyjuk
    so_files=$(find "$pkg_dir" -type f \( -name "*.so" -o -name "*.so.*" \) 2>/dev/null \
        | grep -vE 'libstdc\+\+|libgcc_s|liblzma|libffi|libssl|libcrypto|libz\.|libbz2')

    [ -z "$so_files" ] && continue

    echo "Csomag: $pkg==$version"
    has_error=0

    for so in $so_files; do
        base=$(basename "$so")
        info=$(file -b "$so" 2>/dev/null)

        # Ellenőrzés: ARM 32-bit + ELF
        if echo "$info" | grep -qiE 'ELF.*32-bit.*ARM|ARM.*32-bit'; then
            echo "  ✓ OK: $base"
        else
            echo "  ✗ HIBA: $base"
            echo "       → $info"
            has_error=1
        fi
    done

    if [ $has_error -eq 1 ]; then
        echo "  *** Ez a csomag NEM armv7l kompatibilis! ***"
    fi
    echo
done

echo "=== Ellenőrzés kész ==="
