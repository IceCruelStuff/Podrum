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

from podrum.nbt.tag.CompoundTag import CompoundTag

class R12ToCurrentBlockMapEntry:
    id = None
    meta = None
    blockState = None

    def __init__(self, id, meta, blockState):
        self.id = id
        self.meta = meta
        self.blockState = blockState

    def getId(self):
        return self.id

    def getMeta(self):
        return self.meta

    def getBlockState(self):
        return self.blockState

    def __toString(self):
        return f.'id={self.id}, meta={self.meta}, nbt={self.blockState}'
