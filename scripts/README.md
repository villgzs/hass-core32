Docker wheels builder start locally:
```
docker run --rm -it --platform linux/arm/v7 --entrypoint /bin/bash ghcr.io/villgzs/wheels32bit/armv7/musllinux_1_2/cp314
```

```
bash docker_start_hass.sh ghcr.io/villgzs/hass-core32:2026.9.4 run
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
