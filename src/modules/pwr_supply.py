import pyvisa, time
from loguru import logger


class API:
    def __init__(self, ADDR, VOLT, CURR, CHANNEL=1):
        logger.debug(
            f'Initializing power supply:\n\r\t Address: {ADDR}\n\r\t Voltage: {VOLT} \n\r\t Current limit: {CURR}\n\r\t Channel: {CHANNEL}'
        )
        self.address = ADDR
        self.voltage = VOLT
        self.current = CURR
        self.channel = CHANNEL
        self.inst = pyvisa.ResourceManager().open_resource(f'TCPIP::{self.address}::INSTR')

        self.__config_supply()

    def __config_supply(self):
        self.inst.write(f':APPL CH{self.channel},{self.voltage},{self.current}')

    def change_config(self, VOLT, CURR):
        logger.debug(f'Changing config, Voltage: {VOLT}, Current{CURR}')
        self.voltage = VOLT
        self.current = CURR
        self.__config_supply()

    def on(self):
        logger.debug(f'Turning ON channel {self.channel}')
        self.inst.write(f':OUTP 1,(@{self.channel})')

    def off(self):
        logger.debug(f'Turning OFF channel {self.channel}')
        self.inst.write(f':OUTP 0,(@{self.channel})')

    def reset(self):
        self.off()
        time.sleep(0.5)
        self.on()
