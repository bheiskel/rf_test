# from src.modules.rf_test_exception import RFTestException
import subprocess
import json
from typing import List
from dataclasses import dataclass
from loguru import logger
from src.modules.rf_test_exception import RFTestException
from enum import Enum


class ResetType(Enum):
    DEBUG = 'RESET_DEBUG'
    PIN = 'RESET_PIN'
    SYSTEM = 'RESET_SYSTEM'
    HARD = 'RESET_HARD'
    SOFT = 'RESET_SOFT'


class EraseType(Enum):
    ALL = 'all'
    UICR = 'uicr'


class Core(Enum):
    APPLICATION = 'Application'
    NETWORK = 'Network'
    MODEM = 'Modem'
    SECURE = 'Secure'


class Protection(Enum):
    NONE = 'None'
    ALL = 'All'
    SECURE = 'SecureRegion'
    REGION0 = 'Region0'
    REGION01 = 'Region0Region1'


@dataclass
class TestFW:
    file_path: str
    core: Core


@dataclass
class DeviceInfo:
    family: str
    version: str
    protection: str


class NrfutilLowVoltageError(Exception):
    pass


class NrfutilReadbackError(Exception):
    pass


class NrfutilError(Exception):
    def __init__(self, *args):
        if args:
            self.message = f'{" - ".join(map(str,args))}'
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'NrfutilError, {}'.format(self.message)
        else:
            return 'NrfutilError occurred'


def handle_nrfutil_return(completed) -> dict | None:
    if completed.stderr:
        error = completed.stderr.decode('utf-8')
        logger.error(error)
        if "LOW_VOLTAGE" in error:
            raise NrfutilLowVoltageError
        else:
            raise NrfutilError(error)
    if completed.stdout != b'':
        return json.loads(completed.stdout).get('devices')
    else:
        return None


class API:
    def __init__(self, snr: int | None = None):
        self.snr = snr

    def get_debuggers(self):
        completed = subprocess.run(
            ['nrfutil', 'device', 'list', '--json', '--traits', 'jlink', '--skip-overhead'], capture_output=True
        )
        try:
            devices = handle_nrfutil_return(completed)
            return [int(snr.get('serialNumber')) for snr in devices]
        except RFTestException:
            return None

    def get_snr(self):
        devices = self.get_debuggers()
        match len(devices):
            case 0:
                logger.error('No debuggers connected')
                raise RFTestException('No debuggers connected')
            case 1:
                self.snr = devices[0]
            case _:
                logger.error('Too many debuggers connected to auto detect SNR')
                raise RFTestException('Too many debuggers connected to auto detect SNR')

    def __nrfutil(self, options: List[str], core: Core = None) -> dict:
        if not self.snr:
            self.get_snr()
        command = ['nrfutil', 'device']
        command += options
        command += ['--serial-number', str(self.snr)]
        command += ['--core', core.value] if core else ''
        command += ['--json']
        command += ['--traits', 'jlink']
        command += ['--skip-overhead']
        completed = subprocess.run(command, capture_output=True)
        if data := handle_nrfutil_return(completed):
            for device in data:
                if int(device.get('serialNumber')) == self.snr:
                    return device
            return json.loads(completed.stdout.split(b'\n')[1])
        else:
            return None

    def recover(self, core: Core = Core.APPLICATION):
        logger.debug(f'{self.snr}: Recovering device')
        self.__nrfutil(['recover'], core=core)

    def program(self, hex_files: List[TestFW]):
        for file in hex_files:
            logger.debug(f'{self.snr}: Programming file: {file.file_path} Core: {file.core}')
            command = [
                'program',
                '--options',
                'chip_erase_mode=ERASE_RANGES_TOUCHED_BY_FIRMWARE,verify=VERIFY_READ,reset=RESET_DEBUG',
                '--firmware',
                file.file_path,
            ]
            self.__nrfutil(command, core=file.core)

    def get_protection(self, core: Core = Core.APPLICATION) -> Protection:
        ret = self.__nrfutil(['protection-get'])
        return Protection(ret.get('protectionStatus'))

    def verify(self, hexfile: TestFW):
        self.__nrfutil(['fw-verify', '--firmware', hexfile.file_path], core=hexfile.core)

    def erase(self, type: EraseType = EraseType.ALL, core: Core = Core.APPLICATION):
        logger.debug(f'{self.snr}: Erasing {type.name} in {core.name} core')
        self.__nrfutil(['erase', f'--{type.value}'], core=core)

    def get_device_version(self) -> str:
        ret = self.__nrfutil(['device-info']).get('deviceInfo', {}).get('jlink', {})
        if ret.get('protectionStatus') != 'NRFDL_PROTECTION_STATUS_NONE':
            raise NrfutilReadbackError
        self.device = ret.get('deviceVersion', {})
        logger.debug(f'{self.snr}: Getting device version: {self.device}')
        return self.device

    def get_device_info(self) -> DeviceInfo:
        ret = self.__nrfutil(['device-info'])
        device_version = ret.get('deviceInfo', {}).get('jlink').get('deviceVersion')
        device_family = ret.get('deviceInfo', {}).get('jlink').get('deviceFamily')
        protection_status = ret.get('deviceInfo', {}).get('jlink').get('protectionStatus')

        device_info = DeviceInfo(family=device_family, version=device_version, protection=protection_status)
        logger.debug(f'{self.snr}: Getting device info: {device_info}')
        return device_info

    def reset(self, type: ResetType = ResetType.DEBUG, core: Core = Core.APPLICATION):
        logger.debug(f'{self.snr}: Performing {type.name} reset')
        self.__nrfutil(['reset', '--reset-kind', type.value])

    def write(self, addr: int, data: int, core: Core = Core.APPLICATION):
        logger.debug(f'{self.snr}: Writing {hex(data)} to addr: {hex(addr)}')
        ret = self.__nrfutil(['x-write', '--address', hex(addr), '--value', hex(data)], core)

    def read(self, addr: int, core: Core = Core.APPLICATION) -> int:
        ret = self.__nrfutil(['x-read', '--address', hex(addr), '--direct'], core)
        val = ret.get('memoryData', [])[0].get('values')
        val = int.from_bytes(bytes(val), 'little')
        logger.debug(f'{self.snr}: Reading addr: {hex(addr)}, val: {hex(val)}')
        return val
