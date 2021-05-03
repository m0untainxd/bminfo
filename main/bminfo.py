#coded by Andrew Radcliffe
#03/05/2021 v 1.00

#imports
import os
import json
import tkinter
import webbrowser
from dotenv import load_dotenv
from classes.search import Search
from classes.beatmap import Beatmap
from classes.performance import Performance

#define global variables
search = None
beatmap = None
performance = None

#functions
def mainloop():
    pass

def idsubmit():
    load_dotenv()
    BMINFO_KEY = os.getenv('BMINFO_KEY')

    global search
    search = Search(BMINFO_KEY)

    if mapID != 0:
        search.setmapID(mapID)
        map_data = search.api_mapID()

        for data in map_data:
            global beatmap
            beatmap = Beatmap(
                data["beatmap_id"], 
                data["beatmapset_id"],
                data["title"], 
                data["artist"],
                data["version"],
                data["creator"],
                data["diff_approach"],
                data["diff_size"],
                data["diff_overall"],
                data["diff_drain"],
                data["difficultyrating"],
                data["hit_length"],
                data["bpm"]
            )
    
    elif mapsetID != 0:
        search.setmapsetID(mapsetID)
        diff_list = search.api_mapsetID()
        #tkinter here
    return

def ppsubmit(acc, combo, misses, mods):
    global performance
    peformance = Performance(acc, combo, misses, mods)
    performance.pyttanko(beatmap.getmapID())
    #display pp value with tkinter
    return

def setmods():
    pass

def displayinfo():
    pass

def maplink():
    link = "https://osu.ppy.sh/beatmapsets/" + str(beatmap.getmapsetID()) + "#osu/" + str(beatmap.getmapID())
    webbrowser.open(link, new=2, autoraise=True)
    return

def mapdirect():
    link = "osu://b/" + str(beatmap.getmapID())
    webbrowser.open(link, new=2, autoraise=False)
    return