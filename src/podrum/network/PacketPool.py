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

from copy import deepcopy

from binutilspy.Binary import Binary
from podrum.network.protocol.AdventureSettingsPacket import AdventureSettingsPacket
from podrum.network.protocol.ClientToServerHandshakePacket import ClientToServerHandshakePacket
from podrum.network.protocol.DataPacket import DataPacket
from podrum.network.protocol.DisconnectPacket import DisconnectPacket
from podrum.network.protocol.LoginPacket import LoginPacket
from podrum.network.protocol.PlayStatusPacket import PlayStatusPacket
from podrum.network.protocol.ResourcePacksInfoPacket import ResourcePacksInfoPacket
from podrum.network.protocol.ServerToClientHandshakePacket import ServerToClientHandshakePacket
from podrum.network.protocol.UnknownPacket import UnknownPacket

class PacketPool:
    packetPool = {}
    
    def __init__(self):
        self.registerPackets()
        
    def registerPacket(packet: DataPacket):
        self.pool[packet.NID] = deepcopy(packet)
        
    def registerPackets(self):
        self.registerPacket(AdventureSettingsPacket())
        self.registerPacket(ClientToServerHandshakePacket())
        self.registerPacket(DisconnectPacket())
        self.registerPacket(LoginPacket())
        self.registerPacket(PlayStatusPacket())
        self.registerPacket(ResourcePacksInfoPacket())
        self.registerPacket(ServerToClientHandshakePacket())
        
    def getPacketById(self, pid: int) -> DataPacket:
        try:
            self.pool[pid]
        except:
            return UnknownPacket()
        else:
            return deepcopy(self.pool[pid])
        
    def getPacket(self, buffer: bytes) -> DataPacket:
        offset = 0
        pk = self.getPacketById(Binary.readUnsignedVarInt(buffer, offset) & DataPacket.PID_MASK)
        pk.setBuffer(buffer, offset)
        return pk
