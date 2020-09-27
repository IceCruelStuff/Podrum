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

from podrum.nbt.NBTStream import NBTStream
from podrum.utils.Binary import Binary
import struct

class LittleEndianNBTStream(NBTStream):
    def getShort(self):
        return Binary.readLShort(self.get(2))

    def getSignedShort(self):
        return Binary.readSignedLShort(self.get(2))

    def putShort(self, v: int):
        self.put(Binary.writeLShort(v))

    def getInt(self):
        return Binary.readLInt(self.get(4))

    def putInt(self, v: int):
        self.put(Binary.writeLInt(v))

    def getLLong(self):
        return Binary.readLLong(self.get(8))

    def putLLong(self, v: int):
        self.put(Binary.writeLLong(v))

    def getLFloat(self):
        return Binary.readLFloat(self.get(4))

    def putFloat(self, v):
        self.put(Binary.writeLFloat(v))

    def getDouble(self):
        return Binary.readLDouble(self.get(8))

    def putDouble(self, v):
        self.put(Binary.writeLDouble(v))

    def getIntArray(self):
        len = self.getInt()
        return struct.unpack_from("V*", self.get(len * 4))

    def putIntArray(self, array):
        self.putInt(len(array))
        self.put(struct.pack("V*", array))
