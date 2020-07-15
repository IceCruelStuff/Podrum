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

import json
import os

#from podrum.nbt.tag.ListTag import ListTag
#from podrum.nbt.NetworkLittleEndianNBTStream import NetworkLittleEndianNBTStream
#from podrum.network.convert.RuntimeBlockMapping import RuntimeBlockMapping
from podrum.network.protocol.types.EducationEditionOffer import EducationEditionOffer
from podrum.network.protocol.types.GameRuleType import GameRuleType
from podrum.network.protocol.types.GeneratorType import GeneratorType
from podrum.network.protocol.types.MultiplayerGameVisibility import MultiplayerGameVisibility
from podrum.network.protocol.types.PlayerPermissions import PlayerPermissions
from podrum.network.protocol.types.SpawnSettings import SpawnSettings
from podrum.network.protocol.DataPacket import DataPacket
from podrum.network.protocol.ProtocolInfo import ProtocolInfo
from podrum.network.NetBinaryStream import NetBinaryStream
from podrum.utils.ServerFS import ServerFS

class StartGamePacket(DataPacket):
    NID = ProtocolInfo.START_GAME_PACKET

    blockTableCache = None
    itemTableCache = None
    entityUniqueId = None
    entityRuntimeId = None
    playerGamemode = None
    playerPosition = None
    pitch = None
    yaw = None
    seed = None
    spawnSettings = None
    generator = GeneratorType.OVERWORLD
    worldGamemode = None
    difficulty = None
    spawnX = None
    spawnY = None
    spawnZ = None
    hasAchievementsDisabled = True
    time = -1
    eduEditionOffer = EducationEditionOffer.NONE
    hasEduFeaturesEnabled = False
    eduProductUUID = ""
    rainLevel = None
    lightningLevel = None
    hasConfirmedPlatformLockedContent = False
    isMultiplayerGame = True
    hasLANBroadcast = True
    xboxLiveBroadcastMode = MultiplayerGameVisibility.PUBLIC
    platformBroadcastMode = MultiplayerGameVisibility.PUBLIC
    commandsEnabled = None
    isTexturePacksRequired = True
    gameRules = {
        "naturalregeneration": {
            GameRuleType.BOOL, false
        }
    }
    hasBonusChestEnabled = False
    hasStartWithMapEnabled = False
    defaultPlayerPermission = PlayerPermissions.MEMBER
    serverChunkTickRadius = 4
    hasLockedBehaviorPack = False
    hasLockedResourcePack = False
    isFromLockedWorldTemplate = False
    useMsaGamertagsOnly = False
    isFromWorldTemplate = False
    isWorldTemplateOptionLocked = False
    onlySpawnV1Villagers = False
    vanillaVersion = ProtocolInfo.MCBE_VERSION_NETWORK
    limitedWorldWidth = 0
    limitedWorldLength = 0
    isNewNether = True
    experimentalGameplayOverride = None
    levelId = ""
    worldName = None
    premiumWorldTemplateId = ""
    isTrial = False
    isMovementServerAuthoritative = False
    currentTick = 0
    enchantmentSeed = 0
    multiplayerCorrelationId = ""
    blockTable = None
    itemTable = None
    enableNewInventorySystem = False

    def decodePayload(self):
        self.entityUniqueId = self.getEntityUniqueId()
        self.entityRuntimeId = self.getEntityRuntimeId()
        self.playerGamemode = self.getVarInt()

        self.playerPosition = self.getVector3()

        self.pitch = self.getLFloat()
        self.yaw = self.getLFloat()

        # level settings
        self.seed = self.getVarInt()
        self.spawnSettings = SpawnSettings.read(self)
        self.generator = self.getVarInt()
        self.worldGamemode = self.getVarInt()
        self.difficulty = self.getVarInt()
        self.getBlockPosition(self.spawnX, self.spawnY, self.spawnZ)
        self.hasAchievementsDisabled = self.getBool()
        self.time = self.getVarInt()
        self.eduEditionOffer = self.getVarInt()
        self.hasEduFeaturesEnabled = self.getBool()
        self.eduProductUUID = self.getString()
        self.rainLevel = self.getLFloat()
        self.lightningLevel = self.getLFloat()
        self.hasConfirmedPlatformLockedContent = self.getBool()
        self.isMultiplayerGame = self.getBool()
        self.hasLANBroadcast = self.getBool()
        self.xboxLiveBroadcastMode = self.getVarInt()
        self.platformBroadcastMode = self.getVarInt()
        self.commandsEnabled = self.getBool()
        self.isTexturePacksRequired = self.getBool()
        self.gameRules = self.getGameRules()
        self.hasBonusChestEnabled = self.getBool()
        self.hasStartWithMapEnabled = self.getBool()
        self.defaultPlayerPermission = self.getVarInt()
        self.serverChunkTickRadius = self.getLInt()
        self.hasLockedBehaviorPack = self.getBool()
        self.hasLockedResourcePack = self.getBool()
        self.isFromLockedWorldTemplate = self.getBool()
        self.useMsaGamertagsOnly = self.getBool()
        self.isFromWorldTemplate = self.getBool()
        self.isWorldTemplateOptionLocked = self.getBool()
        self.onlySpawnV1Villagers = self.getBool()
        self.vanillaVersion = self.getString()
        self.limitedWorldWidth = self.getLInt()
        self.limitedWorldLength = self.getLInt()
        self.isNewNether = self.getBool()
        if self.getBool():
            self.experimentalGameplayOverride = self.getBool()
        else:
            self.experimentalGameplayOverride = None

        self.levelId = self.getString()
        self.worldName = self.getString()
        self.premiumWorldTemplateId = self.getString()
        self.isTrial = self.getBool()
        self.isMovementServerAuthoritative = self.getBool()
        self.currentTick = self.getLLong()

        self.enchantmentSeed = self.getVarInt()

        #blockTable = (NetworkLittleEndianNBTStream().read(self.buffer, False, self.offset, 512))
        #if isinstance(blockTable, ListTag):
        #    raise ValueError("Wrong block table root NBT tag type")
        #self.blockTable = blockTable

        self.itemTable = []
        count = self.getUnsignedVarInt()
        for i in range(0, count):
            id = self.getString()
            legacyId = self.getSignedLShort()

            #self.itemTables[id] = legacyId

        self.multiplayerCorrelationId = self.getString()
        self.enableNewInventorySystem = self.getBool()

    def encodePayload(self):
        self.putEntityUniqueId(self.entityUniqueId)
        self.putEntityRuntimeId(self.entityRuntimeId)
        self.putVarInt(self.playerGamemode)

        self.putVector3(self.playerPosition)

        self.putLFloat(self.pitch)
        self.putLFloat(self.yaw)

        # level settings
        self.putVarInt(self.seed)
        self.spawnSettings.write(self)
        self.putVarInt(self.generator)
        self.putVarInt(self.worldGamemode)
        self.putVarInt(self.difficulty)
        self.putBlockPosition(self.spawnX, self.spawnY, self.spawnZ)
        self.putBool(self.hasAchievementsDisabled)
        self.putVarInt(self.time)
        self.putVarInt(self.eduEditionOffer)
        self.putBool(self.hasEduFeaturesEnabled)
        self.putString(self.eduProductUUID)
        self.putLFloat(self.rainLevel)
        self.putLFloat(self.lightningLevel)
        self.putBool(self.hasConfirmedPlatformLockedContent)
        self.putBool(self.isMultiplayerGame)
        self.putBool(self.hasLANBroadcast)
        self.putVarInt(self.xboxLiveBroadcastMode)
        self.putVarInt(self.platformBroadcastMode)
        self.putBool(self.commandsEnabled)
        self.putBool(self.isTexturePacksRequired)
        self.putGameRules(self.gameRules)
        self.putBool(self.hasBonusChestEnabled)
        self.putBool(self.hasStartWithMapEnabled)
        self.putVarInt(self.defaultPlayerPermission)
        self.putLInt(self.serverChunkTickRadius)
        self.putBool(self.hasLockedBehaviorPack)
        self.putBool(self.hasLockedResourcePack)
        self.putBool(self.isFromLockedWorldTemplate)
        self.putBool(self.useMsaGamertagsOnly)
        self.putBool(self.isFromWorldTemplate)
        self.putBool(self.isWorldTemplateOptionLocked)
        self.putBool(self.onlySpawnV1Villagers)
        self.putString(self.vanillaVersion)
        self.putLInt(self.limitedWorldWidth)
        self.putLInt(self.limitedWorldLength)
        self.putBool(self.isNewNether)
        self.putBool(self.experimentalGameplayOverride != None)
        if self.experimentalGameplayOverride != None:
            self.putBool(self.experimentalGameplayOverride)

        self.putString(self.levelId)
        self.putString(self.worldName)
        self.putString(self.premiumWorldTemplateId)
        self.putBool(self.isTrial)
        self.putBool(self.isMovementServerAuthoritative)
        self.putLLong(self.currentTick)

        self.putVarInt(self.enchantmentSeed)

        #if self.blockTable == None:
        #    if self.blockTableCache = None:
        #        self.blockTableCache = NetworkLittleEndianNBTStream().write(ListTag("", RuntimeBlockMapping.getBedrockKnownStates()))
        #    self.put(self.blockTableCache)
        #else:
        #    self.put(NetworkLittleEndianNBTStream().write(self.blockTable))

        #if self.itemTable = None:
        #    if self.itemTableCache = None:
        #        path = 'podrum/resources/vanilla'
        #        self.itemTableCache = self.serializeItemTable(json.loads(ServerFS.checkForFile(path, '/item_id_map.json')))
        #    self.put(self.itemTableCache)
        #else:
        #    self.put(self.serializeItemTable(self.itemTable))

        self.putString(self.multiplayerCorrelationId)
        self.putBool(self.enableNewInventorySystem)

    def serializeItemTable(self, table):
        stream = NetBinaryStream()
        stream.putUnsignedVarInt(len(table))
        for name, legacyId in table:
            stream.putString(name)
            stream.putLShort(legacyId)
        return stream.getBuffer()
