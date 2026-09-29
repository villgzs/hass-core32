python3 /config/check_hass_packages.py --list

python3 /config/check_hass_packages.py \
    --core \
    --frontend \
    --timeout 60 \
    --json /config/hass_package_results.json

