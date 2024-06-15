import time
import enum
from crccheck.crc import Crc32Mpeg2 as CRC32
from ctypes import *
import struct
import serial
import requests
import tempfile
from stm32loader.main import main as stm32loader_main


Index = enum.IntEnum('Index', [
    'HeaderL',
    'HeaderH',
    'PackageSize',
    'Command',
    'SoftwareVersion',
    'HardwareVersion',
    'ErrorCount',
    'RollAngle',
    'PitchAngle',
    'HeadAngle',
    'DepthPosition',
    'Temperature',
    'AccelerationX',
    'AccelerationY',
    'AccelerationZ',
    'HeadAngleControl',
    'HeadPIDP',
    'HeadPIDI',
    'HeadPIDD',
    'PitchPIDP',
    'PitchPIDI',
    'PitchPIDD',
    'RollPIDP',
    'RollPIDI',
    'RollPIDD',
    'DepthPIDP',
    'DepthPIDI',
    'DepthPIDD',
    'ControlDataX',
    'ControlDataY',
    'ControlDataZ',
    'ControlDataH',
    'ControlDataR',
    'ControlDataP',
    'ControlDataUpperArm',
    'ControlDataLowerArm',
    'ControlDataWrist',
    'ControlDataGrip',
    'ControlDataHome'
    'Baudrate',
    'CRC',
    ], start = 0
)


class Commands(enum.IntEnum):             
    PING = 0,
    READ = 1,
    WRITE = 1 << 1,
    BL_JUMP = 1 << 2,
    RESTART = 1 << 3,
    

class _Data():
    def __init__(self, index, type: str, value=0, rw=True) -> None:
        self.__index = int(index)
        self.__value = value
        self.__type = type
        self.__rw = rw
        self.__size = struct.calcsize(type)

    def value(self, value=None):
        if value is None:
            return self.__value
        elif self.__rw:
            self.__value = struct.unpack('<' + self.__type, struct.pack('<' + self.__type, value))[0]
        
    def index(self) -> enum.IntEnum:
        return self.__index
    
    def type(self) -> str:
        return self.__type

    def size(self) -> int:
        return self.__size



