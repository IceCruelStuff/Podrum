"""
*  ____           _
* |  _ \ ___   __| |_ __ _   _ _ __ ___
* | |_) / _ \ / _` | '__| | | | '_ ` _ \
* |  __/ (_) | (_| | |  | |_| | | | | | |
* |_|   \___/ \__,_|_|   \__,_|_| |_| |_|
*
* Licensed under the Apache License, Version 2.0 (the "License")
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""

from struct import unpack, pack, calcsize
from re import match
import decimal
import sys
from .bcmath import bcmath

class Binary:

    def checkLength(string, expect):
        length = len(string)
        assert (length == expect), 'Expected ' + str(expect) + 'bytes, got ' + str(length)
        
    @staticmethod
    def signByte(value: int):
        if calcsize == 8:
            return (int(value) & 0xffffffff) >> 56
        else:
            return (int(value) & 0xffffffff) >> 24

    @staticmethod
    def unsignByte(value: int):
        return int(value) & 0xff

    @staticmethod
    def signShort(value: int):
        if calcsize == 8:
            return (int(value) & 0xffffffff) >> 48
        else:
            return (int(value) & 0xffffffff) >> 16

    @staticmethod
    def unsignShort(value: int):
        return int(value) & 0xffff

    @staticmethod
    def signInt(value: int):
        if calcsize == 8:
            return (int(value) & 0xffffffff) >> 32
        else:
            return (int(value) & 0xffffffff) >> 31

    @staticmethod
    def unsignInt(value: int):
        return int(value) & 0xffffffff

    @staticmethod
    def readTriad(str: bytes) -> int:
        Binary.checkLength(str, 3)
        return unpack('>L', b'\x00' + str)[0]

    @staticmethod
    def writeTriad(value: int) -> bytes:
        return pack('>L', value)[1:]

    @staticmethod
    def readLTriad(str: bytes) -> int:
        Binary.checkLength(str, 3)
        return unpack('<L', b'\x00' + str)[0]

    @staticmethod
    def writeLTriad(value: int) -> bytes:
        return pack('<L', value)[0:-1]
    
    @staticmethod
    def readBool(b: bytes) -> int:
        return unpack('?', b)[0]

    @staticmethod
    def writeBool(b: int) -> bytes:
        return b'\x01' if b else b'\x00'
  
    @staticmethod
    def readByte(c: bytes) -> int:
        Binary.checkLength(c, 1)
        return unpack('>B', c)[0]
    
    @staticmethod
    def readSignedByte(c: bytes) -> int:
        Binary.checkLength(c, 1)
        return unpack('>b', c)[0]

    @staticmethod
    def writeByte(c: int) -> bytes:
        return pack(">B", c)
    
    @staticmethod
    def readShort(str: bytes) -> int:
        Binary.checkLength(str, 2)
        return unpack('>H', str)[0]
    
    @staticmethod
    def readSignedShort(str: bytes) -> int:
        Binary.checkLength(str, 2)
        return Binary.signShort(Binary.readShort(str))

    @staticmethod
    def writeShort(value: int) -> bytes:
        return pack('>H', value)
    
    @staticmethod
    def readLShort(str: bytes) -> int:
        Binary.checkLength(str, 2)
        return unpack('<H', str)[0]
    
    @staticmethod
    def readSignedLShort(str: bytes) -> int:
        Binary.checkLength(str, 2)
        return Binary.signShort(Binary.readLShort(str))

    @staticmethod
    def writeLShort(value: int) -> bytes:
        return pack('<H', value)
    
    @staticmethod
    def readInt(str: bytes) -> int:
        Binary.checkLength(str, 4)
        return unpack('>L', str)[0]

    @staticmethod
    def writeInt(value: int) -> bytes:
        return pack('>L', value)

    @staticmethod
    def readLInt(str: bytes) -> int:
        Binary.checkLength(str, 4)
        return unpack('<L', str)[0]

    @staticmethod
    def writeLInt(value: int) -> bytes:
        return pack('<L', value)

    @staticmethod
    def readFloat(str: bytes) -> int:
        Binary.checkLength(str, 4)
        return unpack('>f', str)[0]
    
    @staticmethod
    def readRoundedFloat(str, accuracy):
        return round(Binary.readFloat(str), accuracy)

    @staticmethod
    def writeFloat(value: int) -> bytes:
        return pack('>f', value)

    @staticmethod
    def readLFloat(str: bytes) -> int:
        Binary.checkLength(str, 4)
        return unpack('<f', str)[0]
    
    @staticmethod
    def readRoundedLFloat(str, accuracy):
        return round(Binary.readLFloat(str), accuracy)

    @staticmethod
    def writeLFloat(value: int) -> bytes:
        return pack('<f', value)
    
    
    @staticmethod
    def printFloat(value):
        return match(r"/(\\.\\d+?)0+$/", "" + value).group(1)

    @staticmethod
    def readDouble(str: bytes) -> int:
        Binary.checkLength(str, 8)
        return unpack('>d', str)[0]

    @staticmethod
    def writeDouble(value: int) -> bytes:
        return pack('>d', value)

    @staticmethod
    def readLDouble(str: bytes) -> int:
        Binary.checkLength(str, 8)
        return unpack('<d', str)[0]

    @staticmethod
    def writeLDouble(value: int) -> bytes:
        return pack('<d', value)

    @staticmethod
    def readLong(str: bytes) -> int:
        Binary.checkLength(str, 8)
        return unpack('>L', str)[0]

    @staticmethod
    def writeLong(value: int) -> bytes:
        return pack('>L', value)

    @staticmethod
    def readLLong(str: bytes) -> int:
        Binary.checkLength(str, 8)
        return unpack('<L', str)[0]

    @staticmethod
    def writeLLong(value: int) -> bytes:
        return pack('<L', value)
   
    @staticmethod
    def readUnsignedVarInt(buffer, offset):
        value = "0";
        buffer = str(buffer)
        i = 0
        while i <= 35:
            i += 7
            offset += 1
            b = ord(buffer[offset])
            value = bcmath.bcadd(value, bcmath.bcmul(str(b & 0x7f), bcmath.bcpow("2", str(i))))
            if (b & 0x80) == 0:
                return value
            elif (len(buffer) - 1) < int(offset):
                raise TypeError('Expected more bytes, none left to read')
        raise TypeError('Varint did not terminate after 5 bytes!')

    @staticmethod
    def readVarInt(buffer, offset):
        raw = Binary.readUnsignedVarInt(buffer, offset)
        temp = bcmath.bcdiv(raw, "2")
        if bcmath.bcmod(raw, "2") == "1":
            temp = bcmath.bcsub(bcmath.bcmul(temp, "-1"), "1")
        return temp
    
    @staticmethod
    def writeUnsignedVarInt(value):
        buffer = ""
        value = value & 0xffffffff
        if bcmath.bccomp(value, "0") == -1:
            value = bcmath.bcadd(value, "18446744073709551616")
        i = 0
        while i <= 5:
            i = i + 1
            byte = int(bcmath.bcmod(value, "128"))
            value = bcmath.bcdiv(value, "128")
            if value != 0:
                buffer += chr(byte | 0x80)
            else:
                buffer += chr(byte)
                return buffer
        raise TypeError('Value too large to be encoded as a varint')
     
    @staticmethod
    def writeVarInt(value):
        value = bcmath.bcmod(bcmath.bcmul(value, "2"), "18446744073709551616")
        if bcmath.bccomp(value, "0") == -1:
            value = bcmath.bcsub(bcmath.bcmul(value, "-1"), "1")
        return Binary.writeUnsignedVarInt(value)
    
    @staticmethod
    def readUnsignedVarLong(buffer, offset):
        value = "0"
        buffer = str(buffer)
        i = 0
        while i <= 63:
            i += 7
            offset += 1
            b = ord(buffer[offset])
            value = bcmath.bcadd(value, bcmath.bcmul(str(b & 0x7f), bcmath.bcpow("2", str(i))))

            if (b & 0x80) == 0:
                return value
            elif (len(buffer) - 1) < int(offset):
                raise TypeError("Expected more bytes, none left to read")

        raise TypeError("VarLong did not terminate after 10 bytes!")
        
    @staticmethod
    def readVarLong(buffer, offset):
        raw = Binary.readUnsignedVarLong(buffer, offset)
        temp = bcmath.bcdiv(raw, "2")
        if bcmath.bcmod(raw, "2") == "1":
            temp = bcmath.bcsub(bcmath.bcmul(temp, "-1"), "1")
        return temp
    
    @staticmethod
    def writeUnsignedVarLong(value):
        buffer = ""
        if bcmath.bccomp(value, "0") == -1:
            value = bcmath.bcadd(value, "18446744073709551616")
        i = 0
        while i <= 10:
            i = i + 1
            byte = int(bcmath.bcmod(value, "128"))
            value = bcmath.bcdiv(value, "128")
            if value != 0:
                buffer += chr(byte | 0x80)
            else:
                buffer += chr(byte)
                return buffer
        raise TypeError("Value too large to be encoded as a VarLong")
        
    @staticmethod
    def writeVarLong(value):
        value = bcmath.bcmod(bcmath.bcmul(value, "2"), "18446744073709551616")
        if bcmath.bccomp(value, "0") == -1:
            value = bcmath.bcsub(bcmath.bcmul(value, "-1"), "1")
        return Binary.writeUnsignedVarLong(value)
    
    @staticmethod
    def flipShortEndianness(value):
        return Binary.readLShort(Binary.writeShort(value))

    @staticmethod
    def flipIntEndianness(value):
        return Binary.readLInt(Binary.writeInt(value))

    @staticmethod
    def flipLongEndianness(value):
        return Binary.readLLong(Binary.writeLong(value))
