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

from podrum.command.Command import Command
from podrum.Player import Player

class OpCommand(Command):
    def __init__(self, name = "", description = ""):
        super().__init__("op", "Op Command")

    def execute(self, sender, args):
        try:
            args[1]
            try:
                name = args.pop(0)
                Player.isValidUserName(name)
            except:
                sender.sendMessage("op <player>")
        except:
            sender.sendMessage("op <player>")
        else:
            sender.sendMessage(" ".join(args[1:]))
