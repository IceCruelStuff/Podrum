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

class ResourcePackClientResponsePacket(DataPacket):
    PID = ProtocolInfo.RESOURCE_PACK_CLIENT_RESPONSE_PACKET

    STATUS_REFUSED = 1
    STATUS_SEND_PACKS = 2
    STATUS_HAVE_ALL_PACKS = 3
    STATUS_COMPLETED = 4

    status = None
    packIds = []

    def decodePayload(self):
        self.status = self.getByte()
        entryCount = self.getLShort()
        while entryCount > 0:
            self.packIds[] = self.getString()
            entryCount -= 1

    def encodePayload(self):
        self.putByte(self.status)
        self.putLShort(len(self.packIds))
        for id in self.packIds:
            self.putString(id)
