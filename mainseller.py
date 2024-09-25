import re
import tkinter as tk
from configparser import ConfigParser
from tkinter import *
from tkinter import ttk

import pandas as pd

# project class imports
import dirutils
import driver
import filereader


# method definitions
def generateFiles():
    search_path = utilObj.workingPath
    print(" inside generateFiles() :" + search_path)
    #TODO clean up driver code
    driver_object = driver.Driver()
    driver_object.directory_name = utilObj.workingPath
    driver_object.server_name = utilObj.server_name
    driver_object.output_dir = output_directory
    update_statusbar("Generating files from logs")
    driver_object.generate_directory()
    update_statusbar("Sales files generated")

def dwClick():
    pass

def foldSelect(adjPath):
    print("foldSelect - This is the folder passed : " + adjPath)
    varSer = StringVar()
    utilObj.workingPath = adjPath
    server_list = utilObj.findEQIIServer(adjPath)
    if len(server_list) == 0:
        print("length was zero")
        update_statusbar("No Logs Found.")
    else:
        varSer.set(server_list[0])
        dropSer = OptionMenu(root, varSer, *server_list, command=folderSelected)
        dropSer.grid(row=2, column=2)
        myButton = Button(root, text="Generate Files", padx=0, pady=5, command=generateFiles)
        myButton.grid(row=2, column=0)
        update_statusbar("Select Server")

def folderSelected(varSer):
    utilObj.server_name = varSer

def dc(event):
    varF = StringVar()
    print("This is the event passed" + event)
    driveLetter = event
    update_statusbar("Searching Drive  " + driveLetter)
    utilObj.current_drive = driveLetter
    folder_list = utilObj.findEQII(driveLetter, "Everquest II")
    varF.set(folder_list[0])
    drop = OptionMenu(root, varF, *folder_list, command=foldSelect)
    drop.grid(row=1, column=2)
    update_statusbar("Drive Search Complete")

def create_window():
    global detail_pane
    detail_pane = tk.Toplevel()
    detail_pane.geometry("500x340")
    detail_pane.title("Sales Details")
    varD=StringVar()
    mlist = utilObj.directoryList(output_directory)
    if len(mlist) == 0:
        file_list = ["No files present"]
    else:
        file_list = mlist
    varD.set(file_list[0])
    det_label = ttk.Label(detail_pane, text='Detail Pane')
    det_label.grid(row=0, column=0)
    drop_details = OptionMenu(detail_pane, varD, *file_list, command=repopulate_detail)
    drop_details.grid(row=1, column=0)
    populate_detail(detail_pane, '')
    detail_pane.mainloop()

def repopulate_detail(varD):
    print(" repopulate_detail :" + varD)
    populate_detail(detail_pane, varD)

def populate_detail(panel, varD):
    global df
    filereaderObj = filereader.Filereader()
    filereaderObj.rootDir = output_directory
    if len(varD) == 0:
        pass
    else:
        filereaderObj.fileToSearch = varD
    file_list = filereaderObj.getRows()
    if len(file_list) == 0:
        print("The file " + filereaderObj.fileToSearch + " was empty!")
        repopulate_tree(varD)
    else:
        ids = []
        dates = []
        items = []
        prices = []
        index = 0
        for i in file_list:
            index = index + 1
            price = None
            datestamp = None
            item = None
            if i.find("for "):
                item_delimited = i.split("for ")
                item = item_delimited[0]
                if len(item_delimited) == 2:
                    pricetime = item_delimited[1].split("\\")
                    price = pricetime[0]
                    datestamp = pricetime[1]
                    ids.append(index)
                    prices.append(price)
                    items.append(item)
                    dates.append(datestamp)
        data = {
            "id": ids,
            "Date": dates,
            "Item": items,
            "Price": prices
        }
        df = pd.DataFrame(data)
        display_tree(panel, df)

def display_tree(pane, df):
    global details_window
    p = re.compile(r'\d+\w*\b')
    dataframe_list = list(df)
    result_set = df.to_numpy().tolist()
    details_window = ttk.Treeview(pane, selectmode='browse', show='headings', height=10, columns=dataframe_list)
    # scrollbars
    vsb = Scrollbar(details_window, orient="vertical", command=details_window.yview)
    vsb.place(relx=0.978, rely=0.175, relheight=0.713, relwidth=0.020)
    details_window.configure(yscrollcommand=vsb.set)
    #TODO fine tune the size of the right scrollbar
    details_window.grid(row=2, column=0, columnspan=3, padx=15, pady=10)
    for col in dataframe_list:
        details_window.column(col, width=100, anchor='c')
        details_window.heading(col, text=col, command=lambda col=col: sort_on_column(col))
    # Populate tree from dataframe
    details_window.tag_configure('GREEN_TAG', foreground='green')
    for dt in result_set:
        v = [r for r in dt]  # creating a list from each row
        try:
            sales_price = resolve_price(v[3])
            v[3] = float("{:.4f}".format(sales_price))
            price_point = int(price_limit)
        except ValueError:
            sales_price=0
            price_point=10
        if sales_price>price_point:
            details_window.insert("", 'end', iid=v[0], values=v, tag='GREEN_TAG')
        else:
            details_window.insert("", 'end', iid=v[0], values=v)

def sort_on_column(column):
    global df,sort_order
    if sort_order:
        sort_order=False # set ascending value
    else:
        order=True
    df=df.sort_values(by=[column],ascending=sort_order)
    display_tree(detail_pane, df)

def repopulate_tree(varD):
    try:
        for row in details_window.get_children():
            details_window.delete(row)
        detail_pane.update()
    except NameError:
        print("first time, panel not defined")

def update_statusbar(message):
    status = Label(root, text=message, relief=SUNKEN, anchor=E)
    status.grid(row=4, column=2, columnspan=3, sticky=W + E)
    status.update()

def resolve_price(data):
    ret_val: float = 0.0
    price_array = data.split("~")
    for index in price_array:
        left_op = int(index[0:2])
        if index.find('p')!=-1:
            ret_val += float(left_op*100)
        elif index.find('g')!=-1:
            ret_val += float(left_op)
        elif index.find('s')!=-1:
            ret_val += float(left_op/100)
        else:
            ret_val += float(left_op/1000)
    return ret_val
#end method definitions

#load configuration options
config = ConfigParser()
config.read('settings.ini')
application_title = config.get('main-section', 'application_title')
output_directory = config.get('main-section', 'output_directory')
price_limit = config.get('main-section', 'price_limit')

#Instantiate utility classes
utilObj = dirutils.Dirutils()
utilObj.directory_name = application_title
currentPathToGenerate = ""
driveList = utilObj.findDrives()

# Begin defining the top level pane.
root = Tk()
root.geometry("290x185")
root.minsize(290, 185)
root.maxsize(580, 370)
root.title("Everquest II Seller monitor")
sort_order = True
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
update_statusbar("idle")
root.mainloop()