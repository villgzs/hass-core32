The image `ghcr.io/villgzs/hass-core32:2026.9.3` is a **32-bit ARM** (linux/arm/v7) build of Home Assistant Core.  
On an AMD64 host you must run it with QEMU emulation.

### 1. Enable QEMU emulation (needed only once)

```bash
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

### 2. Pull the image with the correct platform

```bash
docker pull --platform linux/arm/v7 ghcr.io/villgzs/hass-core32:2026.9.3
```

### 3. Run the container

Recommended command (based on the official repository):

```bash
docker run -d \
  --name homeassistant \
  --platform linux/arm/v7 \
  --network host \
  --restart unless-stopped \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  -v /path/to/your/config:/config \
  -v /etc/localtime:/etc/localtime:ro \
  -v /run/dbus:/run/dbus:ro \
  ghcr.io/villgzs/hass-core32:2026.9.3
```

**Important notes:**
- Replace `/path/to/your/config` with a real directory on your host (e.g. `~/ha-config`).
- The `--platform linux/arm/v7` flag is mandatory, otherwise you will get an `exec format error`.
- `--network host` is strongly recommended for Home Assistant (discovery and many integrations won’t work properly without it).

### Quick test run (without config)

```bash
docker run --rm -it \
  --platform linux/arm/v7 \
  --network host \
  ghcr.io/villgzs/hass-core32:2026.9.3
```

### Check if it is running

```bash
docker ps
docker logs -f homeassistant
```

The web interface should be available at `http://localhost:8123`.

If you get any error (especially `exec format error` or the container exits immediately), please paste the exact error message.

---

A `ghcr.io/villgzs/hass-core32` image **32 bites ARM** (arm/v7) Home Assistant Core.  
AMD64 gépen QEMU emulációval kell futtatni.

### 1. QEMU emuláció bekapcsolása (egyszer kell)

```bash
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

### 2. Image letöltése a megfelelő platformmal

```bash
docker pull --platform linux/arm/v7 ghcr.io/villgzs/hass-core32:2026.9.3
```

### 3. Konténer indítása

Ajánlott parancs (a hivatalos repo alapján módosítva):

```bash
docker run -d \
  --name homeassistant \
  --platform linux/arm/v7 \
  --network host \
  --restart unless-stopped \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  -v /útvonal/a/configodhoz:/config \
  -v /etc/localtime:/etc/localtime:ro \
  -v /run/dbus:/run/dbus:ro \
  ghcr.io/villgzs/hass-core32:2026.9.3
```

**Fontos:**
- Cseréld ki a `/útvonal/a/configodhoz` részt egy létező mappára (pl. `~/ha-config`).
- A `--platform linux/arm/v7` elengedhetetlen, különben `exec format error` lesz.
- `--network host` kell a Home Assistantnak (különben a discovery és sok integráció nem működik jól).

### Gyors teszt indítás (config nélkül)

Ha csak kipróbálni akarod:

```bash
docker run --rm -it \
  --platform linux/arm/v7 \
  --network host \
  ghcr.io/villgzs/hass-core32:2026.9.3
```

### Ellenőrzés

```bash
docker ps
docker logs -f homeassistant
```

A webes felület általában a `http://localhost:8123` címen érhető el.

Ha hibát kapsz (pl. `exec format error` vagy a konténer azonnal kilép), írd meg a pontos hibaüzenetet.
