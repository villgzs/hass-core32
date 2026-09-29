You can find Home-assistant releases here:

[https://github.com/home-assistant/core/releases](https://github.com/home-assistant/core/releases)

Latest official image can be found here:

[https://github.com/home-assistant/core/pkgs/container/home-assistant?tag=latest](https://github.com/home-assistant/core/pkgs/container/home-assistant?tag=latest)

# THIS IS NOT OFFICIAL RELEASE !

---
⚠️ **IMPORTANT DISCLAIMER**

  Unofficial Build: This repository is not created or supported by the official Home Assistant team. Please do not submit issue reports or complaints to Home Assistant developers.

  32-bit Deprecation: Official support for 32-bit systems (armv7) has ended. This repository was created strictly for experimental/testing purposes, following the official build and release steps as closely as possible, though it was not always feasible to do so across all areas.

  No Warranty & No Support: This repository is untested and unmaintained. Do not run this in a production environment.

  Limitation of Liability: The creator of this repository assumes no responsibility or liability for any failures, data loss, or damage to hardware. No claims or demands for damages will be entertained.

USE AT YOUR OWN RISK.
---

Prerequisited: Step No.3 - basic-added

### [Home-assistant/core - actions for releases](https://github.com/home-assistant/core/actions?query=event%3Arelease)

### STEP No.4 

# Home Assistant Core (32-bit ARM Build)

![Docker Image Version](https://img.shields.io/github/v/release/home-assistant/core?label=Home%20Assistant%20Core&color=blue)
![Architecture](https://img.shields.io/badge/Architecture-ARMv6%20%7C%20ARMv7-orange)
![Build Status](https://img.shields.io/github/actions/workflow/status/villgzs/hass-core32/builder.yml?label=Build)

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
  ghcr.io/villgzs/hass-core32:latest
```

Test script - possible bash shell and run option:

```
#!/bin/bash
# docker run -d   --name hass-core   --privileged   --restart=unless-stopped   --net=host   -e TZ="Europe/Budapest"   -v /home/hass/homeassistant-udocker/config:/config   dockergzs/hass-core:python3.14-alpine3.24-2026.7.2-armv7
# docker start hass-core
# docker run -d   --name homeassistant   --privileged   --restart=unless-stopped   --net=host   -e TZ="Europe/Budapest"   -v /home/hass/homeassistant-udocker/config:/config   ghcr.io/adyoull/ha-armv7:2026.7.2


if [ -z "$1" ]; then
    echo "Image legyen megadva tag-gel! Pl.: ghcr.io/villgzs/hass-core32:2026.9.3"
    echo "utána:"
    echo " run"
    echo " check"
    echo " bash - bár ez az alap, ha nincs megadva semmi."

    exit 1
fi

DOCKERNAME=$(basename "$0")
DOCKERNAME="${DOCKERNAME%.*}"
echo "Running dockerimage: $DOCKERNAME"

DOCKER_IMAGE="$1"

IMAGE_NAME="${DOCKER_IMAGE##*/}"
IMAGE_NAME="${IMAGE_NAME%%:*}"

IMAGE_TAG="${DOCKER_IMAGE#*:}"

echo "DOCKER_IMAGE: $DOCKER_IMAGE ; $IMAGE_TAG"
DOCKERCONFIG="config_${IMAGE_NAME}_$IMAGE_TAG/config"
echo "Docker config: $DOCKERCONFIG"

mkdir -p "$DOCKERCONFIG"
cp hass_tests/check_armv7.sh "$DOCKERCONFIG"
cp hass_tests/pymodul_check.sh "$DOCKERCONFIG"
cp hass_tests/chatgpt_pymodul_check.sh "$DOCKERCONFIG"
cp hass_tests/check_sigbus.py "$DOCKERCONFIG"
cp hass_tests/check_hass_packages.py "$DOCKERCONFIG"
cp hass_tests/chatgpt_hass_packages_test.sh "$DOCKERCONFIG"


docker pull "$DOCKER_IMAGE"

docker_run() {

  docker run -d   \
   --name "$DOCKERNAME" \
   --privileged \
   --net=host \
   -e TZ="Europe/Budapest" \
   --cap-add=NET_ADMIN \
   --cap-add=NET_RAW \
   -v /home/user/"$DOCKERCONFIG":/config \
   -v /etc/localtime:/etc/localtime:ro \
   -v /run/dbus:/run/dbus:ro \
   "$DOCKER_IMAGE"
}

docker_bash() {

  docker run -it   \
   --name "$DOCKERNAME" \
   --privileged \
   --net=host \
   -e TZ="Europe/Budapest" \
   --cap-add=NET_ADMIN \
   --cap-add=NET_RAW \
   -v /home/user/"$DOCKERCONFIG":/config \
   -v /etc/localtime:/etc/localtime:ro \
   -v /run/dbus:/run/dbus:ro \
   "$DOCKER_IMAGE" \
   /bin/bash

}

docker_check() {

  docker run -d   \
   --name "$DOCKERNAME" \
   --privileged \
   --net=host \
   -e TZ="Europe/Budapest" \
   --cap-add=NET_ADMIN \
   --cap-add=NET_RAW \
   -v /home/user/"$DOCKERCONFIG":/config \
   -v /etc/localtime:/etc/localtime:ro \
   -v /run/dbus:/run/dbus:ro \
   "$DOCKER_IMAGE" \
   /bin/bash -c "bash check_armv7.sh | tee -a armv7_checking.log"

}


if [ -z "$2" ]; then
    docker_bash
else
    if [ "$2" = "run" ]; then
      docker_run
    fi
    if [ "$2" = "check" ]; then
      docker_check
    fi
fi

echo
echo "dmesg:"
dmesg -T | tail -100

# watch -n 5 docker ps
# trap - SIGINT
echo "Home-assistant log:"
tail -n 10 /home/user/"$DOCKERCONFIG"/home-assistant.log
# docker start "$DOCKERNAME"
echo
echo "docker log:"
docker logs -f --tail 50 "$DOCKERNAME" | tee -a "/home/user/$DOCKERCONFIG/docker.log"

echo
echo 
echo "inspect:"
docker inspect --format='Kezdés: {{.State.StartedAt}} | Leállás: {{.State.FinishedAt}}' "$DOCKERNAME"
docker inspect --format='Exit code: {{.State.ExitCode}}' "$DOCKERNAME"

docker inspect --format='OOMKilled: {{.State.OOMKilled}} | Error: {{.State.Error}}' "$DOCKERNAME"
echo "docker stop:"
docker stop "$DOCKERNAME"
echo "docker rm:"
docker rm "$DOCKERNAME"
```
