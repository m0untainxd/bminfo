#coded by Andrew Radcliffe
#03/05/2021 v 1.00

#imports
import os, json, tkinter, webbrowser, urllib, io, operator
from tkinter import messagebox
from dotenv import load_dotenv
from PIL import ImageTk, Image
from classes.search import Search
from classes.beatmap import Beatmap
from classes.performance import Performance

#define global variables
search = None
beatmap = None
performance = None

#get id window
class IdGet:
    def __init__(self, master):
        self.master = master
        self.master.title("bminfo.exe (idget)")
        self.master.columnconfigure(0, minsize=350)
        self.master.rowconfigure(0, minsize=100)
        ent_val = 0

        #beatmapid section
        self.bmid_frame = tkinter.Frame(master=self.master)
        self.bmid_frame.grid(row=0, column=0)
        self.bmid_label = tkinter.Label(master=self.bmid_frame, text="Enter beatmapID")
        self.bmid_label.pack()
        self.bmid_ent = tkinter.Entry(master=self.bmid_frame)
        self.bmid_ent.insert(0, ent_val)
        self.bmid_ent.pack()

        #beatmapsetid section
        self.master.columnconfigure(1, minsize=350)
        self.master.rowconfigure(0, minsize=100)
        self.bmsid_frame = tkinter.Frame(master=self.master)
        self.bmsid_frame.grid(row=0, column=1)
        self.bmsid_label = tkinter.Label(master=self.bmsid_frame, text="Enter beatmapsetID")
        self.bmsid_label.pack()
        self.bmsid_ent = tkinter.Entry(master=self.bmsid_frame)
        self.bmsid_ent.insert(0, ent_val)
        self.bmsid_ent.pack()

        #or text inbetween bmid and bmsid
        self.or_label = tkinter.Label(master=self.master, text="or")
        self.or_label.place(x=340, y=29)

        #id submit button
        self.bmid_submit = tkinter.Button(
            text="Submit",
            command=self.idsubmit,
        )
        self.bmid_submit.place(x=325, y=75)
    
    def idsubmit(self):

        try:
            self.mapID = int(self.bmid_ent.get())
            self.mapsetID = int(self.bmsid_ent.get())
        except ValueError:
            messagebox.showerror(title="Error", message="ValueError: must enter a number. Please try again.")
            return

        load_dotenv()
        self.BMINFO_KEY = os.getenv('BMINFO_KEY')

        global search
        search = Search(self.BMINFO_KEY)

        if self.mapID != 0 and self.mapsetID == 0:
            search.setmapID(self.mapID)
            map_data = search.api_mapID()

            if map_data == []:
                messagebox.showerror(title="Error", message="BeatmapID not found, please try again.")
                return
            else:
                pass

            for data in map_data:
                global beatmap
                beatmap = Beatmap(
                    data["beatmap_id"], 
                    data["beatmapset_id"],
                    data["title"], 
                    data["artist"],
                    data["version"],
                    data["creator"],
                    float(data["diff_approach"]),
                    float(data["diff_size"]),
                    float(data["diff_overall"]),
                    float(data["diff_drain"]),
                    float(data["difficultyrating"]),
                    int(data["hit_length"]),
                    int(data["bpm"])
                )

            self.mainwindow()
    
        elif self.mapsetID != 0 and self.mapID == 0:
            search.setmapsetID(self.mapsetID)
            diffs = search.api_mapsetID()

            if diffs == []:
                messagebox.showerror(title="Error", message="BeatmapsetID not found, please try again.")
                return
            else:
                pass

            self.diff_list = sorted(diffs, key=operator.itemgetter('difficultyrating'))
            self.diff_names = []
            self.song_title = self.diff_list[0]["title"]
            self.song_artist = self.diff_list[0]["artist"]
            self.song_mapper = self.diff_list[0]["creator"]

            for diff in self.diff_list:
                self.diff_names.append(diff["version"])
            
            self.diffwindow()

        elif self.mapID != 0 and self.mapsetID != 0:
            msg = messagebox.askyesnocancel(title="Message", message="Both values entered. BeatmapID will be used. Do you wish to continue?")
            if msg == True:
                search.setmapID(self.mapID)
                map_data = search.api_mapID()

                for data in map_data:
                    beatmap = Beatmap(
                        int(data["beatmap_id"]), 
                        int(data["beatmapset_id"]),
                        data["title"], 
                        data["artist"],
                        data["version"],
                        data["creator"],
                        float(data["diff_approach"]),
                        float(data["diff_size"]),
                        float(data["diff_overall"]),
                        float(data["diff_drain"]),
                        float(data["difficultyrating"]),
                        int(data["hit_length"]),
                        int(data["bpm"])
                    )

                self.mainwindow()
            else:
                pass
        
        else:
            messagebox.showerror(title="Error", message="No value entered, please try again.")
        
        return

    def mainwindow(self):
        self.newWindow = tkinter.Toplevel(self.master)
        self.app = Main(self.newWindow)
        try:
            self.master.withdraw()
        except AttributeError:
            pass

        return
    
    def diffwindow(self):
        self.newWindow = tkinter.Toplevel(self.master)
        self.app = Diff(self.newWindow, self.song_title, self.song_artist, self.song_mapper, self.diff_names, self.diff_list)
        self.master.withdraw()

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("bminfo.exe (main)")
        self.master.rowconfigure(0, minsize=200)
        self.master.columnconfigure(0, minsize=350)
        self.image_frame = tkinter.Frame(master=self.master)
        self.image_frame.grid(row=0, column=0)
        
        #image section
        path = "https://assets.ppy.sh/beatmaps/" + str(beatmap.getmapsetID()) + "/covers/cover.jpg"
        im = urllib.request.urlopen(path).read()
        img = Image.open(io.BytesIO(im))
        img = img.resize((350, 97), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img)
        self.image_label = tkinter.Label(master=self.image_frame, image=image)
        self.image_label.image = image
        self.image_label.pack()

        #beatmap link section
        self.bmlink_button = tkinter.Button(
            master=self.master,
            text="Link to beatmap page",
            command=self.maplink,
            width=21
        )
        self.bmlink_button.place(x=5, y=160)

        #osu direct link section
        self.osudirect_link = tkinter.Button(
            master=self.master,
            text="osu!direct (supporter only)",
            command=self.mapdirect
        )
        self.osudirect_link.place(x=195, y=160)

        #mods section
        self.master.columnconfigure(1, minsize=350)
        self.mods_frame = tkinter.Frame(master=self.master)
        self.mods_frame.grid(row=0, column=1)
        self.mods_header = tkinter.Label(master=self.master, text="Mods")
        self.mods_header.place(x=515, y=50)

        #checkboxes
        self.ez = tkinter.IntVar()
        self.mods_ez_check = tkinter.Checkbutton(master=self.master, text="Easy", variable=self.ez)
        self.mods_ez_check.place(x=375, y=85)

        self.nf = tkinter.IntVar()
        self.mods_nf_check = tkinter.Checkbutton(master=self.master, text="NoFail", variable=self.nf)
        self.mods_nf_check.place(x=430, y=85)

        self.ht = tkinter.IntVar()
        self.mods_ht_check = tkinter.Checkbutton(master=self.master, text="HalfTime", variable=self.ht)
        self.mods_ht_check.place(x=498, y=85)

        self.hr = tkinter.IntVar()
        self.mods_hr_check = tkinter.Checkbutton(master=self.master, text="HardRock", variable=self.hr)
        self.mods_hr_check.place(x=375, y=115)

        self.dt = tkinter.IntVar()
        self.mods_dt_check = tkinter.Checkbutton(master=self.master, text="DoubleTime", variable=self.dt)
        self.mods_dt_check.place(x=460, y=115)

        self.hd = tkinter.IntVar()
        self.mods_hd_check = tkinter.Checkbutton(master=self.master, text="Hidden", variable=self.hd)
        self.mods_hd_check.place(x=555, y=115)

        self.fl = tkinter.IntVar()
        self.mods_fl_check = tkinter.Checkbutton(master=self.master, text="Flashlight", variable=self.fl)
        self.mods_fl_check.place(x=625, y=115)

        #map info section
        #title, artist, creator and difficulty
        self.master.rowconfigure(1, minsize=100)
        self.map_frame = tkinter.Frame(master=self.master)
        self.map_frame.grid(row=1, column=0)

        self.map_title_label = tkinter.Label(master=self.map_frame, text=beatmap.title)
        self.map_title_label.pack(side=tkinter.TOP)

        self.map_artist_label = tkinter.Label(master=self.map_frame, text=beatmap.artist)
        self.map_artist_label.pack(side=tkinter.TOP)

        self.map_creator_label = tkinter.Label(master=self.map_frame, text="Mapped by " + beatmap.creator)
        self.map_creator_label.pack(side=tkinter.TOP)

        self.map_version_label = tkinter.Label(master=self.map_frame, text="[" + beatmap.version + "]")
        self.map_version_label.pack(side=tkinter.TOP)

        #map metadata
        self.master.rowconfigure(2, minsize=100)
        self.metadata_frame = tkinter.Frame(master=self.master)
        self.metadata_frame.grid(row=2, column=0)

        self.ar_label = tkinter.Label(master=self.master, text="AR " + str(beatmap.getar()))
        self.ar_label.place(x=75, y=295)

        self.cs_label = tkinter.Label(master=self.master, text="CS " + str(beatmap.getcs()))
        self.cs_label.place(x=75, y=315)

        self.od_label = tkinter.Label(master=self.master, text="OD " + str(beatmap.getod()))
        self.od_label.place(x=75, y=335)

        self.hp_label = tkinter.Label(master=self.master, text="HP " + str(beatmap.gethp()))
        self.hp_label.place(x=75, y=355)

        self.stars_label = tkinter.Label(master=self.master, text="Stars " + str(beatmap.getstars()))
        self.stars_label.place(x=235, y=295)

        length = self.lengthconvert(beatmap.getlength())
        self.length_label = tkinter.Label(master=self.master, text="Length " + str(length))
        self.length_label.place(x=235, y=315)

        self.bpm_label = tkinter.Label(master=self.master, text="BPM " + str(beatmap.getbpm()))
        self.bpm_label.place(x=235, y=335)

        #pp section
        self.pp_header_label = tkinter.Label(master=self.master, text="PP Calculator")
        self.pp_header_label.place(x=495, y=207)

        self.pp_acc_label = tkinter.Label(master=self.master, text="Accuracy")
        self.pp_acc_label.place(x=430, y=237)
        self.pp_acc_ent = tkinter.Entry(master=self.master, width=10)
        self.pp_acc_ent.place(x=425, y=257)

        self.pp_combo_label = tkinter.Label(master=self.master, text="Max Combo")
        self.pp_combo_label.place(x=497, y=237)
        self.pp_combo_ent = tkinter.Entry(master=self.master, width=10)
        self.pp_combo_ent.place(x=500, y=257)

        self.pp_misses_label = tkinter.Label(master=self.master, text="Misses")
        self.pp_misses_label.place(x=587, y=237)
        self.pp_misses_ent = tkinter.Entry(master=self.master, width=10)
        self.pp_misses_ent.place(x=575, y=257)

        self.pp_submit_button = tkinter.Button(
            master=self.master,
            text="Submit",
            command=self.ppsubmit,
        )
        self.pp_submit_button.place(x=508, y=282)


        #buttons to get another map or exit the program
        self.idget_button = tkinter.Button(
            master=self.master,
            text="Get another map",
            command=self.goback
        )
        self.idget_button.place(x=515, y=370)

        self.exit_button = tkinter.Button(
            master=self.master,
            text="Exit",
            command=self.close,
            width=10
        )
        self.exit_button.place(x=620, y=370)

    def maplink(self):
        link = "https://osu.ppy.sh/beatmapsets/" + str(beatmap.getmapsetID()) + "#osu/" + str(beatmap.getmapID())
        webbrowser.open(link, new=2, autoraise=True)
    
    def mapdirect(self):
        link = "osu://b/" + str(beatmap.getmapID())
        webbrowser.open(link, new=2, autoraise=False)
    
    def lengthconvert(self, seconds):
        m, s = divmod(seconds, 60)
        response = f'{m:02d}:{s:02d}'
        return response
    
    def setmods(self):
        self.mods = ""
        valid = True
        
        #error handler to check for conflicting mods
        if self.hr.get() == 1 and self.ez.get() == 1:
            messagebox.showerror(title="Error", message="Both HR and EZ cannot be selected as they are conflicting mods, please try again.")
            valid = False
            return valid
        if self.dt.get() == 1 and self.ht.get() == 1:
            messagebox.showerror(title="Error", message="Both DT and HT cannot be selected as they are conflicting mods, please try again.")
            valid = False
            return valid
        
        #all if statements not if, elif, elif, etc because it needs to check each var individually
        if self.ez.get() == 1:
            self.mods = self.mods + "EZ"
        if self.nf.get() == 1:
            self.mods = self.mods + "NF"
        if self.hd.get() == 1:
            self.mods = self.mods + "HD"
        if self.ht.get() == 1:
            self.mods = self.mods + "HT"
        if self.dt.get() == 1:
            self.mods = self.mods + "DT"
        if self.hr.get() == 1:
            self.mods = self.mods + "HR"
        if self.fl.get() == 1:
            self.mods = self.mods + "FL"

        return self.mods

    def ppsubmit(self):
        
        #error handlers
        try:
            self.pp_value_label.destroy()
        except AttributeError:
            pass

        try:
            pp_acc = float(self.pp_acc_ent.get())
        except ValueError:
            messagebox.showerror(title="Error", message="ValueError: must enter an integer or float value for accuracy. Please try again.")
            return

        try:
            pp_combo = int(self.pp_combo_ent.get())
            pp_misses = int(self.pp_misses_ent.get())
        except ValueError:
            messagebox.showerror(title="Error", message="ValueError: must enter an integer value for max combo and/or number of misses. Please try again.")
            return
        
        if pp_acc > 0 and pp_acc <= 100:
            acc = pp_acc
        else:
            msg = messagebox.showerror(title="Error", message="Accuracy value must be between 0 and 100, please try again.")
            return

        if int(self.pp_combo_ent.get()) >= 0:
            combo = int(self.pp_combo_ent.get())
        else:
            msg = messagebox.showerror(title="Error", message="Combo value must be equal to or larger than 0, please try again.")
            return
        
        if int(self.pp_misses_ent.get()) >= 0:
            misses = int(self.pp_misses_ent.get())
        else:
            msg = messagebox.showerror(title="Error", message="Miss count value must be equal to or larger than 0, please try again.")
            return

        global performance
        performance = Performance(acc, combo, misses)
        valid = self.setmods()

        if valid:
            pass
        else:
            return
            
        performance.setmods(self.mods)
        performance.pyttanko(beatmap.getmapID())
        self.pp = performance.getpp()

        #display pp value with tkinter
        self.pp_value_label = tkinter.Label(master=self.master, text=self.pp + " PP")
        self.pp_value_label.place(x=510, y=317)
        return
    
    def close(self):
        msg = messagebox.askyesnocancel(title="Exit", message="Are you sure you wish to exit the program?")

        if msg == True:
            idget.destroy()
        else:
            pass
    
    def goback(self):
        msg = messagebox.askyesnocancel(title="bminfo", message="Are you sure you wish to enter another map?")

        if msg == True:
            self.master.destroy()
            idget.deiconify()

