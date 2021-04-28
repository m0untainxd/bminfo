#coded by Andrew Radcliffe
#27/04/2021 V1.0

import requests
import json

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

    def api_mapID(self):
        #sets parameters for connection to the api
        parameters = {
            "k": self.api_key, #required api key
            "b": self.beatmapID #ID for the map to be returned
        }

        raw = requests.get('https://osu.ppy.sh/api/get_beatmaps', params=parameters) #get data from the api
        response = raw.json()
        diff_data = json.dumps(response)
        data = json.loads(diff_data)

        return data

    def api_mapsetID(self):
        #params for connection to api
        parameters = {
            "k": self.api_key, #required api key
            "s": self.beatmapsetID,
            "m": 0
        }

        raw = requests.get('https://osu.ppy.sh/api/get_beatmaps', params=parameters) #get data from the api
        response = raw.json()
        into_list = json.dumps(response)
        diff_list = json.loads(into_list)

        return diff_list
        