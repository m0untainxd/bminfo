# bminfo

This app is for getting information from the osu!api and displaying beatmap info and performance point values.  The information can be taken by either directly inputting the beatmapID or by searching for the difficulty by inputting the beatmapsetID.

This program is going to be solely coded in Python.

Note: This app can only be used for std beatmaps (as of now)

# beatmap section

The information that will be shown is the beatmap name, artist, mapper name, diff name (if applies), list of diffs in beatmapset, beatmapid, beatmapsetid, beatmap values (ie, ar, cs, od, hp).  There will also be a section for calculating pp values for the beatmap.  The options that will be included will be mods used, accuracy and misses to gain an accurate calculation for the value.

also, the app will provide both the beatmap link and a link to downloading the beatmap with osu!direct (supp only).

In the future, I would like to figure out how to get real time information from the game using it's msn integration so real time performance point calculation is possible.  This could also be used so that the user does not have to search for the beatmap manually to see it's information

# pp section

The PP calculations will be solely handled by <a href="https://pypi.org/project/pyttanko/">pyttanko</a> which is a python implementation of the <a href="https://github.com/Francesco149/oppai-ng">oppai-ng</a> PP calculator.

# difficulty select section

If a beatmapsetID is input, another window will be opened showing a list of difficulty names with the name of the song, the artist and the mapper.  The user will select one of the difficulties and confirm.  From this, the beatmapID will be found, and then the information can be requested from the API.

# UI

The UI is built using Python <a href="https://docs.python.org/3/library/tkinter.html">tkinter</a>