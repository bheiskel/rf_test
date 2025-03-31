import pyvisa
from loguru import logger


class SperectumError(Exception):
    def __init__(self, *args):
        if args:
            self.message = f'{" - ".join(map(str, args))}'
        else:
            self.message = "SpectrumError occured"

    def __str__(self):
        return self.message


class API:
    def __init__(self, IP: str):
        self.inst = pyvisa.ResourceManager().open_resource(f'TCPIP::{IP}::INSTR')
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'
        self.inst.timeout = 500000
        self.__write('HCOP:DEV:COL ON')
        self.__write('HCOP:DEV:LANG PNG')
        self.__write("HCOP:DEST 'MMEM'")
        self.filePathInstr = r"c:\temp\hcopy_dev.png"

        # file path on instrument
        self.__write(f'MMEM:NAME "{self.filePathInstr}"')

    def __write(self, cmd):
        logger.debug(f"Writing to spectrum analyzer: {cmd}")
        self.inst.write(cmd)
        err, err_msg = self.inst.query('SYST:ERR?').split(',')

        if int(err) != 0:
            logger.error(f'Command "{cmd}" failed with error: {err_msg}')
            raise SpectrumError(f'Command "{cmd}" failed with error: {err_msg}')

    def __write_read(self, cmd):
        logger.debug(f"Writing to spectrum analyzer: {cmd}")
        self.inst.write(cmd)
        logger.debug("Reading responce")
        out = self.inst.read()
        err, err_msg = self.inst.query('SYST:ERR?').split(',')

        if int(err) != 0:
            logger.error(f'Command "{cmd}" failed with error: {err_msg}')
            raise SpectrumError(f'Command "{cmd}" failed with error: {err_msg}')
        else:
            return out

    def set_frequency(self, freq: int):
        self.__write(f'FREQ:CENT {freq} MHz;*WAI')

    def set_span_kHz(self, span: int):
        self.__write(f'FREQ:SPAN {span} kHz;*WAI')

    def set_ref_level_offset(self, offset: float):
        self.__write(f'DISP:TRAC:Y:RLEV:OFFS {offset}dB')

    def remove_marker(self, marker):
        self.__write(f'CALC:MARK{marker} OFF;*WAI')

    def screenshot(self, filename):
        self.__write('HCOP:IMM;*WAI')
        try:
            fileData = bytes(self.inst.query_binary_values(f'MMEM:DATA? "{self.filePathInstr}";*WAI', datatype='s'))
        except:
            err, err_msg = self.inst.query('SYST:ERR?').split(',')
            if int(err) != 0:
                logger.error(f'Failed taking screenshot with error: {err_msg}')
                raise SpectrumError(f'Failed taking screenshot with error: {err_msg}')

        logger.debug(f"Saving screenshot: {filename}")
        with open(filename, "wb") as f:
            f.write(fileData)

    def set_spectrum(self, spectrum: int):
        if spectrum == 1:
            self.__write("INST:SEL SAN")
        else:
            self.__write(f"INST:SEL 'Spectrum {spectrum}'")

    def read_delta(self):
        self.__write('CALC:DELT1:MAX;*WAI')
        out = self.__write_read('CALC:DELT1:X:REL?;*WAI')
        return float(out)

    def read_max(self, marker: int = 1):
        self.__write(f'CALC:MARK{marker}:MAX;*WAI')
        out = self.__write_read(f'CALC:MARK{marker}:Y?;*WAI')
        return float(out)

    def load_config(self, config_path: str):
        self.__write(f"MMEM:LOAD:STAT 1,'{config_path}';*WAI")

    def set_ref_level(self, lvl: int):
        self.__write(f'DISP:TRAC:Y:RLEV {lvl}')
