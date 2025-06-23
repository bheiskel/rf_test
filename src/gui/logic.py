from src.modules.nrfutil_wrapper import (
    API as Nrfutil,
    TestFW,
    Core,
    ResetType,
    NrfutilLowVoltageError,
    NrfutilReadbackError,
    NrfutilError,
)
from src.modules.rf_test_dongle_api import API as Dongle
from src.modules.rf_test_dongle_api import RadioConfig, RFTestDongleError
from src.modules.rf_test_exception import RFTestException

from yaml import safe_load
from typing import List
from PySide6.QtCore import QObject, Signal, QThread, QWaitCondition, QMutex
from loguru import logger
from enum import Enum
import os, re
from dataclasses import fields
import __main__


class TestModes(Enum):
    Unmodulated_TX = 1
    Modulated_TX = 0
    Unmodulated_TX_sweep = 3
    RX = 2
    RX_sweep = 4


class DataRates(Enum):
    BLE_1_Mbit = 3
    BLE_2_Mbit = 4
    NRF_1_Mbit = 0
    NRF_2_Mbit = 1


class GUISignals(QObject):
    update_device = Signal(str)
    flash_device_result = Signal(bool)
    dongle_fw_version = Signal(str)
    connected_debuggers = Signal(list)
    recovery_completed = Signal()
    test_started_success = Signal(bool)
    error = Signal(str)
    reset_buttons = Signal()


guiSignals = GUISignals()

with open('devices.yaml', 'r') as f:
    devices = safe_load(f)


def get_hex_files(device: str) -> List[TestFW]:
    device_config = devices[device]
    out = []
    for core, hex_path in device_config['firmware'].items():
        out.append(
            TestFW(
                file_path=os.path.join(os.getcwd(), hex_path),
                core=Core.NETWORK if core == 'net' else Core.APPLICATION,
            )
        )
    return out


def get_devices() -> List[str]:
    return devices.keys()


def handle_error(err: Exception) -> None:
    if isinstance(err, NrfutilLowVoltageError):
        message = "Low voltage, check debugger connections"
    elif isinstance(err, NrfutilReadbackError):
        message = "Device is readback protected, please recover it"
    elif isinstance(err, NrfutilError):
        message = "No connection to the device"
    else:
        raise err
    guiSignals.reset_buttons.emit()
    guiSignals.error.emit(message)


def detect_device(snr: str) -> None | str:
    if snr == '':
        return None
    try:
        device_version = Nrfutil(snr=int(snr)).get_device_version().split('_')[0]
    except (NrfutilError, NrfutilLowVoltageError, NrfutilReadbackError) as err:
        handle_error(err)
        device_version = ""
    guiSignals.update_device.emit(device_version)
    return device_version


def fem_config_to_ints(fem_config: dict) -> None | dict:
    for key, item in fem_config.items():
        if item == '':
            fem_config[key] = 0xFF
        else:
            if port_pin := re.search(r'(?<=P)\d+\.\d+', item):
                port_pin = port_pin.group().split('.')
                port = int(port_pin[0])
                pin = int(port_pin[1])
                fem_config[key] = pin + port * 32
            elif item.isdigit():
                fem_config[key] = int(item)
            else:
                logger.error(f'{key} is not a pin number')
                return None
    return fem_config


class GetDebuggersTask(QThread):
    def run(self):
        logger.debug("Getting connected debuggers")
        try:
            debuggers = [str(snr) for snr in Nrfutil().get_debuggers()]
        except TypeError:
            debuggers = None
        guiSignals.connected_debuggers.emit(debuggers)


class DongleFWVersionTask(QThread):
    def run(self):
        try:
            with Dongle() as dongle:
                version = dongle.get_dongle_version()
            if version != __main__.REQ_DONGLE_VERSION:
                guiSignals.error.emit("Incorrect dongle version found")
        except RFTestDongleError as err:
            logger.error(err)
            version = None
        guiSignals.dongle_fw_version.emit(version)


