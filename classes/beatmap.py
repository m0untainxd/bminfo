#coded by Andrew Radcliffe
#29/04/2021 v1.00

class Beatmap:
    
    def __init__(self): #initialise the class and define variables
        self.beatmapID = 0
        self.title = ""
        self.artist = ""
        self.version = ""
        self.creator = ""
        self.ar = 0.0
        self.cs = 0.0
        self.od = 0.0
        self.hp = 0.0
        self.stars = 0.00
        self.length = 0
        self.bpm = 0

    #set functions

    def setmapID(self, beatmapID):
        self.beatmapID = beatmapID
        return
    
    def settitle(self, title):
        self.title = title
        return

    def setartist(self, artist):
        self.artist = artist
        return

    def setversion(self, diffname):
        self.version = diffname
        return

    def setcreator(self, mapper):
        self.creator = mapper
        return

    def setar(self, ar):
        self.ar = ar
        return

    def setcs(self, cs):
        self.cs = cs
        return

    def setod(self, od):
        self.od = od
        return

    def sethp(self, hp):
        self.hp = hp
        return

    def setstars(self, stars):
        self.stars = stars
        return

    def setlength(self, length):
        self.length = length
        return

    def setbpm(self, bpm):
        self.bpm = bpm
        return

    #get methods

    def getmapID(self):
        return self.beatmapID

    def gettitle(self):
        return self.title

    def getartist(self):
        return self.artist

    def getversion(self):
        return self.version

    def getcreator(self):
        return self.creator

    def getar(self):
        return self.ar

    def getcs(self):
        return self.cs

    def getod(self):
        return self.od
    
    def gethp(self):
        return self.hp

    def getstars(self):
        return self.stars

    def getlength(self):
        return self.length

    def getbpm(self):
        return self.bpm