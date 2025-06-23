#!/bin/bash

declare -A DEVICES
DEVICES[nrf54l15]="nrf54l15dk/nrf54l15/cpuapp"
DEVICES[nrf54l10]="nrf54l15dk/nrf54l10/cpuapp"
DEVICES[nrf54l05]="nrf54l15dk/nrf54l05/cpuapp"
DEVICES[nrf5340]="nrf5340dk/nrf5340/cpunet"
DEVICES[nrf52840]="nrf52840dk/nrf52840"
DEVICES[nrf52833]="nrf52833dk/nrf52833"
DEVICES[nrf52820]="nrf52833dk/nrf52820"
DEVICES[nrf52811]="nrf52840dk/nrf52811"
DEVICES[nrf52832]="nrf52dk/nrf52832"
DEVICES[nrf52810]="nrf52dk/nrf52810"
DEVICES[nrf52805]="nrf52dk/nrf52805"

mkdir -p ../hex
for device in "${!DEVICES[@]}"
do
  echo "Building for $device"
  west build -b "${DEVICES[$device]}" -d "builds/$device" --sysbuild
  if [ $device = "nrf5340" ]
  then
    cp "builds/$device/rf_test_app_core/zephyr/zephyr.hex" ../hex/empty_app_core.hex
  fi
  cp "builds/$device/dut_firmware/zephyr/zephyr.hex" ../hex/$device.hex
done