class FlashFWTask(QThread):
    def __init__(self, snr: str, load_cap: str, fem_config: dict | None = None, parent=None):
        super().__init__(parent)
        if snr == '':
            self.snr = None
        else:
            self.snr = int(snr)
        self.load_cap = load_cap
        self.fem_config = fem_config

        guiSignals.connected_debuggers.connect(self.stop_waiting)

        self.waitcondition = QWaitCondition()
        self.waitMutex = QMutex()

    def stop_waiting(self, debuggers):
        logger.debug("Done waiting")
        self.waitcondition.wakeAll()
        if len(debuggers) > 0:
            self.snr = int(debuggers[0])
        guiSignals.connected_debuggers.disconnect(self.stop_waiting)

    def wait_for_snr(self):
        logger.debug('Waiting for detecting debuggers')
        self.waitMutex.lock()
        self.waitcondition.wait(self.waitMutex)
        self.waitMutex.unlock()

    def run(self):
        try:
            if not self.snr:
                GetDebuggersTask().run()
                self.wait_for_snr()
                logger.debug("continuing")
                if not self.snr:
                    guiSignals.flash_device_result.emit(False)

            debugger = Nrfutil(self.snr)

            if self.fem_config:
                self.fem_config = fem_config_to_ints(self.fem_config)
            device = detect_device(self.snr)
            testfw = get_hex_files(device)
            try:
                debugger.program(testfw)
                success = True
            except RFTestException as err:
                logger.error(err)
                success = False

            if self.fem_config:
                logger.debug('Writing FEM config to device')
                fem_config_reg0 = (
                    self.fem_config.get('pinPDN')
                    | self.fem_config.get('pinTXEN') << 8
                    | self.fem_config.get('pinRXEN') << 16
                    | self.fem_config.get('pinMODE') << 24
                )

                fem_config_reg1 = self.fem_config.get('pinANTSEL') | 0xFFFFFF << 8

                fem_config_reg0_addr = devices.get(device).get('fem').get('fem_config_reg0')
                fem_config_reg1_addr = devices.get(device).get('fem').get('fem_config_reg1')
                coprocessor = devices.get(device).get('fem').get('coprocessor', 'APPLICATION')
                logger.debug(f"test: {getattr(Core, coprocessor).value}")
                debugger.write(fem_config_reg0_addr, fem_config_reg0, getattr(Core, coprocessor))
                debugger.write(fem_config_reg1_addr, fem_config_reg1, getattr(Core, coprocessor))

            if self.load_cap != '':
                if load_cap_config := devices.get(device).get('load_cap'):
                    logger.debug(f"Configuring internal load caps to: {self.load_cap}")
                    logger.debug(f"UICR load cap config addr: {hex(load_cap_config.get('config_register'))}")
                    logger.debug(f"Load cap multiply factor: {load_cap_config.get('multiply_factor')}")
                    try:
                        debugger.write(
                            load_cap_config.get('config_register'),
                            int(float(self.load_cap) * load_cap_config.get('multiply_factor', 1)),
                            getattr(Core, load_cap_config.get('coprocessor')),
                        )
                    except ValueError:
                        logger.error(f'Load cap value is not float')
                    debugger.reset()
                else:
                    logger.error('No load capacitor config in device config')

            guiSignals.flash_device_result.emit(success)
        except (NrfutilError, NrfutilLowVoltageError, NrfutilReadbackError) as err:
            guiSignals.flash_device_result.emit(False)
            handle_error(err)


class RecoverTask(QThread):
    def __init__(self, snr: str, parent=None):
        super().__init__(parent)
        self.snr = int(snr)

    def run(self):
        try:
            Nrfutil(snr=self.snr).recover()
            guiSignals.recovery_completed.emit()
        except (NrfutilError, NrfutilLowVoltageError, NrfutilReadbackError) as err:
            guiSignals.recovery_completed.emit()
            handle_error(err)


class StartTestTask(QThread):
    def __init__(self, radio_config: RadioConfig, parent=None):
        super().__init__(parent)
        self.radio_config = radio_config

    def run(self):

        for field in fields(self.radio_config):
            match field.name:
                case 'data_rate':
                    setattr(
                        self.radio_config,
                        field.name,
                        DataRates[getattr(self.radio_config, field.name).replace(' ', '_')].value,
                    )
                case 'rf_cmd':
                    setattr(
                        self.radio_config,
                        field.name,
                        TestModes[getattr(self.radio_config, field.name).replace(' ', '_')].value,
                    )
                case _:
                    try:
                        setattr(self.radio_config, field.name, int(getattr(self.radio_config, field.name)))
                    except ValueError:
                        logger.error(f'Radio config {key} is not int')
                        raise RFTestException(f'Radio config {key} is not int')
        setattr(self.radio_config, 'usb_cmd', 0x0B)
        logger.debug(f'Starting RF test with test_config:{self.radio_config}')
        with Dongle() as dongle:
            dongle.set_config(self.radio_config)
            success = dongle.send_cmd()
        guiSignals.test_started_success.emit(success)


def get_test_modes() -> List[str]:
    return [mode.name.replace('_', ' ') for mode in TestModes]


def get_data_rates() -> List[str]:
    return [rate.name.replace('_', ' ') for rate in DataRates]


def reset(snr: str):
    Nrfutil(int(snr)).reset(ResetType.PIN)
