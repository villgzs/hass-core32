Dockerfile: 
  removed: --index-strategy unsafe-best-match \
```
    RUN \
    echo "First RUN is started..." \
    ls -las /init \
    && echo "cython<3.2.7" > /etc/pip-build-constraints.txt \
    # Verify go2rtc can be executed
    && go2rtc --version \
    && apk add --no-cache libffi libjpeg-turbo zlib freetype \
    && apk add --no-cache --virtual .build-deps \
        cmake make ninja meson gcc g++ musl-dev \
        rust cargo linux-headers \
        libffi-dev jpeg-dev zlib-dev freetype-dev \
        ffmpeg-dev \
    # Install uv at the version pinned in the requirements file
    && pip3 install --no-cache-dir "uv==$(awk -F'==' '/^uv==/{print $2}' homeassistant/requirements.txt)" \
    && uv pip install \
        --index-strategy unsafe-best-match \
        -r homeassistant/requirements.txt \
    && apk del --no-cache .build-deps
```

```
RUN \
    echo "Second RUN is started..." \
    && apk add --no-cache --virtual .build-deps autoconf cmake make ninja gcc g++ \
        musl-dev rust cargo linux-headers libffi-dev jpeg-dev zlib-dev freetype-dev ffmpeg-dev\
        pkgconf gfortran openblas-dev libxml2-dev libxslt-dev mariadb-dev postgresql-dev glib-dev\
        openssl-dev mariadb-connector-c-dev \
    && apk add --no-cache ffmpeg-libs libavc1394 openblas libgfortran libxml2 libxslt mariadb-connector-c postgresql-libs \
    && if ls homeassistant/home_assistant_*.whl 1> /dev/null 2>&1; then \
        uv pip install homeassistant/home_assistant_*.whl; \
    fi \
    && uv pip install \
        -r homeassistant/requirements_all.txt \
        --index-strategy unsafe-best-match \
    && apk del --no-cache .build-deps
```

```
RUN \
    echo "Third... Setup Home Assistant Core" \
    && uv pip install \
        --index-strategy unsafe-best-match \
        -e ./homeassistant \
    && python3 -m compileall \
        homeassistant/homeassistant
```
