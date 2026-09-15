**Igen, sajnos ez ismert korlátozás.**

Az `actions/upload-artifact` + `actions/download-artifact` **nem őrzi meg** a fájlok execute bitjét (`+x`). A dokumentáció szerint minden fájl `644`, minden könyvtár `755` lesz a letöltés után.

### Nincs paraméter, ami megőrizné

Nincs olyan `with:` opció a hivatalos action-ben, ami megtartaná a jogosultságokat.

### Megoldások

### 1. Legjobb és legegyszerűbb (ajánlott neked)

A letöltés után egyszerűen állítsd vissza:

```yaml
- name: Download prepared source
  uses: actions/download-artifact@v4
  with:
    name: ha-core-prepared
    path: ha-core

- name: Restore execute permissions
  run: |
    chmod +x ha-core/rootfs/init
    ls -l ha-core/rootfs/init
```

### 2. Tar-os megoldás (ha sok fájlnál kell a jog)

**Upload oldalon** (`prepare` job végén):

```yaml
- name: Create tar with permissions
  run: |
    cd ha-core
    tar -cvf ../ha-core-prepared.tar .
    
- name: Upload prepared source (tar)
  uses: actions/upload-artifact@v4
  with:
    name: ha-core-prepared
    path: ha-core-prepared.tar
```

**Download oldalon** (build jobokban):

```yaml
- name: Download prepared source
  uses: actions/download-artifact@v4
  with:
    name: ha-core-prepared
    path: .

- name: Extract tar (permissions preserved)
  run: |
    mkdir -p ha-core
    tar -xvf ha-core-prepared.tar -C ha-core
    ls -l ha-core/rootfs/init
```

### 3. Dockerfile-ban védekezés (legbiztosabb)

```dockerfile
COPY rootfs /
RUN chmod +x /init
```

---

**Összefoglalva a jelenlegi helyzetedre:**

Mivel csak az `/init`-re van szükséged, a **1. megoldás** (chmod a download után) a legegyszerűbb és leggyorsabb. A Dockerfile-ba tett `RUN chmod +x /init` pedig extra biztonságot ad.
