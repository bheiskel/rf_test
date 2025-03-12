from argparse import ArgumentParser
from loguru import logger
from src.gui.gui import GUI
import sys, yaml

VERSION = '1.0.0'

parser = ArgumentParser(prog="RF test", description="RF test")

parser.add_argument('-v', '--version', help='Print version number', action='store_true')
parser.add_argument('-V', '--verbose', help='Enable verbose logging', action='store_true')

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

logger.debug('Starting GUI')
gui = GUI()
gui.run()
exit()
