#!/bin/bash

echo "=== Telepített Python csomagok armv7l kompatibilitási ellenőrzése ==="
echo

# Csak azokat a csomagokat nézzük, amiknek van natív kódja
pip list --format=freeze | while IFS='==' read -r pkg version; do
    # Csomag helyének megkeresése
    location=$(python -c "import importlib.util, sys; spec = importlib.util.find_spec('$pkg'); print(spec.origin if spec and spec.origin else '')" 2>/dev/null)
    
    if [ -z "$location" ]; then
        continue
    fi

    # A csomag könyvtárának meghatározása
    pkg_dir=$(dirname "$location")
    
    # .so fájlok keresése a csomagban
    so_files=$(find "$pkg_dir" -name "*.so" -o -name "*.so.*" 2>/dev/null)
    
    if [ -z "$so_files" ]; then
        # Nincs natív kód → tiszta Python → OK
        continue
    fi

    echo "Csomag: $pkg==$version"
    
    for so in $so_files; do
        # Architektúra ellenőrzése
        arch_info=$(file "$so" 2>/dev/null)
        
        if echo "$arch_info" | grep -qE 'ARM|armv7|armhf|32-bit'; then
            # További részletes ellenőrzés (NEON, VFP stb. ha kell)
            cpu_arch=$(readelf -A "$so" 2>/dev/null | grep -E 'Tag_CPU_arch|Tag_CPU_name|Tag_Advanced_SIMD' | head -5)
            echo "  ✓ OK: $(basename "$so")"
            # echo "    $cpu_arch"   # ha részletesebb infót akarsz
        else
            echo "  ✗ HIBA: $(basename "$so") → $arch_info"
            echo "    Ez a fájl NEM armv7l kompatibilis!"
        fi
    done
    echo
done

echo "=== Ellenőrzés kész ==="
