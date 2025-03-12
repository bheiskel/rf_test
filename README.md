# RF Test application for Nordic Semiconductor nRF5x series SoC.

RF test application for Nordic Semiconductor nRF5x series of SoC.

## Requirements
### Python
Python 3.12 or newer is required.

#### External packages
- PyYAML
- loguru
- pyusb
- PySide6

Install requirements using:
~~~
python -m pip install -r requirements.txt
~~~

### nRFutil
[https://www.nordicsemi.com/Products/Development-tools/nRF-Util/Download#infotabs](https://www.nordicsemi.com/Products/Development-tools/nRF-Util/Download#infotabs)
Place executable in PATH or in project folder.

nrfutil-device is also required, to install it run:
~~~
nrfutil install device
~~~

### Dongle
The application uses Enhanced ShockBurst to communicate with the DUT, a development kit or dongle with rf_test_dongle firmware is needed. Only nRF52840DK and dongle have been tested.

On Windows the WinUSB driver is needed for the dongle. Use Zadig to install the driver:
[https://zadig.akeo.ie/](https://zadig.akeo.ie/)

## Usage

### Test Modes
#### Unmodulated TX
The radio transmits a unmodulated carrier at the configured frequency with the configured power.

#### Modulated TX
The radio transmits a modulated carrier at the configured frequency with the configured power and data rate.

#### Unmodulated TX Sweep
The radio aweeps a unmodulated carrier between the start and stop frequency with the configured power.

#### RX
The radio is set in RX at the configured frequency.
Note, this can not be used for actually receiving packages. This test mode is used for measuring spurious emission from the radio in RX mode.

#### RX Sweep
The radio sweeps between the start and stop frequency in RX mode.

### Front End Module
The nRF21540 in GPIO only mode is supported. Any other simple GPIO controlled FEM can also work, but the pin naming will be different.

#### Pin states
|| TX_EN | RX_EN | PDN | MODE | ANT_SEL |
| - | - | - | - | - | - |
| TX | 1 | 0 | 1 | x | x |
| RX | 0 | 1 | 1 | x | x |

MODE and ANT_SEL can be configured high or low dynamically in the FEM config.

### HFXO load capacitor configuration
On devices with internal HFXO load capacitors, these can be configured when flashing the test firmware.
If external load capacitors are used this option should be set to 0 to disable the internal ones.
If the option is left blank the default load capacitance is used.

