  
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

from podrum.network.protocol.DataPacket import DataPacket
from podrum.network.protocol.ProtocolInfo import ProtocolInfo

class ResourcePackStackPacket(DataPacket):
    NID = ProtocolInfo.RESOURCE_PACK_STACK_PACKET

    mustAccept = False
    behaviorPackStack = []
    resourcePackStack = []
    isExperimental = False
    baseGameVersion = ProtocolInfo.MCBE_VERSION_NETWORK

    def decodePayload(self):
        self.mustAccept = self.getBool()
        behaviorPackCount = self.getUnsignedVarInt()
        while behaviorPackCount > 0:
            self.getString()
            self.getString()
            self.getString()

        resourcePackCount = self.getUnsignedVarInt()
        while resourcePackCount > 0:
            self.getString()
            self.getString()
            self.getString()

        self.isExperimental = self.getBool()
        self.baseGameVersion = self.getString()

    def encodePayload(self):
        self.putBool(self.mustAccept)

        self.putUnsignedVarInt(len(self.behaviorPackStack))
        for entry in self.behaviorPackStack:
            self.putString(entry.getPackId())
            self.putString(entry.getPackVersion())
            self.putString("") # TODO: subpack name

        self.putUnsignedVarInt(len(self.resourcePackStack))
        for entry in self.resourcePackStack:
            self.putString(entry.getPackId())
            self.putString(entry.getPackVersion())
            self.putString("") # TODO: subpack name

        self.putBool(self.isExperimental)
        self.putString(self.baseGameVersion)
