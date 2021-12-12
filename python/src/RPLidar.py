''' Basic module for working with RPLidar'''
'''         Author: DONG HAITAO          '''

# Import libraries
import codecs
import serial
import struct
import sys
import time

# Define parameters
SCAN_MODE = {
    'normal': {'byte': b'\x20', 'response': 129, 'size': 5},
    'force': {'byte': b'\x21', 'response': 129, 'size': 5},
}

SYNC_BYTE = b'\xA5'
SYNC_BYTE2 = b'\x5A'

GET_INFO_BYTE = b'\x50'
GET_HEALTH_BYTE = b'\x52'

STOP_BYTE = b'\x25'
RESET_BYTE = b'\x40'

DESCRIPTOR_LEN = 7
INFO_LEN = 20
HEALTH_LEN = 3

INFO_TYPE = 4
HEALTH_TYPE = 6

MAX_PWM = 1023
DEFAULT_PWM = 660
SET_PWM_BYTE = b'\xF0'

_HEALTH_STATUS = {
    0: 'Good',
    1: 'Warning',
    2: 'Error',
}

class rplidar():
    def __init__(self, port, baudrate=115200, timeout=1):
        '''Initialize connection for RPLidar sensor'''

        self._serial = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.rotary = None
        self._rotary_speed = DEFAULT_PWM
        self.scanning = [False, 0, 'normal']        
        self.express_data = False
        self.express_trame = 32
        self.connect()
    
    def connect(self):
        '''Connects to the serial port with the name `self.port`. 
        If it was connected to another serial port disconnects from it first.'''
        if self._serial is not None:
            self.disconnect()
        try:
            self._serial = serial.Serial(
                self.port, self.baudrate,
                parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout)
        except serial.SerialException as err:
            print('Failed to connect to the sensor due to: %s' % err)
    
    def disconnect(self):
        '''Disconnects from the serial port'''
        if self._serial is None:
            return
        self._serial.close()

    def start_rotary(self): # start_motor
        '''Starts sensor motor'''
        self._serial.setDTR(False)
        self._set_pwm(self._rotary_speed)
        self.rotary = True # motor_running

    def stop_rotary(self): # stop_motor
        '''Stops sensor motor'''
        self._set_pwm(0)
        time.sleep(.001)
        self._serial.setDTR(True)
        self.rotary = False
    
    def motor_speed(self):
        '''Sensor motor rotates at default speed'''
        return self._rotary_speed
    
    def motor_speed(self, pwm):
        '''Sensor motor rotates at selected speed'''
        if 0 < pwm < MAX_PWM:
            self._rotary_speed = pwm
        else:
            self._rotary_speed = MAX_PWM
        if self.rotary:
            self._set_pwm(self._rotary_speed)
    
    def _set_pwm(self, pwm):
        payload = struct.pack("<H", pwm)
        self._send_payload_cmd(SET_PWM_BYTE, payload)
    
    def _send_payload_cmd(self, cmd, payload):
        '''Sends `cmd` command with `payload` to the sensor'''
        size = struct.pack('B', len(payload))
        req = SYNC_BYTE + cmd + size + payload
        checksum = 0
        for v in struct.unpack('B'*len(req), req):
            checksum ^= v
        req += struct.pack('B', checksum)
        self._serial.write(req)

    def _send_cmd(self, cmd):
        '''Sends `cmd` command to the sensor'''
        req = SYNC_BYTE + cmd
        self._serial.write(req)              
           
    def _read_descriptor(self):
        '''Reads descriptor packet'''
        descriptor = self._serial.read(DESCRIPTOR_LEN)
        is_single = b2i(descriptor[-2]) == 0
        return b2i(descriptor[2]), is_single, b2i(descriptor[-1])        
     
    def _read_response(self, dsize):
        '''Reads response packet with length of `dsize` bytes'''
        while self._serial.inWaiting() < dsize:
            time.sleep(0.001)
        data = self._serial.read(dsize)
        return data
    
    def get_info(self):
        '''Get sensor information

        Returns
        -------
        dict
            Dictionary with the sensor information
        '''
        if self._serial.inWaiting() > 0:
            return ('Data in buffer, you can\'t have info ! '
                    'Run clean_input() to emptied the buffer.')
        self._send_cmd(GET_INFO_BYTE)
        dsize, is_single, dtype = self._read_descriptor()
        raw = self._read_response(dsize)
        serialnumber = codecs.encode(raw[4:], 'hex').upper()
        serialnumber = codecs.decode(serialnumber, 'ascii')
        data = {
            'model': b2i(raw[0]),
            'firmware': (b2i(raw[2]), b2i(raw[1])),
            'hardware': b2i(raw[3]),
            'serialnumber': serialnumber,
        }
        return data
    
    def get_health(self):
        '''Get device health state.

        Returns
        -------
        status : str
            'Good', 'Warning' or 'Error' statuses
        error_code : int
            The related error code that caused a warning/error.
        '''
        if self._serial.inWaiting() > 0:
            return ('Data in buffer, you can\'t have info ! '
                    'Run clean_input() to emptied the buffer.')
        self._send_cmd(GET_HEALTH_BYTE)
        dsize, is_single, dtype = self._read_descriptor()
        raw = self._read_response(dsize)
        status = _HEALTH_STATUS[b2i(raw[0])]
        error_code = (b2i(raw[1]) << 8) + b2i(raw[2])
        return status, error_code

    def clean_input(self):
        '''Clean input buffer by reading all available data'''
        if self.scanning[0]:
            return 'Cleanning not allowed during scanning process active !'
        self._serial.flushInput()
        self.express_trame = 32
        self.express_data = False
    
    def start(self, scan_mode='normal'):
        '''Start the scanning process

        Parameters
        ----------
        scan : normal, force or express.
        '''
        if self.scanning[0]:
            return 'Scanning already running !'
        # RPLidar health check
        status, error_code = self.get_health()
        if status == _HEALTH_STATUS[2]:
            self.reset()
            status, error_code = self.get_health()
            if status == _HEALTH_STATUS[2]:
                print('RPLidar hardware failure. '
                                       'Error code: %d' % error_code)
        elif status == _HEALTH_STATUS[1]:
            print('Warning sensor status detected! '
                                'Error code: %d', error_code)
        # Scan mode check
        cmd = SCAN_MODE[scan_mode]['byte']
        self._send_cmd(cmd)
        dsize, is_single, dtype = self._read_descriptor()
        self.scanning = [True, dsize, scan_mode]
    
    def stop(self):
        '''Stops scanning process, disables laser diode and the measurement
        system, moves sensor to the idle state.'''
        self._send_cmd(STOP_BYTE)
        time.sleep(.1)
        self.scanning[0] = False
        self.clean_input()
    
    def reset(self):
        '''Resets sensor core, reverting it to a similar state as it has
        just been powered up.'''
        self._send_cmd(RESET_BYTE)
        time.sleep(2)
        self.clean_input()
    
    def measurements(self, scan_type='normal', max_buf_meas=3000):
        '''Rotates motor and starts scan.

        Parameters
        ----------
        max_buf_meas : int or False if you want unlimited buffer
            Maximum number of bytes to be stored inside the buffer.

        Yields
        ------
        angle : float
            The measure heading angle in degree unit [0, 360)
        distance : float
            Measured object distance related to the sensor's rotation center.
            In millimeter unit. Set to 0 when measure is invalid.
        '''
        self.start_rotary()
        if not self.scanning[0]:
            self.start(scan_type)
        while True:
            dsize = self.scanning[1]
            if max_buf_meas:
                data_in_buf = self._serial.inWaiting()
                if data_in_buf > max_buf_meas:
                    self.stop()
                    self.start(self.scanning[2])
            raw = self._read_response(dsize)
            yield read_output(raw)

def b2i(byte):
    '''Converts byte to integer (for Python 2 compatability)'''
    return byte if int(sys.version[0]) == 3 else ord(byte)

def read_output(raw):
    '''Processes input raw data and returns measurement data'''
    angle = ((b2i(raw[1]) >> 1) + (b2i(raw[2]) << 7)) / 64.
    distance = (b2i(raw[3]) + (b2i(raw[4]) << 8)) / 4.
    #print("Angle %.2f degree - Distance %.2f mm" %(angle, distance))
    return angle, '  -  ', distance