from configparser import ConfigParser
from operator import itemgetter
from tkinter import *
from tkinter import ttk
import tkinter as tk
import dirutils
import driver
import filereader

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
    folder_list = utilObj.findEQII(driveLetter, "Everquest II")
    varF.set(folder_list[0])
    drop = OptionMenu(root, varF, *folder_list, command=foldSelect)
    drop.grid(row=1, column=2)

def create_window():
    global detail_pane
    global details_frame
    detail_pane = tk.Toplevel()
    detail_pane.geometry("600x340")
    detail_pane.title("Sales Details")
    varD=StringVar()
    mlist = utilObj.directoryList(output_directory)
    if len(mlist) == 0:
        file_list = ["No files present"]
    else:
        file_list = mlist
    varD.set(file_list[0])
    det_label = ttk.Label(detail_pane, text='Detail Pane')
    det_label.pack()
    drop_details = OptionMenu(detail_pane, varD, *file_list, command=repopulate_tree)
    drop_details.pack()

    details_frame = ttk.Treeview(detail_pane)
    details_frame['columns'] = ("Item", "Price")
    details_frame.column("#0", width=100, minwidth=90)
    details_frame.column("Item",anchor=W, width=240)
    details_frame.column("Price", anchor=CENTER, width=100)
    details_frame.heading("#0", text="Label", anchor=W)
    details_frame.heading("Item", text="Item", anchor=W)
    details_frame.heading("Price", text="Price", anchor=CENTER)
    populate_detail(details_frame,'')
    details_frame.pack(pady=1)
    detail_pane.mainloop()

def populate_detail(panel, varD):
    print("populating detail_pane")
    filereaderObj = filereader.Filereader()
    filereaderObj.rootDir = output_directory
    if len(varD) == 0:
        pass
    else:
        filereaderObj.fileToSearch = varD
    file_list = filereaderObj.getRows()
    if len(file_list) == 0:
        print("The file " + filereaderObj.fileToSearch + " was empty!")
    else:
        for i in file_list:
            print("detail is : " + i)
            price = ""
            datestamp = ""
            item = ""
            if i.find("for "):
                itemdelimited = i.split("for ")
                item = itemdelimited[0]
                if len(itemdelimited[1]):
                    pricetime = itemdelimited[1].split("\\")
                    price = pricetime[0]
                    datestamp = pricetime[1]
            panel.insert(parent='', index='end', text=datestamp, values=(item, price))

def repopulate_tree(varD):
    for row in details_frame.get_children():
        details_frame.delete(row)
    detail_pane.update()
    populate_detail(details_frame, varD)
#end method definitions

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