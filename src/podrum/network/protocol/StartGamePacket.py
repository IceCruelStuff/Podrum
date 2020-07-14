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
        # https://github.com/pmmp/PocketMine-MP/blob/stable/src/pocketmine/network/mcpe/protocol/StartGamePacket.php#L197
