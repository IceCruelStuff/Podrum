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

from podrum.network.NetBinaryStream import NetBinaryStream

class SpawnSettings:
    BIOME_TYPE_DEFAULT = 0
    BIOME_TYPE_USER_DEFINED = 1

    biomeType = None
    biomeName = None
    dimension = None

    def __init__(self, biomeType, biomeName, dimension):
        self.biomeType = biomeType
        self.biomeName = biomeName
        self.dimension = dimension

    def getBiomeType(self):
        return self.biomeType

    def getBiomeName(self):
        return self.biomeName

    def getDimension(self):
        return self.dimension

    @staticmethod
    def read(self, in):
        in = NetBinaryStream()
        biomeType = in.getLShort()
        biomeName = in.getString()
        dimension = in.getVarInt()

        return self(biomeType, biomeName, dimension)

    def write(self, out):
        out = NetBinaryStream()
        out.putLShort(self.biomeType)
        out.putString(self.biomeName)
        out.putVarInt(self.dimension)
