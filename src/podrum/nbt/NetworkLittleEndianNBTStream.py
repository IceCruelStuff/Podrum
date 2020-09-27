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

from podrum.nbt.LittleEndianNBTStream import LittleEndianNBTStream
from podrum.utils.Binary import Binary

class NetworkLittleEndianNBTStream(LittleEndianNBTStream):
    def getInt(self):
        return Binary.readVarInt(self.buffer, self.offset)

    def putInt(self, v: int):
        self.put(Binary.writeVarInt(v))
    
    def getLong(self):
        return Binary.readVarLong(self.buffer, self.offset)

    def putLong(self, v: int):
        self.put(Binary.writeVarLong(v))

    def getString(self):
        return self.get(self.checkReadStringLength(Binary.readUnsignedVarInt(self.buffer, self.offset)))

    def putString(self, v: str):
        self.put(Binary.writeUnsignedVarInt(self.checkWriteStringLength(len(v))) + v)

    def getIntArray(self):
        len = self.getInt() # varint
        ret = []
        i = 0
        while i < len:
            i += 1
            ret[] = self.getInt() # varint

        return ret

    def putIntArray(self, array):
        self.putInt(len(array)) # varint
        for v in array:
            self.putInt(v) #varint
