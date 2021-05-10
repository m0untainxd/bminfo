#coded by Andrew Radcliffe
#30/04/2021 v1.00

import os
import sys
import modules.pyttanko

class Performance:

    def __init__(self, acc, combo, misses):
        self.accuracy = acc
        self.maxcombo = combo
        self.misses = misses
        self.mods = ""
        self.pp = 0

    #set methods

    def setacc(self, acc):
        self.accuracy = acc
        return
    
    def setcombo(self, combo):
        self.maxcombo = combo
        return

    def setmisses(self, misses):
        self.misses = misses
        return

    def setmods(self, mods):
        if self.mods != "":
            self.mods = mods
        else:
            self.mods = "+" + mods

    def setpp(self, pp):
        self.pp = pp

    #get methods

    def getacc(self):
        return self.accuracy

    def getcombo(self):
        return self.maxcombo

    def getmisses(self):
        return self.misses

    def getpp(self):
        return self.pp

    #special methods

    def pyttanko(self, mapID):
        cmd = "curl https://osu.ppy.sh/osu/" + str(mapID) + " | .\main\pyttanko.py +" + self.mods + " " + str(self.maxcombo) + "x " + str(self.misses) + "m " + str(self.accuracy) + "%"
        run = os.popen(cmd)
        result = run.read()

        start = result.find('threshold\n') + 10
        end = result.find('.', start)
        self.pp = result[start:end]
        return