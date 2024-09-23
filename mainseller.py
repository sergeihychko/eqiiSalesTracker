from configparser import ConfigParser
from tkinter import *
from tkinter import ttk
import tkinter as tk
import dirutils
import driver

root = Tk()
root.geometry("280x190")
root.minsize(280, 190)
root.maxsize(520, 400)
#load configuration options
config = ConfigParser()
config.read('settings.ini')
application_title = config.get('main-section', 'application_title')
output_directory = config.get('main-section', 'output_directory')
print(application_title + ":" + output_directory)

def generateFiles():
    search_path = utilObj.workingPath
    print(" inside generateFiles() :" + search_path)
    #TODO clean up driver code
    driver_object = driver.Driver()
    driver_object.directory_name = utilObj.workingPath
    driver_object.server_name = utilObj.server_name
    driver_object.output_dir = output_directory
    print(" using driver obj ")
    driver_object.generate_directory()
    status = Label(root, text="Generating files from the logs.", relief=SUNKEN, anchor=E)
    status.grid(row=4, column=2, columnspan=3, sticky=W+E)

def dwClick():
    pass

def foldSelect(adjPath):
    print("foldSelect - This is the folder passed : " + adjPath)
    varSer = StringVar()
    utilObj.workingPath = adjPath
    server_list = utilObj.findEQIIServer(adjPath)
    if len(server_list) == 0:
        print("length was zero")
        status = Label(root, text="No Logs Found.", relief=SUNKEN, anchor=E)
        status.grid(row=4, column=2, columnspan=3, sticky=W + E)
    else:
        varSer.set(server_list[0])
        dropSer = OptionMenu(root, varSer, *server_list, command=folderSelected)
        dropSer.grid(row=2, column=2)
        myButton = Button(root, text="Generate Files", padx=0, pady=5, command=generateFiles)
        myButton.grid(row=2, column=0)
        status = Label(root, text="Select Server.", relief=SUNKEN, anchor=E)
        status.grid(row=4, column=2, columnspan=3, sticky=W + E)

def folderSelected(varSer):
    utilObj.server_name = varSer

def dc(event):
    varF = StringVar()
    print("This is the event passed" + event)
    driveLetter = event
    utilObj.current_drive = driveLetter
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


myButton = Button(root, text = "Generate Files", padx = 0, pady = 5)
dwButton = Button(root, text = "Data Window", padx = 0, pady = 5, command = create_window)

myLabelFiller = Label(root, text="")
myLabelFiller.grid(row=1, column=0)
myButton.grid(row = 2, column = 0)
dwButton.grid(row = 3, column = 0)

status = Label(root, text="current status", relief = SUNKEN, anchor=E)
status.grid(row = 4, column = 2, columnspan=3, sticky=W+E)

root.mainloop()