from argparse import ArgumentParser
from loguru import logger
from src.gui.gui import GUI
from src.modules.automatic_rf_test import AutoTest
import sys

REQ_DONGLE_VERSION = '1.0.0'

VERSION = '1.1.0'

DEFAULT_VOLTAGE = 3.0
DEFAULT_CURRENT = 0.1
DEFAULT_CHANNEL = 1

parser = ArgumentParser(prog="RF test", description="RF test")

parser.add_argument('-v', '--version', help='Print version number', action='store_true')
parser.add_argument('-V', '--verbose', help='Enable verbose logging', action='store_true')

auto_test_mode_args = parser.add_argument_group('Automatic RF test mode')
auto_test_mode_args.add_argument('-a', '--auto', help='Automatic test mode for RF tuning', action='store_true')
auto_test_mode_args.add_argument(
    '--frequencies', default=[2, 40, 80], help='Test frequencies for automatic test mode'
),
auto_test_mode_args.add_argument('--tx_powers', default=[8, 4, 0], help='Test TX powers for automatic test mode')
auto_test_mode_args.add_argument('--spectrum_ip', help='Spectrum analyzer ip for automatic test mode')
auto_test_mode_args.add_argument('--power_supply_ip', help='Power supply ip for automatic test mode')
auto_test_mode_args.add_argument('--img_path', default='', help='Path for output images')
auto_test_mode_args.add_argument('--img_prefix', default='', help='Prefix for output images')
auto_test_mode_args.add_argument('--ref_offset', default=0.7, help='Reference level offset for automatic test mode')


args = parser.parse_args()

if args.verbose:
    log_level = 'DEBUG'
else:
    log_level = 'INFO'
logger.configure(handlers=[{'sink': sys.stdout, 'level': log_level}])

if args.version:
    print(f'rf_test: {VERSION}')
    try:
        with RFTestDongleAPI() as dongle_api:
            dongle_fw_version = dongle_api.get_dongle_version()
            print(f'dongle_fw: {dongle_fw_version}')
    except:
        pass
    exit()

if args.auto:
    if not args.spectrum_ip:
        print('Spectrum IP required for automatic testing')
        exit()
    if not args.power_supply_ip:
        print('Power supply IP required for automatic testing')
        exit()
    logger.info("Starting automated RF test")
    auto_test = AutoTest(args.ref_offset, args.img_path, args.img_prefix)
    logger.info("Initializing power supply")
    auto_test.init_power_supply(args.power_supply_ip, DEFAULT_VOLTAGE, DEFAULT_CURRENT, DEFAULT_CHANNEL)
    logger.info("Initializing spectrum analyzer")
    auto_test.init_spectrum(args.spectrum_ip, args.ref_offset)
    logger.info("Measuring frequency offset")
    auto_test.measure_freq_offset()
    logger.info("Measuring output power and harmonics")
    auto_test.rf_tuning_measurements(args.frequencies, args.tx_powers)
    exit()

logger.debug('Starting GUI')
gui = GUI()
gui.run()
exit()
