#!/bin/bash

declare -A DEVICES
DEVICES[nrf52833_dk]="nrf52833dk/nrf52833"
DEVICES[nrf52840_dk]="nrf52840dk/nrf52840"
DEVICES[nrf52840_dongle]="nrf52840dongle/nrf52840"

for device in "${!DEVICES[@]}"
do
  echo "Building for $device"
  west build -b "${DEVICES[$device]}" -d "builds/$device"
  cp "builds/$device/dongle_firmware/zephyr/zephyr.hex" "rf_test_dongle_$device.hex"
done
