#!/bin/bash
# docker run -d   --name hass-core   --privileged   --restart=unless-stopped   --net=host   -e TZ="Europe/Budapest"   -v /home/hass/homeassistant-udocker/config:/config   dockergzs/hass-core:python3.14-alpine3.24-2026.7.2-armv7
# docker start hass-core
# docker run -d   --name homeassistant   --privileged   --restart=unless-stopped   --net=host   -e TZ="Europe/Budapest"   -v /home/hass/homeassistant-udocker/config:/config   ghcr.io/adyoull/ha-armv7:2026.7.2


if [ -z "$1" ]; then
    echo "TAG legyen megadva! Pl.: 2026.9.3"
    exit 1
fi
IMAGE_TAG="$1"

DOCKERNAME=$(basename "$0")
DOCKERNAME="${DOCKERNAME%.*}"
echo "$DOCKERNAME"

DOCKER_IMAGE="dockergzs/homeassistant-arm32:2026.7.2"
DOCKER_IMAGE="ghcr.io/villgzs/hass-core32:$IMAGE_TAG"
echo "DOCKER_IMAGE: $DOCKER_IMAGE"


docker pull "$DOCKER_IMAGE"

docker_run() {

  docker run -d   \
   --name "$DOCKERNAME" \
   --privileged \
   --net=host \
   -e TZ="Europe/Budapest" \
   --cap-add=NET_ADMIN \
   --cap-add=NET_RAW \
   -v /home/user/"$DOCKERNAME"/config:/config \
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
   -v /home/user/"$DOCKERNAME"/config:/config \
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
   -v /home/user/"$DOCKERNAME"/config:/config \
   -v /etc/localtime:/etc/localtime:ro \
   -v /run/dbus:/run/dbus:ro \
   "$DOCKER_IMAGE" \
   /bin/bash -c "bash check_armv7.sh | tee armv7_checking.log"

}


docker_check

# watch -n 5 docker ps
# trap - SIGINT
echo "Home-assistant log:"
tail -n 10 /home/user/"$DOCKERNAME"/config/home-assistant.log
# docker start "$DOCKERNAME"
echo
echo "docker log:"
docker logs -f --tail 50 docker_start_hass

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
