A bővebb logoláshoz a Home Assistantnak a `LOGGER` környezeti változót kell beállítani.

### Ajánlott indítás (debug szintű loggal)

```bash
docker run -d \
  --name homeassistant \
  --platform linux/arm/v7 \
  --network host \
  --restart unless-stopped \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  -e LOGGER=debug \
  -v /home/zsolti/hass/dockeremu/config:/config \
  -v /etc/localtime:/etc/localtime:ro \
  -v /run/dbus:/run/dbus:ro \
  ghcr.io/villgzs/hass-core32:2026.9.3
```

### Még részletesebb log (ha kell)

Ha a `debug` még nem elég, használhatod ezt:

```bash
-e LOGGER=debug \
-e PYTHONUNBUFFERED=1
```

### Logok követése

Indítás után:

```bash
docker logs -f --tail 200 homeassistant
```

vagy időbélyeggel:

```bash
docker logs -f -t homeassistant
```

---

**Megjegyzés:**  
A `LOGGER=debug` jelentősen több sort fog produkálni, különösen a Zeroconf / hálózati részeknél. Ha a konténer hamar leáll, a logok így jobban láthatóvá teszik, pontosan hol bukik el.
