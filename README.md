[**LICENSE**](https://raw.githubusercontent.com/home-assistant/workflows/refs/heads/main/LICENSE)

# Home Assistant Core (32-bit ARM Build) 

**Unsupported Third Party Container**

Originals:
- [Home-Assistant Core repository](https://github.com/home-assistant/core) 
- [Wheels](https://github.com/home-assistant/wheels) 
- [Docker](https://github.com/home-assistant/docker) 
- [Docker-base](https://github.com/home-assistant/docker-base)

You can find Home-assistant official releases here:  
[https://github.com/home-assistant/core/releases](https://github.com/home-assistant/core/releases)  

Latest official image can be found here:  
[https://github.com/home-assistant/core/pkgs/container/home-assistant?tag=latest](https://github.com/home-assistant/core/pkgs/container/home-assistant?tag=latest)

[**Home-assistant/core - actions for releases**](https://github.com/home-assistant/core/actions?query=event%3Arelease)  
[Home-assistant/docker - actions for releases](https://github.com/home-assistant/docker/actions?query=event%3Arelease)  

# THIS IS NOT OFFICIAL RELEASE !

---
⚠️ **IMPORTANT DISCLAIMER**

  **Unofficial Build:** This repository is not created or supported by the official Home Assistant team. Please do not submit issue reports or complaints to Home Assistant developers.

  **32-bit Deprecation:** [Official support for 32-bit systems (armv7) has ended.](https://www.home-assistant.io/blog/2025/05/22/deprecating-core-and-supervised-installation-methods-and-32-bit-systems/) This repository was created strictly for experimental/testing purposes, following the official build and release steps as closely as possible, though it was not always feasible to do so across all areas.

  **No Warranty & No Support:** This repository has not undergone thorough testing. Testing is limited to occasional spot checks, and no automated tests are integrated into the build process. Do not run this in a production environment.

  **Limitation of Liability:** The creator of this repository assumes no responsibility or liability for any failures, data loss, or damage to hardware. No claims or demands for damages will be entertained.

USE AT YOUR OWN RISK.
---

![Docker Image Version](https://img.shields.io/github/v/release/home-assistant/core?label=Home%20Assistant%20Core&color=blue)
![Architecture](https://img.shields.io/badge/Architecture-ARMv7-orange)
[![Build CORE-32-bit Home Assistant](https://github.com/villgzs/hass-core32/actions/workflows/builder.yml/badge.svg)](https://github.com/villgzs/hass-core32/actions/workflows/builder.yml)

# Home Assistant Core (32-bit ARM Build) and others
[*Github repository : hass-core32*](https://github.com/villgzs/hass-core32)   
[*ARMV7 - 32bit musllinux wheels*](https://villgzs.github.io/musllinux-index/)  

A custom Docker build of **Home Assistant Core** optimized exclusively for [**32-bit ARM (armv7)**](https://www.home-assistant.io/blog/2025/05/22/deprecating-core-and-supervised-installation-methods-and-32-bit-systems/) architecture. It is designed for older Raspberry Pi models, [**Orange Pi Zero**](https://armbian.com/boards/orangepizero), and similar single-board computers, as well as Android phones running in a [**Termux + udocker**](https://github.com/villgzs/udocker_hass_core_alcatel) environment.  

Rather than relying on a single-step build, this repository orchestrates a complete, automated multi-stage build pipeline:  
- **Base Image Generation:** Builds the required foundational base images directly from the upstream docker-base and docker repositories.
- **Custom Wheel Compilation:** Sets up a dedicated builder container from the wheels repository to pre-compile all necessary armv7 Python wheels required for the core build.
- **Core Image Assembly:** Fetches the latest stable Home Assistant Core source, applies custom container configurations, and builds the final runtime image using the pre-built wheels.
- **Automated Release Tracking & Nightly Builds:** Periodically checks for new upstream releases and automatically builds daily snapshots directly from the development (dev) branch.

## 🚀 Powered by Open Source

Huge credit goes to the [Home Assistant project](https://www.home-assistant.io/) and community. **Thanks to Home Assistant being fully open source**, even building a specialized 32-bit (armv7) variant is completely achievable—every single piece of information, build script, and dependency detail required to make this happen was openly available right inside the project. Deep appreciation goes out to everyone keeping this ecosystem transparent, welcoming, and accessible for older or unconventional hardware.

## 📦 Container Registry

The resulting images are published to the GitHub Container Registry (GHCR) and dockerhub:

```bash
ghcr.io/villgzs/hass-core32:<version>
dockergzs/armv7-homeassistant:<version>
dockergzs/homeassistant-armv7:<version>
```

## Run the container

Fill in ___PATH_TO_YOUR_CONFIG___ section:

```
docker run -d \
  --name homeassistant \
  --network host \
  --restart unless-stopped \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  -v /___PATH_TO_YOUR_CONFIG___:/config \
  -v /etc/localtime:/etc/localtime:ro \
  -v /run/dbus:/run/dbus:ro \
  dockergzs/armv7-homeassistant:<version>
```

## 🔗 Base Images, Including the Wheels Builder

- [DOCKERBASE ALPINE (base)](https://github.com/villgzs/hass-core32/pkgs/container/hass-core32-basealpine)
- [DOCKERBASE PYTHON (base-python)](https://github.com/villgzs/hass-core32/pkgs/container/hass-core32-basepython)
- [DOCKER (homeassistant-base)](https://github.com/villgzs/hass-core32/pkgs/container/hass-core32-baseadded)
- [Wheels builder](https://github.com/villgzs/hass-core32/pkgs/container/hass-core32-wheeler)

## 💡 Additional options / availability for armv7 core image

- [Github - Andrew Youll and Andrew Youll](https://github.com/adyoull/HA-ARMv7)
- [Github - Petr Gregor](https://github.com/Gregy/homeassistant-armv7) and [Dockerhub](https://hub.docker.com/r/gregy/homeassistant-armv7)
- [Don't forget the latest official](https://hub.docker.com/r/homeassistant/armv7-homeassistant/tags)
- [Results of this repo ](https://hub.docker.com/r/dockergzs/homeassistant-armv7/tags)

