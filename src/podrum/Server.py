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

import time
import os

from podrum.lang.Base import Base
from podrum.network.PacketPool import PacketPool as Pool
from podrum.network.QueryHandler import QueryHandler
from podrum.network.NetworkInterface import NetworkInterface
from podrum.Player import Player
from podrum.plugin.PluginLoader import PluginLoader
from podrum.utils.Logger import Logger
from podrum.utils.ServerFS import ServerFS
from podrum.utils.Utils import Utils
from podrum.wizard.Wizard import Wizard

class Server:

    path = None
    withWizard = None
    operators = None
    addr = "0.0.0.0"
    port = 19132
    players = []
    queryHandler = None
    mainInterface = None
    podrumLogo = """
            ____           _                      
           |  _ \ ___   __| |_ __ _   _ _ __ ___  
           | |_) / _ \ / _` | '__| | | | '_ ` _ \ 
           |  __/ (_) | (_| | |  | |_| | | | | | |
           |_|   \___/ \__,_|_|   \__,_|_| |_| |_|
    """

    def __init__(self, path, withWizard, isTravisBuild = False):
        super().__init__()
        startTime = Utils.microtime(True)
        self.path = path
        self.withWizard = withWizard
        self.tickrate = 20/1000
        if(withWizard):
            ServerFS.checkAllFiles(path)
        else:
            Wizard.skipWizard(path, True)
        print(str(self.podrumLogo))
        Wizard.isInWizard = False
        Logger.log('info',  str(Base.get("startingServer")).replace("{ip}", str(Utils.getPrivateIpAddress())).replace("{port}", str(self.port)))
        Logger.log('info', str(Base.get("extIpMsg")).replace("{ipPublic}", str(Utils.getPublicIpAddress())))
        Logger.log('info', str(Base.get("license")))
        PluginLoader.loadAll()
        doneTime = Utils.microtime(True)
        self.queryHandler = QueryHandler(self)
        self.mainInterface = NetworkInterface(self)
        self.mainInterface.process()
        finishStartupSeconds = "%.3f" % (doneTime - startTime)
        Logger.log('info', f'Done in {str(finishStartupSeconds)}s. Type "help" to view all available commands.')
        if (isTravisBuild):
            Server.checkTravisBuild(path)
        else:
            while Wizard.isInWizard == False:
                cmd = input('> ')
                Server.command(cmd, True)
                cmd = None
            ticking = True
            while ticking:
                time.sleep(self.tickrate)
                
    def getLogger(self):
        return Logger()
    
    def getAddress(self):
        return self.addr
    
    def getPort(self):
        return self.port
    
    def addPlayer(self, identifier, player):
        self.players.insert(identifier, player)
        
    def handlePacket(self, interface, address, port, payload):
        if len(payload) > 2 and payload[0:2] == b"\xfe\xfd" and isinstance(self.queryHandler, QueryHandler(self)):
            self.queryHandler.handle(interface, address, port, payload)

    @staticmethod
    def command(string, fromConsole):
        if string.lower() == 'stop':
            Logger.log('info', 'Stopping server...')
            PluginLoader.unloadAll()
            Logger.log('info', 'Server stopped.')
            Utils.killServer()
        elif string.lower() == '':
            return
        elif string.lower() == 'help':
            Logger.log('info', '/stop: Stops the server')
        elif string.lower() == 'reload':
            PluginLoader.reloadAll()
            Logger.log('info', 'Reload successful!')
        elif string.lower() == 'plugins' or string.lower() == 'pl':
            pluginsString = ""
            for pluginName in PluginLoader.loadedPluginsList:
                pluginsString = pluginsString + pluginName
                if pluginName != PluginLoader.loadedPluginsList[PluginLoader.loadedPluginsCount - 1]:
                    pluginsString += ", "
            Logger.log('info', f'Plugins({PluginLoader.loadedPluginsCount}): {pluginsString}')
        else:
            Logger.log('error', str(Base.get("invalidCommand")))
    
    def checkTravisBuild(path):
        if not ServerFS.checkForFile(path, "server.json"):
            Logger.log("error", "Couldn't find server.json file.")
            os._exit(1)
        if os.path.getsize(f'{path}/server.json') == 0:
            Logger.log("error", "The server.json file is empty.")
            os._exit(1)
        print("Build success.")
        os._exit(0)

    def isOp(self, name):
        return self.operators.exists(name, True)

    def getOps(self):
        return self.operators
