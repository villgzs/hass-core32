e```
cat > /config/check_ha_packages.py << 'EOF'
#!/usr/bin/env python3
"""
Home Assistant Core csomagok verzió-ellenőrzője.
Minden telepített csomagnál megpróbálja importálni és kiírni a verzióját.
"""

from __future__ import annotations

import importlib
import importlib.metadata
import sys
from typing import Optional

# Néhány csomagnál a pip neve ≠ az import név
IMPORT_NAME_MAP = {
    "Pillow": "PIL",
    "PyYAML": "yaml",
    "PyJWT": "jwt",
    "python-slugify": "slugify",
    "PyTurboJPEG": "turbojpeg",
    "opencv-python-headless": "cv2",
    "opencv-python": "cv2",
    "opencv-contrib-python": "cv2",
    "scikit-learn": "sklearn",
    "scikit-image": "skimage",
    "beautifulsoup4": "bs4",
    "protobuf": "google.protobuf",
    "pyserial": "serial",
    "pyserial-asyncio": "serial_asyncio",
    "pyserial-asyncio-fast": "serial_asyncio_fast",
    "Ruamel.yaml": "ruamel.yaml",
    "ruamel.yaml": "ruamel.yaml",
    "attrs": "attr",
    "typing-extensions": "typing_extensions",
    "importlib-metadata": "importlib.metadata",
    "importlib-resources": "importlib.resources",
    "backports.zoneinfo": "backports.zoneinfo",
    "async-timeout": "async_timeout",
    "frozenlist": "frozenlist",
    "multidict": "multidict",
    "yarl": "yarl",
    "aiohttp": "aiohttp",
    "home-assistant-bluetooth": "home_assistant_bluetooth",
    "ha-ffmpeg": "haffmpeg",
    "hass-nabucasa": "hass_nabucasa",
    "home-assistant-frontend": "hass_frontend",
    "home-assistant-intents": "home_assistant_intents",
}


def get_installed_distributions() -> list[tuple[str, str]]:
    """Visszaadja a telepített csomagokat (név, verzió) listaként."""
    dists = []
    for dist in importlib.metadata.distributions():
        name = dist.metadata.get("Name") or dist.metadata.get("name")
        version = dist.version
        if name and version:
            dists.append((name, version))
    # ABC sorrend
    dists.sort(key=lambda x: x[0].lower())
    return dists


def guess_import_name(pkg_name: str) -> str:
    """Pip névből megpróbálja kitalálni az import nevet."""
    if pkg_name in IMPORT_NAME_MAP:
        return IMPORT_NAME_MAP[pkg_name]

    # leggyakoribb átalakítások
    name = pkg_name.replace("-", "_")
    return name


def get_module_version(module) -> Optional[str]:
    """Különböző helyeken keresi a verziót a modulban."""
    for attr in ("__version__", "VERSION", "version", "__VERSION__"):
        v = getattr(module, attr, None)
        if v is not None:
            return str(v)

    # néha a version egy objektum
    ver_obj = getattr(module, "version", None)
    if ver_obj is not None and hasattr(ver_obj, "__str__"):
        return str(ver_obj)

    return None


def check_package(pkg_name: str, pkg_version: str) -> None:

    print(f"{pkg_name:40}", end="")  
    import_name = guess_import_name(pkg_name)

    try:
        mod = importlib.import_module(import_name)
    except Exception as e:
        print(f"pip={pkg_version:12}  IMPORT FAIL: {type(e).__name__}: {e}")
        return

    mod_version = get_module_version(mod)

    if mod_version is None:
        print(f"{pkg_name:40}  pip={pkg_version:12}  import={import_name:25}  (nincs __version__)")
    else:
        match = "OK" if mod_version == pkg_version else "DIFF"
        print(
            f"{pkg_name:40}  pip={pkg_version:12}  "
            f"import={import_name:25}  mod={mod_version:12}  [{match}]"
        )


def main() -> None:
    print(f"Python: {sys.version}")
    print(f"Prefix: {sys.prefix}")
    print("-" * 100)

    packages = get_installed_distributions()
    print(f"Telepített csomagok száma: {len(packages)}\n")

    for name, version in packages:
        check_package(name, version)

    print("-" * 100)
    print("Kész.")


if __name__ == "__main__":
    main()

EOF
```
