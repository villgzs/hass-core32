You can find Home-assistant releases here:

[https://github.com/home-assistant/core/releases](https://github.com/home-assistant/core/releases)

Latest official image can be found here:

[https://github.com/home-assistant/core/pkgs/container/home-assistant/1201250336?tag=latest](https://github.com/home-assistant/core/pkgs/container/home-assistant/1201250336?tag=latest)

# THIS IS NOT OFFICIAL RELEASE !

---
⚠️ **IMPORTANT DISCLAIMER**

  Unofficial Build: This repository is not created or supported by the official Home Assistant team. Please do not submit issue reports or complaints to Home Assistant developers.

  32-bit Deprecation: Official support for 32-bit systems (armv7) has ended. This repository was created strictly for experimental/testing purposes following official build instructions.

  No Warranty & No Support: This repository is untested and unmaintained. Do not run this in a production environment.

  Limitation of Liability: The creator of this repository assumes no responsibility or liability for any failures, data loss, or damage to hardware. No claims or demands for damages will be entertained.

USE AT YOUR OWN RISK.
---

Prerequisited: Step No.3 - basic-added

### STEP No.4 

# Home Assistant Core (32-bit ARM Build)

![Docker Image Version](https://img.shields.io/github/v/release/home-assistant/core?label=Home%20Assistant%20Core&color=blue)
![Architecture](https://img.shields.io/badge/Architecture-ARMv6%20%7C%20ARMv7-orange)
![Build Status](https://img.shields.io/github/actions/workflow/status/villgzs/hass-core32/build.yml?label=Build)

A custom Docker build of **Home Assistant Core** optimized for 32-bit ARM architectures (`linux/arm/v7` and `linux/arm/v6`), such as older Raspberry Pi models. This repository automatically fetches the latest stable Home Assistant Core source, replaces the standard container configuration, and builds a multi-architecture container image.

---

## 🚀 Key Features

- **32-Bit ARM Support:** Pre-built binaries targeting `linux/arm/v7` (Raspberry Pi 2/3/4 32-bit OS) and `linux/arm/v6` (Raspberry Pi 1/Zero).
- **Fast Dependency Management:** Uses [`uv`](https://github.com/astral-sh/uv) for high-speed Python package installation during container builds.
- **Integrated `go2rtc`:** Includes a pre-installed `go2rtc` binary (`v1.9.14`) for ultra-low latency camera streaming.
- **Automated Nightly Builds:** GitHub Actions workflow automatically tracks and builds the latest official stable Home Assistant release daily.
- **Multi-Arch Manifest:** Automatically published as a unified image tag supporting multiple 32-bit platforms.

---

## 📦 Container Registry

The resulting images are published to the GitHub Container Registry (GHCR):

```bash
ghcr.io/villgzs/hass-core32:latest
ghcr.io/villgzs/hass-core32:<version>
