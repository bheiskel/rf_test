import usb
from loguru import logger
from src.modules.rf_test_exception import RFTestException
import time
from dataclasses import dataclass


@dataclass
class RadioConfig:
    first_channel: int
    last_channel: int
    radio_power: int
    data_rate: int
    rf_cmd: int
    fem_config: int
    usb_cmd: int

    def __setitem__(self, key, value):
        setattr(self, key, value)


VENDOR_ID = 0x1915
PRODUCT_ID = 0x0103


class RFTestDongleError(Exception):
    def __init__(self, *args):
        if args:
            self.message = f'{" - ".join(map(str,args))}'
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'RFTestDongleError, {}'.format(self.message)
        else:
            return 'RFTestDongleError occurred'


class API:
    def __init__(self):
        self.radio_config = RadioConfig(
            first_channel=0x00,
            last_channel=0x00,
            radio_power=0x00,
            data_rate=0x00,
            fem_config=0x00,
            rf_cmd=0x01,
            usb_cmd=0x0B,
        )

        self.dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        if not self.dev:
            raise RFTestDongleError("USB dongle not found")
        self.dev.set_configuration()
        cfg = self.dev.get_active_configuration()
        intf = cfg[(0, 0)]
        self.dongle_endpoint_out = usb.util.find_descriptor(
            intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )
        in_endpoints = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN,
            find_all=True,
        )
        for a in in_endpoints:
            if a.bEndpointAddress == 0x82:
                self.dongle_endpoint_in = a
        assert self.dongle_endpoint_out is not None

    def __enter__(self):
        return self

    def __exit__(self, execption_type, exception_value, exception_traceback):
        self.close()

    def set_config(self, config: RadioConfig):
        self.radio_config = config

        if self.radio_config.radio_power < 0:
            self.radio_config.radio_power = self.radio_config.radio_power + 2**8

    def set_channel(self, first_channel: int, last_channel: int = 80):
        logger.debug(f'Setting tx channel: {first_channel} {last_channel}')
        self.radio_config['first_channel'] = first_channel
        self.radio_config['last_channel'] = last_channel

    def set_tx_power(self, tx_power: int):
        logger.debug(f'Setting tx power: {tx_power}')
        if tx_power < 0:
            self.radio_config['radio_power'] = tx_power + 2**8
        else:
            self.radio_config['radio_power'] = tx_power

    def set_mode(self, mode: int):
        logger.debug(f'Setting mode: {mode}')
        self.radio_config['rf_cmd'] = mode

    def set_data_rate(self, rate: int):
        logger.debug(f'Setting data rate: {rate}')
        self.radio_config['data_rate'] = rate

    def send_cmd(self) -> bool:
        command = [
            getattr(self.radio_config, 'first_channel'),
            getattr(self.radio_config, 'last_channel'),
            getattr(self.radio_config, 'radio_power'),
            getattr(self.radio_config, 'data_rate'),
            getattr(self.radio_config, 'fem_config'),
            getattr(self.radio_config, 'rf_cmd'),
            getattr(self.radio_config, 'usb_cmd'),
        ]
        logger.debug(f'Sending command: {command}')
        self.dongle_endpoint_out.write(command)
        time.sleep(0.5)
        self.dongle_endpoint_out.write([0, 0, 0, 0, 0, 0, 12])
        return bool(self.dongle_endpoint_in.read(1)[0])

    def get_dongle_version(self):
        command = [0, 0, 0, 0, 0, 0, 1]
        logger.debug(f'Sending command: {command}')
        self.dongle_endpoint_out.write(command)
        ret = self.dongle_endpoint_in.read(4)
        version = f'{ret[1]}.{ret[2]}.{ret[3]}'
        return version

    def close(self):
        if self.dev:
            usb.util.dispose_resources(self.dev)

    def __del__(self):
        self.close()