class Diff:
    
    def __init__(self, master, title, artist, mapper, diff_names, diff_list):
        self.master = master
        self.master.title("bminfo.exe (diffselect)")
        self.diff_names = diff_names
        self.diff_list = diff_list

        #title
        self.title_frame = tkinter.Frame(master=self.master, padx=160, pady=10)
        self.title_frame.pack()
        self.title_label = tkinter.Label(master=self.title_frame, text="Difficulty Select")
        self.title_label.pack()
        
        #map information
        self.map_frame = tkinter.Frame(master=self.master, padx=160, pady=10)
        self.map_frame.pack()
        self.song_title_label = tkinter.Label(master=self.map_frame, text=title)
        self.song_title_label.pack()
        self.song_artist_label = tkinter.Label(master=self.map_frame, text=artist)
        self.song_artist_label.pack()
        self.song_mapper_label = tkinter.Label(master=self.map_frame, text="Mapped by " + mapper)
        self.song_mapper_label.pack()

        #diff select
        self.diff_frame = tkinter.Frame(master=self.master, padx=160, pady=10)
        self.diff_frame.pack()

        self.diff = tkinter.IntVar()
        checkboxes = []        
        for i in range(len(diff_names)):
            checkboxes.append(tkinter.Checkbutton(master=self.diff_frame, text=diff_names[i], onvalue=i + 1, variable=self.diff))
            checkboxes[i].pack()

        #buttons
        self.button_frame = tkinter.Frame(master=self.master)
        self.button_frame.pack()
        self.submit_button = tkinter.Button(
            master=self.master,
            text="Submit",
            command=self.submit,
            width=10
        )
        self.cancel_button = tkinter.Button(
            master=self.master,
            text="Cancel",
            command=self.cancel,
            width=10
        )
        self.exit_button = tkinter.Button(
            master=self.master,
            text="Exit",
            command=self.close,
            width=10
        )
        self.exit_button.pack(side=tkinter.RIGHT, padx=5)
        self.cancel_button.pack(side=tkinter.RIGHT)
        self.submit_button.pack(side=tkinter.RIGHT, padx=5)

    def submit(self):
        found = False

        for i in range(len(self.diff_names)):
            if int(self.diff.get()) == i+1:
                found = True
                global beatmap
                beatmap = Beatmap(
                    self.diff_list[i]["beatmap_id"], 
                    self.diff_list[i]["beatmapset_id"],
                    self.diff_list[i]["title"], 
                    self.diff_list[i]["artist"],
                    self.diff_list[i]["version"],
                    self.diff_list[i]["creator"],
                    float(self.diff_list[i]["diff_approach"]),
                    float(self.diff_list[i]["diff_size"]),
                    float(self.diff_list[i]["diff_overall"]),
                    float(self.diff_list[i]["diff_drain"]),
                    float(self.diff_list[i]["difficultyrating"]),
                    int(self.diff_list[i]["hit_length"]),
                    int(self.diff_list[i]["bpm"])
                )
            else:
                pass
        
        if found == False:
            messagebox.showerror(title="Error", message="No option was selected, please try again.")
        else:
            self.master.destroy()
            IdGet.mainwindow(idget)

    def cancel(self):
        msg = messagebox.askyesnocancel(title="Cancel", message="Are you sure you wish to cancel?")

        if msg == True:
            self.master.destroy()
            idget.deiconify()

    def close(self):
        msg = messagebox.askyesnocancel(title="Exit", message="Are you sure you wish to exit the program?")

        if msg == True:
            idget.destroy()
        else:
            pass

idget = tkinter.Tk()
app = IdGet(idget)
idget.mainloop()