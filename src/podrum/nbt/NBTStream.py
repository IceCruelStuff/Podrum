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

from abc import ABCMeta, abstractmethod

class NBTStream:
    __metaclass__ = ABCMeta

    buffer = ""
    offset = 0

    def get(self, len):
        if len == 0:
            return ""

        buflen = len(self.buffer)
        if len == True:
            str = self.buffer[:self.buffer]
            self.offset = buflen
            return str
        if len < 0:
            self.offset = buflen - 1
            return ""
        remaining = buflen - self.offset
        if remaining < len:
            raise Exception("Not enough bytes left in buffer: need {}, have {}".format(len, remaining))

        return self.buffer[self.offset += 1] if len == 1 else self.buffer[(self.offset += len) - len:len]

    def put(self, v):
        self.buffer += v

    def feof(self):
        #try:
        #    self.buffer[self.offset]
        #except NameError:
        #    return ()
        # https://github.com/pmmp/NBT/blob/stable/src/NBTStream.php#L94
