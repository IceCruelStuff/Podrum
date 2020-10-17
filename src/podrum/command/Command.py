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

class Command:
    name = None
    description = None

    def __init__(self, name = "", description = ""):
        self.name = name
        self.description = description

    def execute(self, sender, args):
        pass

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description