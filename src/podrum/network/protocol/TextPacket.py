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

class TextPacket(DataPacket):
    NID = ProtocolInfo.TEXT_PACKET

    TYPE_RAW = 0
    TYPE_CHAT = 1
    TYPE_TRANSLATION = 2
    TYPE_POPUP = 3
    TYPE_JUKEBOX_POPUP = 4
    TYPE_TIP = 5
    TYPE_SYSTEM = 6
    TYPE_WHISPER = 7
    TYPE_ANNOUNCEMENT = 8
    TYPE_JSON_WHISPER = 9
    TYPE_JSON = 10

    type = None
    needsTranslation = False
    sourceName = None
    message = None
    parameters = []
    xboxUserId = ""
    platformChatId = ""

    def decodePayload(self):
        self.type = self.getByte()
        self.needsTranslation = self.getBool()
        if self.type == self.TYPE_CHAT or self.type == self.TYPE_WHISPER or self.type == self.TYPE_ANNOUNCEMENT:
            self.sourceName = self.getString()
        elif self.type == self.TYPE_RAW or self.type == self.TYPE_TIP or self.type == self.TYPE_SYSTEM or self.type == self.TYPE_JSON_WHISPER or self.type == self.TYPE_JSON:
            self.message = self.getString()
        elif self.type == self.TYPE_TRANSLATION or self.type == self.TYPE_POPUP or self.type == self.TYPE_JUKEBOX_POPUP:
            self.message = self.getString()
            count = self.getUnsignedVarInt()
            for i in range(0, count):
                self.parameters[None] = self.getString()

        self.xboxUserId = self.getString()
        self.platformChatId = self.getString()

    def encodePayload(self):
        self.putByte(self.type)
        self.putBool(self.needsTranslation)
        if self.type == self.TYPE_CHAT or self.type == self.TYPE_WHISPER or self.type == self.TYPE_ANNOUNCEMENT:
            self.putString(self.sourceName)
        elif self.type == self.TYPE_RAW or self.type == self.TYPE_TIP or self.type == self.TYPE_SYSTEM or self.type == self.TYPE_JSON_WHISPER or self.type == self.TYPE_JSON:
            self.putString(self.message)
        elif self.type == self.TYPE_TRANSLATION or self.type == self.TYPE_POPUP or self.type == self.TYPE_JUKEBOX_POPUP:
            self.putString(self.message)
            self.putUnsignedVarInt(len(self.parameters))
            for p in self.parameters:
                self.putString(p)

        self.putString(self.xboxUserId)
        self.putString(self.platformChatId)
