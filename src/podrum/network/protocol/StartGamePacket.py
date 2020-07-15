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

# from podrum.nbt.tag.ListTag import ListTag
# from podrum.nbt.NetworkLittleEndianNBTStream import NetworkLittleEndianNBTStream
from podrum.network.protocol.types.EducationEditionOffer import EducationEditionOffer
from podrum.network.protocol.types.GameRuleType import GameRuleType
from podrum.network.protocol.types.GeneratorType import GeneratorType
from podrum.network.protocol.types.MultiplayerGameVisibility import MultiplayerGameVisibility
from podrum.network.protocol.types.PlayerPermissions import PlayerPermissions
from podrum.network.protocol.types.SpawnSettings import SpawnSettings
from podrum.network.protocol.DataPacket import DataPacket
from podrum.network.protocol.ProtocolInfo import ProtocolInfo

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

        # blockTable = (NetworkLittleEndianNBTStream().read(self.buffer, False, self.offset, 512))
        # if blockTable isinstance ListTag:
        #     raise ValueError("Wrong block table root NBT tag type")
        # self.blockTable = blockTable

        self.itemTable = []
        count = self.getUnsignedVarInt()
        for i in range(0, count):
            id = self.getString()
            legacyId = self.getSignedLShort()

            # self.itemTables[id] = legacyId

        self.multiplayerCorrelationId = self.getString()
        self.enableNewInventorySystem = self.getBool()

    def encodePayload(self):
        self.putEntityUniqueId(self.entityUniqueId)
        self.putEntityRuntimeId(self.entityRuntimeId)
        self.putVarInt(self.playerGamemode)

        self.putVector3(self.playerPosition)

        self.putLFloat(self.pitch)
        # https://github.com/pmmp/PocketMine-MP/blob/stable/src/pocketmine/network/mcpe/protocol/StartGamePacket.php#L269
