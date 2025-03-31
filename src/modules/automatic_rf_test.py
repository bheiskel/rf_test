from src.modules.rf_test_dongle_api import API as dongleAPI
from src.modules.pwr_supply import API as pwrAPI
from src.modules.rns_spectrum import API as rnsAPI
import time

DEFAULT_VOLT = 3.0
DEFAULT_CURR_A = 0.1
DEFAULT_CHANNEL = 1

SPECTRUM_CONFIG_PATH = r'C:\R_S\Instr\user\automated_rf_test.dfl'

TIMEOUT_RADIO_START_S = 5
TIMEOUT_FREQ_STABILIZE_S = 5


class TestTimeoutError(Exception):
    def __init__(self, *args):
        if args:
            self.message = f'{" - ".join(map(str, args))}'
        else:
            self.message = "Test timedout"

    def __str__(self):
        return self.message


class AutoTestError(Exception):
    def __init__(self, *args):
        if args:
            self.message = f'{" - ".join(map(str, args))}'
        else:
            self.message = "Automatic test timed out"

    def __str__(self):
        return self.message


class AutoTest:
    def __init__(self, ref_offset=0, img_path='', img_prefix=''):
        self.dongle = dongleAPI()
        self.freq_offset = 0
        self.ref_offset = ref_offset
        self.img_path = img_path
        self.img_prefix = img_prefix
        self.pwr = None
        self.specturm = None

    def init_power_supply(self, address: str, voltage: float, current: float, channel: int):
        self.pwr = pwrAPI(address, voltage, current, channel)

    def init_spectrum(self, spectrumIP, ref_level_offset):
        self.spectrum = rnsAPI(spectrumIP)
        self.spectrum.load_config(SPECTRUM_CONFIG_PATH)
        self.spectrum.change_ref_level_offset(ref_level_offset)

    def start_radio(self):
        start_time = time.time()
        while not self.dongle.send_cmd():
            if time.time - start_time > TIMEOUT_RADIO_START_S:
                raise TestTimeoutError("Timed out starting radio TX")
            self.pwr.reset()
            time.sleep(0.2)

    def measure_freq_offset(self, save_screenshot=True):
        self.spectrum.change_spectrum(2)
        self.spectrum.change_frequency(2440)
        self.spectrum.change_ref_level_offset(self.ref_offset)

        self.dongle.set_channel(40)
        self.dongle.set_tx_power(0)
        self.dongle.set_mode(1)
        self.start_radio()

        start_time = time.time()
        while abs(self.spectrum.read_delta() - self.freq_offset) != 0:
            self.freq_offset = self.spectrum.read_delta()
            if time.time() - start_time > TIMEOUT_FREQ_STABILIZE_S:
                raise TestTimeoutError("Timed out waiting for frequency offset to stabilize")
            time.sleep(1)

        self.spectrum.screenshot(
            f'{self.img_path}/{self.img_prefix}{"_" if self.img_prefix else ""}crystal_accuracy.png'
        )

    def measure_radio_output(self, channel: int, tx_pwr: int, init=False):
        if init:
            self.spectrum.change_spectrum(1)
            self.set_ref_level_offset(self.ref_offset)

        self.spectrum.change_frequency(2400 + channel + self.freq_offset / 1e6)
        self.dongle.set_channel(channel)
        self.dongle.set_tx_power(tx_pwr)
        self.start_radio()
        self.spectrum.screenshot(
            f'{self.img_path}/{self.img_prefix}{"_" if self.img_prefix else ""}{2400+channel}_{pwr}dBm.png'
        )

    def rf_tuning_measurements(self, channels, tx_powers):
        self.spectrum.change_spectrum(1)
        self.change_ref_level_offset(self.ref_offset)
        for channel in channels:
            for pwr in tx_powers:
                self.measure_radio_output(channel, pwr)

    def run(self):
        self.pwr.reset()
        self.measure_freq_offset()
        self.measure_radio_output()
