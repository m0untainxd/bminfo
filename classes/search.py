#coded by Andrew Radcliffe
#27/04/2021 V1.0

import requests

class Search:

    def __init__(self, key):
        self.beatmapID = 0
        self.beatmapsetID = 0
        self.api_key = key

    #set functions

    def setmapID(self, id):
        self.beatmapID = id

    def setmapsetID(self, id):
        self.beatmapsetID = id

    #get functions

    def getmapID(self):
        return self.beatmapID

    def getmapsetID(self):
        return self.beatmapsetID

    #special functions

    def api(self):
        parameters = {
            "k": self.api_key,
            "b": self.beatmapID
        }

        response = requests.get('https://osu.ppy.sh/api/get_beatmaps', params=parameters)
        return response.json()

    def database(self):
        pass