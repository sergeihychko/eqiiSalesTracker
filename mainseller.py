from tkinter import *
from tkinter import ttk
import tkinter as tk
import dirutils

root = Tk()
root.geometry("280x190")
root.minsize(280, 190)
root.maxsize(520, 400)

def generateFiles(adjPath):
    serverList = utilObj.findEQIIServer(adjPath)
    print(serverList)
    status = Label(root, text="Generating files from the logs.", relief=SUNKEN, anchor=E)
    status.grid(row=4, column=2, columnspan=3, sticky=W+E)

def dwClick():
    pass

def foldSelect(adjPath):
    print("foldSelect - This is the folder passed : " + adjPath)
    varSer = StringVar()
    serverList = utilObj.findEQIIServer(adjPath)
    utilObj.workingPath = adjPath
    if len(serverList) == 0:
        print("length was zero")
        status = Label(root, text="No Logs Found.", relief=SUNKEN, anchor=E)
        status.grid(row=4, column=2, columnspan=3, sticky=W + E)
    else:
        varSer.set(serverList[0])
        dropSer = OptionMenu(root, varSer, *serverList, command=foldSelect)
        dropSer.grid(row=2, column=2)
        myButton = Button(root, text="Generate Files", padx=0, pady=5, command=generateFiles(adjPath))
        myButton.grid(row=2, column=0)
        status = Label(root, text="Select Server.", relief=SUNKEN, anchor=E)
        status.grid(row=4, column=2, columnspan=3, sticky=W + E)

#def foldSelect(event):
#    adjPath = str(event).replace("\\", "\\\\")
#    print(" the folder was selected : " + adjPath)
#    dwButton = Button(root, text="Data Window", padx=0, pady=5, command=dwClick(adjPath))
#    dwButton.grid(row=3, column=0)

def dc(event):
    varF = StringVar()
    print("This is the event passed" + event)
    driveLetter = event
    folderList = utilObj.findEQII(driveLetter, "Everquest II")
    varF.set(folderList[0])
    drop = OptionMenu(root, varF, *folderList, command=foldSelect)
    drop.grid(row=1, column=2)

def create_window():
    detail_pane = tk.Toplevel()
    detail_pane.geometry("400x300")
    detail_pane.title("Sales Details")
    ttk.Label(detail_pane, text='Detail Pane').pack()

root.title("Everquest II Seller monitor")

utilObj = dirutils.Dirutils()
currentPathToGenerate = ""
driveList = utilObj.findDrives()
#driveList = ["C:", "F:", "H:"]
myLabel0 = Label(root, text = "Available Drives: ")
var = StringVar()
var.set(driveList[0])
drop = OptionMenu(root, var, *driveList, command = dc)
myLabel0.grid(row = 0, column = 0)
drop.grid(row = 0, column = 2)

myLabel3 = Label(root, text="Available Installations:")
myLabel3.grid(row=1, column=0)

#root.winfo_width(500)
myButton = Button(root, text = "Generate Files", padx = 0, pady = 5)
dwButton = Button(root, text = "Data Window", padx = 0, pady = 5, command = create_window)
#myLabel = Label(root, text = "Status", padx = 50, pady = 5)
myLabelFiller = Label(root, text="")
myLabelFiller.grid(row=1, column=0)
myButton.grid(row = 2, column = 0)
dwButton.grid(row = 3, column = 0)

status = Label(root, text="current status", relief = SUNKEN, anchor=E)
status.grid(row = 4, column = 2, columnspan=3, sticky=W+E)

root.mainloop()