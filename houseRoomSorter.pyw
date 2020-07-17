import random
import tkinter as tk
from functools import partial

allRooms = []
allMortals = []

def assign(housemates):
    random.shuffle(housemates)
    for i in housemates:
        for j in i.prefs:
            if j.assigned == False:
                j.assign(i)
                break

class mortal:
    def __init__(self, name):
        self.name = name
    def list_prefs(self, prefs):
        self.prefs = prefs

class room:
    assigned = False
    def __init__(self, title):
        self.title = title
    def assign(self, mortal):
        if self.assigned == False:
            self.assigned = True
            self.assignedTo = mortal

def run():
    rooms = int(input("How many rooms are there?"))
    for x in range(rooms):
        roomName = input("Please give a name for room "+str(x))
        newRoom = room(roomName)
        allRooms.append(newRoom)
    mortals = int(input("How many people live in the house?"))
    for y in range(mortals):
        mortalName = input("Please give a name for mortal "+str(y))
        newMortal = mortal(mortalName)
        allMortals.append(newMortal)
    random.shuffle(allMortals)
    for z in allMortals:
        print(z.name + " please list the rooms in order of preference (preferred room first)")
        prefList = []
        while(len(prefList) != len(allRooms)):
            nextRoom = input()
            for a in allRooms:
                if nextRoom == a.title:
                    prefList.append(a)
        z.list_prefs(prefList)
    assign(allMortals)
    for b in allRooms:
        print(b.title + ": " + b.assignedTo.name)

def makeGUI():
    allMortalFrames = []
    valuesList = []
    upButtonIDs = []
    downButtonIDs = []
    window = tk.Tk()
    window.title("Shared House Room Organiser")

    buttonsFrame = tk.Frame(master=window, borderwidth=5)
    buttonsFrame.pack()
     
    mortalsFrame = tk.Frame(master=window, borderwidth=5)
    mortalsFrame.pack()

    goTimeFrame = tk.Frame(master=window, borderwidth=5)
    goTimeFrame.pack()

    def newMortalFrame(name):
        mortalFrame = tk.Frame(master=mortalsFrame, borderwidth = 5)
        mortalFrame.grid(row = 0, column = len(allMortalFrames))
        mortalLabel = tk.Label(master = mortalFrame, text = name)
        mortalLabel.grid(row = 0, column = 0)
        allMortalFrames.append(mortalFrame)
        newMortalEntry.delete(0, "end")

        for itera, room in enumerate(allRooms):
            roomFrame = tk.Frame(master=mortalFrame, borderwidth = 4)
            roomFrame.grid(row = itera+1, column = 0)
            roomLabel = tk.Label(master = roomFrame, text = room.title)
            roomLabel.grid(row = 0, column = 0)
            roomUpButton = tk.Button(master = roomFrame, text = "+", command = partial(roomUp, len(upButtonIDs)))
            upButtonIDs.append(roomUpButton)
            roomUpButton.grid(row = 0, column = 3)
            roomDownButton = tk.Button(master = roomFrame, text = "-", command = partial(roomDown, len(downButtonIDs)))
            downButtonIDs.append(roomDownButton)
            roomDownButton.grid(row = 0, column = 4)

    def roomUp(identity):
        button = upButtonIDs[identity]
        parentFrame = button._nametowidget(button.winfo_parent())
        grandparentFrame = parentFrame._nametowidget(parentFrame.winfo_parent())
        position = parentFrame.grid_info()["row"]
        if position == 1:
            return
        for item in grandparentFrame.winfo_children():
            if item.grid_info()["row"] == position - 1:
                item.grid(row = item.grid_info()["row"]+1, column = 0)
            elif item.grid_info()["row"] == position:
                item.grid(row = item.grid_info()["row"] - 1, column = 0)

    def roomDown(identity):
        button = downButtonIDs[identity]
        parentFrame = button._nametowidget(button.winfo_parent())
        grandparentFrame = parentFrame._nametowidget(parentFrame.winfo_parent())
        position = parentFrame.grid_info()["row"]
        if position == len(allRooms):
            return
        for item in grandparentFrame.winfo_children():
            if item.grid_info()["row"] == position + 1:
                item.grid(row = item.grid_info()["row"]-1, column = 0)
            elif item.grid_info()["row"] == position:
                item.grid(row = item.grid_info()["row"] + 1, column = 0)

    def addNewRoom(roomTitle):
        for frame in allMortalFrames:
            roomFrame = tk.Frame(master=frame, borderwidth = 4)
            roomFrame.grid(row = len(allRooms)+1, column = 0)
            roomLabel = tk.Label(master = roomFrame, text = roomTitle)
            roomLabel.grid(row = 0, column = 0)
            roomUpButton = tk.Button(master = roomFrame, text = "+", command = partial(roomUp, len(upButtonIDs)))
            upButtonIDs.append(roomUpButton)
            roomUpButton.grid(row = 0, column = 3)
            roomDownButton = tk.Button(master = roomFrame, text = "-", command = partial(roomDown, len(downButtonIDs)))
            downButtonIDs.append(roomDownButton)
            roomDownButton.grid(row = 0, column = 4)
        
        allRooms.append(room(roomTitle))
        newRoomEntry.delete(0, "end")

    def sortRooms():
        housemates = []
        for frame in allMortalFrames:
            housemate = mortal(frame.winfo_children()[0].cget("text"))
            print(housemate.name)
            roomPrefs = []
            iterrooms = iter(frame.winfo_children())
            next(iterrooms)
            tempList = [None] * len(allRooms)
            for room in iterrooms:
                tempList[room.grid_info()['row']-1] = room.winfo_children()[0].cget("text")
            for roomName in tempList:
                for space in allRooms:
                    if roomName == space.title:
                        roomPrefs.append(space)
                        print(space.title)
                        break
            housemate.list_prefs(roomPrefs)
            housemates.append(housemate)
        assign(housemates)
        for frame in allMortalFrames:
            housemate = frame.winfo_children()[0].cget("text")
            roomPrefs = []
            for space in allRooms:
                if space.assignedTo.name == housemate:
                    iterrooms = iter(frame.winfo_children())
                    next(iterrooms)
                    for room in iterrooms:
                        if room.winfo_children()[0].cget("text") == space.title:
                            room.configure(bg = "green")

    newMortalLabel = tk.Label(master = buttonsFrame, text = "Add new housemate")
    newMortalEntry = tk.Entry(master = buttonsFrame)
    newMortalButton = tk.Button(master = buttonsFrame, text = "Add", command = lambda: newMortalFrame(newMortalEntry.get()))
    newMortalLabel.grid(row = 0, column = 0)
    newMortalEntry.grid(row = 0, column = 1)
    newMortalButton.grid(row = 0, column = 2)

    newRoomLabel = tk.Label(master = buttonsFrame, text = "Add new room")
    newRoomEntry = tk.Entry(master = buttonsFrame)
    newRoomButton = tk.Button(master = buttonsFrame, text = "Add", command = lambda: addNewRoom(newRoomEntry.get()))
    newRoomLabel.grid(row = 1, column = 0)
    newRoomEntry.grid(row = 1, column = 1)
    newRoomButton.grid(row = 1, column = 2)

    goGoButton = tk.Button(master = goTimeFrame, text = "Sort out rooms!", command = lambda: sortRooms())
    goGoButton.grid(row = 0, column = 0)

    

makeGUI()
tk.mainloop()

