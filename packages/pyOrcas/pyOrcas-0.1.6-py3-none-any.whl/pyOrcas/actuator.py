# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:34:23 2024

@author: DAlexander, work based on code by RMcWilliam's Matlab integration
Can read and write parameters, configure all haptic effects, and kinematic motions

Classes
Actuator
|-Haptic
|-Kinematic

Usage:
    from pyOrcas import Actuator
    
    actuator = Actuator(port='COM3', baudrate=9600)
"""

from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
import struct
from .constants import *
import time


class Actuator:
    """ DEFAULT CLASS METHODS """
    def __init__(self, port:str, baudrate:int):
        """Constructs the class based on provide COM and baudrate"""
        self.client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, parity='E', stopbits=1, bytesize=8, timeout=1000)
        if self.client.connect():
            print("Modbus connection successful.")
        else:
            print("Modbus connection failed.")
            self.close()
            
        # Initialize mode handlers
        self.haptic = self._HapticMode(self)
        self.kinematic = self._KinematicMode(self)
        
        # Initialize motor properties
        self._position = 0 #Set as both property and setter
        self._force = 0 #Set as both property and setter
        self._power = 0
        self._temperature = 0
        self._voltage = 0
        self._errors = 0
        self._op_mode = 0
        
        # Initialize device information
        self.stator_type = None
        self.device_name = None
        self.serial_number = None
        self.revision = None
        
        self._initialize_info() #Set basic information of actuator, cannot be in init
        
    def __str__(self):
        """String representation of the Actuator object"""
        return (          
            f"Device Name: {self.device_name}\n"
            f"Serial Number: {self.serial_number}\n"
            f"Firmware: {self.revision}\n"
        )
        
    def __del__(self):
        """Ensure the Modbus connection is closed when the object is deleted."""
        self.close()
        
    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object."""
        self.close()
        
    """ GETTERS AND SETTERS """        
    @property
    def position(self):
        self.read_stream(0,1)
        return self._position
    
    @position.setter
    def position(self, position_um:int):
        positionbytes = struct.pack('>i', position_um)
        message = [1, MotorCommand, 30] + list(positionbytes)
        message_with_crc = self._append_crc(message)
        
        #self._flush_input_buffer()
        self.client.send(bytes(message_with_crc))
        data=self.client.recv(19)

        self._position = struct.unpack('>i', bytes(data[2:6]))[0]
        self._force = struct.unpack('>i', bytes(data[6:10]))[0]
        self._power = struct.unpack('>H', bytes(data[10:12]))[0]
        self._temperature = data[12]
        self._voltage = struct.unpack('>H', bytes(data[13:15]))[0]
        self._errors = struct.unpack('>H', bytes(data[15:17]))[0]
    
    @property
    def force(self):
        self.read_stream(0,1)
        return self._force
    
    @force.setter
    def force(self, force_mN:int):
        forcebytes = struct.pack('>i', force_mN)
        message = [1, MotorCommand, 28] + list(forcebytes)
        message_with_crc = self._append_crc(message)
        
        #self._flush_input_buffer()
        self.client.send(bytes(message_with_crc))
        data=self.client.recv(19)

        self._position = struct.unpack('>i', bytes(data[2:6]))[0]
        self._force = struct.unpack('>i', bytes(data[6:10]))[0]
        self._power = struct.unpack('>H', bytes(data[10:12]))[0]
        self._temperature = data[12]
        self._voltage = struct.unpack('>H', bytes(data[13:15]))[0]
        self._errors = struct.unpack('>H', bytes(data[15:17]))[0]
    
    @property
    def power(self):
        self.read_stream(0,1)
        return self._power
    
    @property
    def temperature(self):
        self.read_stream(0,1)
        return self._temperature
    
    @property
    def voltage(self):
        self.read_stream(0,1)
        return self._voltage
    
    @property
    def errors(self):
        self.read_stream(0,1)
        return self._errors
    
    @property
    def op_mode(self):
        self.read_stream(0,1)
        return self._op_mode
        
        
    def close(self):
        self.client.close()  
        
    """ INTERNAL COMMANDS """
    
    def _initialize_info(self):
        #Basic Stator Information        
        self.stator_type=self.read_register(418, 1)[0]
        
        if self.stator_type==0:        
            self.device_name="Orca-6-24V"
        elif self.stator_type==1:  
            self.device_name="Orca-6-48V"
        elif self.stator_type==2:  
            self.device_name="Orca-15-48V"
        else:
            self.device_name="Unknown"
        
        sn_u16s=self.read_register(406, 2)
        self.serial_number=self._combine_u16_to_u32(sn_u16s[0],sn_u16s[1])
        
        rev=self.read_register(408, 3)
        self.revision=f"{rev[0]}.{rev[1]}.{rev[2]}"

        self.sleep()
        time.sleep(0.1)
        
    
    def _u16_to_bytes(self, data):
        """Convert a 16-bit unsigned integer to a byte array in big-endian order."""
        if isinstance(data, list):
            result = []
            for value in data:
                result.extend(struct.pack('>H', value))
            return result
        else:
            return list(struct.pack('>H', data))  # Use '>' for big-endian
    
    
    def _int32_to_u16(self, data):
        """Convert a 32-bit integer to a 16-bit unsigned integer."""
        if not (-2**31 <= data < 2**31):
            raise ValueError("Input data is out of range for a 32-bit integer")
        byte_data = struct.pack('<i', data)
        return list(struct.unpack('<2H', byte_data))
    
    
    def _combine_u16_to_u32(self, low, high):
        """Combine two 16-bit unsigned integers into a single 32-bit unsigned integer."""
        return (high << 16) | low
    
    

    def _calculate_crc(self, message):
        """Calculate the CRC for a Modbus message."""
        crc = 0xFFFF
        polynomial = 0xA001
        for byte in message:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc >>= 1
                    crc ^= polynomial
                else:
                    crc >>= 1
        low_byte = crc & 0xFF
        high_byte = (crc >> 8) & 0xFF
        return [low_byte, high_byte]
    
    
    def _append_crc(self, message):
        """Append the CRC to the message."""
        return message + self._calculate_crc(message)
        
    """ READ AND WRITE COMMANDS """

    def read_register(self, register_address:int, num_registers:int):
        """Read Modbus registers by sending a custom message with CRC."""
        address_bytes = self._u16_to_bytes(register_address)
        num_registers_bytes = self._u16_to_bytes(num_registers)
        message = [1, Read] + address_bytes + num_registers_bytes  # 1 for slave address, 3 for read function code
        message_with_crc = self._append_crc(message)
        
        self.client.send(bytes(message_with_crc))
        data = self.client.recv(5 + 2 * num_registers)
        
        if not data:
            print("Failed to read registers")
            return None

        read_value = []
        for i in range(num_registers):
            high_byte = data[2 * i + 3]
            low_byte = data[2 * i + 4]
            value = struct.unpack('H', struct.pack('BB', low_byte, high_byte))[0]
            read_value.append(value)

        return read_value
        
    def write_registers(self, registers_start_address:int, register_data:int):
        """Write multiple values to consecutive Modbus registers.
        Can accept an array of integers or individual integers, and will write
        consecutive registers equal to the number of arguments"""
        
        # Ensure register_data is a list
        if isinstance(register_data, int):
            register_data = [register_data]
        
        num_registers = len(register_data)
        databytes = self._u16_to_bytes(register_data)
        num_registers_bytes = self._u16_to_bytes(num_registers)
        address_bytes = self._u16_to_bytes(registers_start_address)
        byte_count = [num_registers * 2]

        message = [1, Write_Multi] + address_bytes + num_registers_bytes + byte_count + databytes
        message_with_crc = self._append_crc(message)
        
        self.client.send(bytes(message_with_crc))
        self.client.recv(8)
        
    def write_stream(self, registers_start_address:int, width:int, value:int):
        address_bytes = self._u16_to_bytes(registeraddr)
        value_bytes = struct.pack('>i', value)
        message = [1, MotorWrite] + address_bytes + [width] + list(value_bytes)
        message_with_crc = self._append_crc(message)
        
        self.client.send(bytes(message_with_crc))
        data=self.client.recv(20)
        
        if len(data) == 20:
            self._op_mode = data[2]
            self._position = struct.unpack('>i', bytes(data[3:7]))[0]
            self._force = struct.unpack('>i', bytes(data[7:11]))[0]
            self._power = struct.unpack('>H', bytes(data[11:13]))[0]
            self._temperature = data[13]
            self._voltage = struct.unpack('>H', bytes(data[14:16]))[0]
            self._errors = struct.unpack('>H', bytes(data[16:18]))[0]
        else:
            print("Received data length is incorrect")
        
    def read_stream(self,register_address:int,width:int):
        address_bytes = self._u16_to_bytes(register_address)
        message = [1, MotorRead] + address_bytes + [width]
        message_with_crc = self._append_crc(message)
        
        self.client.send(bytes(message_with_crc))
        data=self.client.recv(24)
        
        if len(data) == 24:
            self._op_mode = data[6]
            read_value = struct.unpack('>i', data[2:6])[0]
            self._position = struct.unpack('>i', bytes(data[7:11]))[0]
            self._force = struct.unpack('>i', bytes(data[11:15]))[0]
            self._power = struct.unpack('>H', bytes(data[15:17]))[0]
            self._temperature = data[17]
            self._voltage = struct.unpack('>H', bytes(data[18:20]))[0]
            self._errors = struct.unpack('>H', bytes(data[20:22]))[0]
            
            return float(read_value)
        else:
            print("Received data length is incorrect")
    
    """ SPECIFIC ORCA FUNCTIONS """
    def sleep(self):
        """Put motor to sleep"""
        self.write_registers(MODE_Reg, SleepMode)
    
    def Tune_PID(self, saturation:int, p_gain:int, i_gain:int, dv_gain:int, de_gain:int):
        sat_data=self._int32_to_u16(saturation)
        data=[p_gain,i_gain,dv_gain,de_gain]+sat_data
        
        self.write_registers(133, data)


    """ NESTED HAPTICS OBJECT """
    class _HapticMode:
        def __init__(self, actuator):
            self.actuator = actuator #Allows use of parent class methods in nested object

        def enable(self):
            """Enable Haptics"""
            self.actuator.write_registers(MODE_Reg, HapticMode)
            
        """ HAPTIC EFFECTS """
        def set_spring(self, ID:int, gain:int, center:int, deadzone:int, saturation: int=0, coupling: int=0, enable: bool=None):
            """Set spring components (A,B, or C). Can enable the spring optionally as well"""

            # Check if variables are valid
            if not (isinstance(ID, int) and ID in [0, 1, 2]):
                print("Error: Invalid spring ID. Must be 0, 1, or 2.")
                return
            
            if not (isinstance(coupling, int) and coupling in [0, 1, 2]):
                print("Error: Invalid coupling value. Must be 0, 1, or 2.")
                return
        
            # Check if all values are positive integers
            if not all(isinstance(x, int) and x >= 0 for x in [gain, center, deadzone, saturation]):
                print("Error: All values must be positive integers.")
                return
    
            # Constructing message
            centerLH = self.actuator._int32_to_u16(center)
            data = [gain] + centerLH + [coupling, deadzone, saturation]
            self.actuator.write_registers(int(644 + ID * 6), data)  # setting spring parameters
            
            if enable!=None: # Set enable of spring if actually set
                self.toggle_spring(ID, enable)
        
        def toggle_spring(self, ID:int, enable: bool=True):
            """Enable spring ID to True or False"""
            effect_bits=self.actuator.read_register(641,1)[0]
            if enable == True:
                self.actuator.write_registers(641, effect_bits | (1 << (1 + ID)))
            else:
                self.actuator.write_registers(641, effect_bits & ~(1 << (1 + ID)))
                
        def set_oscillator(self, ID:int, gain:int, osctype:int, freq:int, duty:int, enable: bool=None):
            """Set oscilaltor components (A, or B). Can enable the effect optionally as well"""
            
            # Check if variables are valid
            if not (isinstance(ID, int) and ID in [0, 1]):
                print("Error: Invalid oscillator ID. Must be 0, or 1.")
                return
            
            if not (isinstance(osctype, int) and osctype in [0, 1, 2, 3]):
                print("Error: Invalid coupling value. Must be 0 (square), 1(sine), 2(triangle), or 3(saw).")
                return
        
            # Check if all values are positive integers
            if not all(isinstance(x, int) and x >= 0 for x in [gain, freq, duty]):
                print("Error: All values must be positive integers.")
                return
    
            # Constructing message
            data = [gain, osctype, freq, duty]
            self.actuator.write_registers(int(664 + ID * 4), data)  # setting parameters
            
            if enable!=None: # Set enable of oscillator if actually set
                self.toggle_oscillator(ID, enable)
        
        def toggle_oscillator(self, ID:int, enable: bool=True):
            """Enable oscillator ID to True or False"""
            effect_bits=self.actuator.read_register(641,1)[0]
            if enable == True:
                self.actuator.write_registers(641, effect_bits | (1 << (6 + ID)))
            else:
                self.actuator.write_registers(641, effect_bits & ~(1 << (6 + ID)))
                
        def set_force(self, gain:int, enable: bool=None):
            """Set constant force. Can enable the force optionally as well"""
        
            # Check if gain is integer
            if not isinstance(gain, int):
                print("Error: Gain must be an integer")
                return
    
            # Constructing message
            data = self.actuator._int32_to_u16(gain)
            self.actuator.write_registers(642, data)  # setting parameters
            
            if enable!=None: # Set enable of force if actually set
                self.toggle_force(enable)
        
        def toggle_force(self, enable: bool=True):
            """Enable force to True or False"""
            effect_bits=self.actuator.read_register(641,1)[0]
            if enable == True:
                self.actuator.write_registers(641, effect_bits | (1 << (0)))
            else:
                self.actuator.write_registers(641, effect_bits & ~(1 << (0)))
                 
        def set_damper(self, gain:int, enable: bool=None):
            """Set damper. Can enable the damper optionally as well"""
        
            # Check if gain is integer
            if not isinstance(gain, int):
                print("Error: Gain must be an integer")
                return
    
            # Constructing message
            self.actuator.write_registers(662, gain)  # setting parameters
            
            if enable!=None: # Set enable of damper if actually set
                self.toggle_damper(enable)
        
        def toggle_damper(self, enable: bool=True):
            """Enable damper to True or False"""
            effect_bits=self.actuator.read_register(641,1)[0]
            if enable == True:
                self.actuator.write_registers(641, effect_bits | (1 << (4)))
            else:
                self.actuator.write_registers(641, effect_bits & ~(1 << (4)))
                
        def set_intertia(self, gain:int, enable: bool=None):
            """Set inertia. Can enable the inertia optionally as well"""
        
            # Check if gain is integer
            if not isinstance(gain, int):
                print("Error: Gain must be an integer")
                return
    
            # Constructing message
            self.actuator.write_registers(663, gain)  # setting parameters
            
            if enable!=None: # Set enable of inertia if actually set
                self.toggle_inerta(enable)
        
        def toggle_inertia(self, enable: bool=True):
            """Enable damper to True or False"""
            effect_bits=self.actuator.read_register(641,1)[0]
            if enable == True:
                self.actuator.write_registers(641, effect_bits | (1 << (5)))
            else:
                self.actuator.write_registers(641, effect_bits & ~(1 << (5)))
                                     
        def toggle_effects(self, f: bool=False, s0: bool=False, s1: bool=False, 
                           s2: bool=False, d: bool=False, i: bool=False, 
                           o1: bool=False, o2: bool=False)  :
            """Take booleans of the haptic effects to set value"""
            array=[o2,o1,i,d,s2,s1,s0,f]
            data=int("".join(["01"[i] for i in array]), 2)
            self.actuator.write_registers(641, data)
                
            
    """ NESTED KINEMATICS OBJECT """
    class _KinematicMode:
        def __init__(self, actuator):
            self.actuator = actuator #Allows use of parent class methods in nested object
            
        def enable(self):
            """Enable Kinematics"""
            self.actuator.write_registers(MODE_Reg, KinematicMode)
            
        """ KINEMATIC MOTIONS """            
        def set_motion(self,ID:int,position:int,time:int,delay:int,nextID:int,autonext:int,motion_type:int=0):
            """Set parameters of motion based on ID"""
            # Check if variables are valid
            if not (isinstance(motion_type, int) and motion_type in [0, 1]):
                print("Error: Invalid motion type. Must be 0, or 1.")
                return
            
            if not (isinstance(autonext, int) and autonext in [0, 1]):
                print("Error: Invalid autonext value. Must be 0, or 1.")
                return
            
            if not (isinstance(nextID, int) and nextID <= 31 and nextID>= 0):
                print("Error: Next ID must be from 0 t0 31")
                return
        
            # Check if all values are positive integers
            if not all(isinstance(x, int) and x >= 0 for x in [position, time, delay]):
                print("Error: All values must be positive integers.")
                return
            
            positionLH = self.actuator._int32_to_u16(position)
            timeLH = self.actuator._int32_to_u16(time)
            combined=(nextID << 3) + (motion_type << 1) + autonext
            data=positionLH+timeLH+[delay,combined]
            
            self.actuator.write_registers(780+ID*6,data)
            
        def trigger(self,ID:int):
            """Trigger kinematic motion id"""
            self.enable()
            self.actuator.write_registers(9,ID)