class Protocol():
    CONST_DATA_SIZE = 8
    __RELEASE_URL = "https://github.com/CASMarine/CASXII_MB_FW_FILE/raw/master/CASXII_MotherBoard_V1.0.0.bin"
    def __init__(self, baud=115200, port='/dev/ttyTHS1') -> None:
        self.__ser = serial.Serial(port=port, baudrate=baud, timeout=0.1)
        self.__ack_size = 0
        self.__post_time_sleep = 15 / baud
        self.variables = [
                _Data(Index.HeaderL, 'B', 0x59, rw=False),
                _Data(Index.HeaderH, 'B', 0x73, rw=False),
                _Data(Index.PackageSize, 'B'),
                _Data(Index.Command, 'B'),
                _Data(Index.SoftwareVersion, 'I'),
                _Data(Index.HardwareVersion, 'I'),
                _Data(Index.ErrorCount, 'I'),
                _Data(Index.RollAngle, 'h'),
                _Data(Index.PitchAngle, 'h'),
                _Data(Index.HeadAngle, 'h'),
                _Data(Index.DepthPosition, 'h'),
                _Data(Index.Temperature, 'B'),
                _Data(Index.AccelerationX, 'B'),
                _Data(Index.AccelerationY, 'B'),
                _Data(Index.AccelerationZ, 'B'),
                _Data(Index.HeadAngleControl, 'B'),
                _Data(Index.HeadPIDP, 'f'),
                _Data(Index.HeadPIDI, 'f'),
                _Data(Index.HeadPIDD, 'f'),
                _Data(Index.PitchPIDP, 'f'),
                _Data(Index.PitchPIDI, 'f'),
                _Data(Index.PitchPIDD, 'f'),
                _Data(Index.RollPIDP, 'f'),
                _Data(Index.RollPIDI, 'f'),
                _Data(Index.RollPIDD, 'f'),
                _Data(Index.DepthPIDP, 'f'),
                _Data(Index.DepthPIDI, 'f'),
                _Data(Index.DepthPIDD, 'f'),
                _Data(Index.ControlDataX, 'h'),
                _Data(Index.ControlDataY, 'h'),
                _Data(Index.ControlDataZ, 'h'),
                _Data(Index.ControlDataH, 'h'),
                _Data(Index.ControlDataR, 'h'),
                _Data(Index.ControlDataP, 'h'),
                _Data(Index.ControlDataUpperArm, 'h'),
                _Data(Index.ControlDataLowerArm, 'h'),
                _Data(Index.ControlDataWrist, 'h'),
                _Data(Index.ControlDataGrip, 'h'),
                _Data(Index.ControlDataHome, 'h'),
                _Data(Index.Baudrate, 'I'),
                _Data(Index.CRC, 'I'),
              ]

    def __write_bus(self, data):
        self.__ser.write(data)

    def __read_bus(self, byte_count):
        data = self.__ser.read(byte_count)
        if (len(data) == byte_count):
            return data
        return None
    
    def get_ack_size(self) -> int:
        return self.__ack_size

    def __set_variables(self, idx_list=[], value_list=[]):

        # Set command to write
        self.variables[int(Index.Command)].value(int(Commands.WRITE))

        fmt_str = ''.join([var.type() for var in self.variables[:4]])   # The initial for standart value
        for idx, value in zip(idx_list, value_list):
            self.variables[int(idx)].value(value)
            fmt_str += 'B' + self.variables[int(idx)].type()
        
        struct_out = [var.value() for var in self.variables[:4]]
        for idx in idx_list:
            struct_out += [*[int(idx), self.variables[int(idx)].value()]]
        
        struct_out = list(struct.pack('<' + fmt_str, *struct_out))

        struct_out[int(Index.PackageSize)] = len(struct_out) + self.variables[int(Index.CRC)].size()
        self.variables[int(Index.CRC)].value(CRC32.calc(struct_out))
        
        return bytes(struct_out) + struct.pack('<' + self.variables[int(Index.CRC)].type(), self.variables[int(Index.CRC)].value())

    def set_variables(self, id_list: list, val_list: list):
        data = self.__set_variables(idx_list=id_list, value_list=val_list)
        self.__write_bus(data)

    def __get_variables(self, id_list: list):
        self.variables[int(Index.Command)].value(int(Commands.READ))
        fmt_str = ''.join([var.type() for var in self.variables[:4]])
        
        for _ in id_list:
            fmt_str += 'B'

        self.__ack_size = struct.calcsize(fmt_str) + self.variables[int(Index.CRC)].size() + struct.calcsize(''.join([self.variables[int(idx)].type() for idx in id_list]))
        struct_out = list(struct.pack(fmt_str, *[*[var.value() for var in self.variables[:4]], *[int(index) for index in id_list]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.variables[int(Index.CRC)].size()
        self.variables[int(Index.CRC)].value(CRC32.calc(struct_out))
        return bytes(struct_out) + struct.pack('<' + self.variables[int(Index.CRC)].type(), self.variables[int(Index.CRC)].value())

    def parse_received(self, data):
        data = data[4:-4]
        fmt_str = '<'

        i = 0
        while i < len(data):
            fmt_str += 'B' + self.variables[int(data[i])].type()
            i += self.variables[int(data[i])].size() + 1

        unpacked = list(struct.unpack(fmt_str, data))
        grouped = zip(*(iter(unpacked),) * 2)
        for group in grouped:
            self.variables[group[0]].value(group[1])

    def get_variables(self, id_list: list):
        data = self.__get_variables(id_list)
        self.__write_bus(data)
        time.sleep(self.__post_time_sleep)

        if self.read_ack():
            pass

    def read_ack(self) -> bool:
        ret = self.__read_bus(self.get_ack_size())
        if ret is None:
            return False
        if len(ret) == self.get_ack_size():
            if (CRC32.calc(ret[:-4]) == struct.unpack('<I', ret[-4:])[0]):
                if ret[int(Index.PackageSize)] >= self.__class__.CONST_DATA_SIZE:
                    self.parse_received(ret)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        
    def ping(self) -> bool:
        self.variables[int(Index.Command)].value(Commands.PING)
        fmt_str = ''.join([var.type() for var in self.variables[:4]])
        self.__ack_size = struct.calcsize(fmt_str) + self.variables[int(Index.CRC)].size()
        struct_out = [var.value() for var in self.variables[:4]]
        struct_out = list(struct.pack('<' + fmt_str, *struct_out))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.variables[int(Index.CRC)].size()
        self.variables[int(Index.CRC)].value(CRC32.calc(struct_out))
        data = bytes(struct_out) + struct.pack('<' + self.variables[int(Index.CRC)].type(), self.variables[int(Index.CRC)].value())
        self.__write_bus(data)
        pre_xfer_time = time.time()
        is_alive = self.read_ack()
        post_xfer_time = time.time()
        print("connection is {}, got {} bytes,  time={}".format(is_alive, self.__ack_size, post_xfer_time - pre_xfer_time))
        return is_alive

    def reboot(self):
        self.variables[int(Index.Command)].value(Commands.RESTART)
        fmt_str = ''.join([var.type() for var in self.variables[:4]])
        struct_out = [var.value() for var in self.variables[:4]]
        struct_out = list(struct.pack('<' + fmt_str, *struct_out))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.variables[int(Index.CRC)].size()
        self.variables[int(Index.CRC)].value(CRC32.calc(struct_out))
        data =bytes(struct_out) + struct.pack('<' + self.variables[int(Index.CRC)].type(),
                                               self.variables[int(Index.CRC)].value())
        self.__write_bus(data)

    def enter_bootloader(self):
        self.variables[int(Index.Command)].value(Commands.BL_JUMP)
        fmt_str = ''.join([var.type() for var in self.variables[:4]])
        struct_out = [var.value() for var in self.variables[:4]]
        struct_out = list(struct.pack('<' + fmt_str, *struct_out))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.variables[int(Index.CRC)].size()
        self.variables[int(Index.CRC)].value(CRC32.calc(struct_out))
        data = bytes(struct_out) + struct.pack('<' + self.variables[int(Index.CRC)].type(),
                                            self.variables[int(Index.CRC)].value())
        print(list(data))
        self.__write_bus(data)

    def update_fw_version(self):
        fw_file = tempfile.NamedTemporaryFile("wb+")
    
        response = requests.get(url=self.__class__.__RELEASE_URL)
        if response.status_code == 200 :
            
            response = requests.get(url=self.__class__.__RELEASE_URL)
            if (response.status_code == 200):
                fw_file.write(response.content)
            else:
                raise Exception("Could not fetch requested binary file! Check your connection to GitHub.")

            self.enter_bootloader()
            time.sleep(0.1)

            # Close serial port
            serial_settings = self.__ser.get_settings()
            self.__ser.close()

            # Upload binary
            args = ['-p', self.__ser.portstr, '-b', str(115200), '-e', '-w', '-v', fw_file.name]
            stm32loader_main(*args)

            # Delete uploaded binary
            if (not fw_file.closed):
                fw_file.close()

            # Re open port to the user with saved settings
            self.__ser.apply_settings(serial_settings)
            self.__ser.open()
            return True
        else:
            raise Exception("Could not found requested firmware files list! Check your connection to GitHub.")