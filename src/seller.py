"""
module containing the class which wraps the gui components,
 and event handling for the Seller project
"""
import os
import re
import tkinter as tk
from configparser import ConfigParser
from tkinter import *
from tkinter import ttk

import pandas as pd

# project class imports
import driver
from fileio import filereader, dirutils
from sql import schema, updatedatabase


class GUIDriver:
    """
    class containing all gui components and event methods
    """
    utilObj = dirutils.Dirutils()
    driver_object = driver.Driver()
    application_title = ""
    output_directory = ""
    price_limit = ""
    database = ""
    driveList = []
    seller_list = []

    def __init__(self):
        self.root = tk.Tk()
        # Begin defining the top level pane.
        self.root.geometry("290x185")
        self.root.minsize(290, 185)
        self.root.maxsize(580, 370)
        self.root.title("Everquest II Seller monitor")

        self.create_widgets()

    def run(self):
        """
        run entry point for the top level gui object
        """
        self.root.mainloop()

    def generateFiles(self):
        """
        function that will attempt to generate the output dir and files
        when the button is selected. If the drive, folder, and server have been selected.
        :return:
        """
        search_path = self.utilObj.workingPath
        print(" inside generateFiles() :" + search_path)
        self.driver_object.directory_name = self.utilObj.workingPath
        self.driver_object.server_name = self.utilObj.server_name
        self.driver_object.output_dir = self.output_directory
        self.driver_object.db_name = self.database
        self.update_statusbar("Generating files from logs")
        self.driver_object.generate_directory()
        self.update_statusbar("Sales files generated")

    def dwClick(self):
        pass

    def generate_seller_list(self):
        self.seller_list = updatedatabase.get_seller_list()

    def foldSelect(self, adjPath):
        print("foldSelect - This is the folder passed : " + adjPath)
        varSer = StringVar()
        self.utilObj.workingPath = adjPath
        server_list = self.utilObj.find_eqii_server(adjPath)
        if len(server_list) == 0:
            print("length was zero")
            self.update_statusbar("No Logs Found.")
        else:
            varSer.set(server_list[0])
            dropSer = OptionMenu(self.root, varSer, *server_list, command=self.folderSelected)
            dropSer.grid(row=2, column=2)
            myButton = Button(self.root, text="Generate Files", padx=0, pady=5, command=self.generateFiles)
            myButton.grid(row=2, column=0)
            self.update_statusbar("Select Server")

    def folderSelected(self, varSer):
        self.utilObj.server_name = varSer

    def dc(self, event):
        varF = StringVar()
        drive_letter = event
        self.update_statusbar("Searching Drive  " + drive_letter)
        self.utilObj.current_drive = drive_letter
        folder_list = self.utilObj.find_eqii(drive_letter, "Everquest II")
        varF.set(folder_list[0])
        drop = OptionMenu(self.root, varF, *folder_list, command=self.foldSelect)
        drop.grid(row=1, column=2)
        self.update_statusbar("Drive Search Complete")

    def create_window(self):
        global detail_pane
        detail_pane = tk.Toplevel()
        detail_pane.geometry("500x340")
        detail_pane.title("Sales Details")
        varD=StringVar()
        if len(self.seller_list) == 0:
            file_list = ["No sellers present"]
        else:
            file_list = self.seller_list
        varD.set(file_list[0])
        det_label = ttk.Label(detail_pane, text='Detail Pane')
        det_label.grid(row=0, column=0)
        det_button = ttk.Button(detail_pane, text="refresh", command=self.generate_seller_list)
        det_button.grid(row=0, column=2)
        drop_details = OptionMenu(detail_pane, varD, *file_list, command=self.repopulate_detail)
        drop_details.grid(row=1, column=0)
        self.populate_detail(detail_pane, '')
        detail_pane.mainloop()

    def repopulate_detail(self, varD):
        #print(" repopulate_detail :" + varD)
        self.populate_detail(detail_pane, varD)
        self.create_window()

    def populate_detail(self, panel, varD):
        global df
        seller = varD[0]
        filereaderObj = filereader.Filereader()
        filereaderObj.rootDir = self.output_directory
        if len(varD) == 0:
            pass
        else:
            filereaderObj.fileToSearch = varD
        file_list = filereaderObj.get_rows()
        print("about to call db retrieve: " + seller)
        file_list2 = updatedatabase.retrieve_seller_data(seller)
        for b in file_list2:
            print("db returned row : " + str(b))
        if len(file_list) == 0:
            print("The file " + filereaderObj.fileToSearch + " was empty!")
            self.repopulate_tree(varD)
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
            self.display_tree(panel, df)

    def display_tree(self, pane, df):
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
            details_window.heading(col, text=col, command=lambda col=col: self.sort_on_column(col))
        # Populate tree from dataframe
        details_window.tag_configure('GREEN_TAG', foreground='green')
        for dt in result_set:
            v = [r for r in dt]  # creating a list from each row
            try:
                sales_price = self.resolve_price(v[3])
                v[3] = float("{:.4f}".format(sales_price))
                price_point = int(self.price_limit)
            except ValueError:
                sales_price=0
                price_point=10
            if sales_price>price_point:
                details_window.insert("", 'end', iid=v[0], values=v, tag='GREEN_TAG')
            else:
                details_window.insert("", 'end', iid=v[0], values=v)

    def sort_on_column(self, column):
        global df,sort_order
        if sort_order:
            sort_order=False # set ascending value
        else:
            order=True
        df=df.sort_values(by=[column],ascending=sort_order)
        self.display_tree(detail_pane, df)

    def repopulate_tree(self, varD):
        try:
            for row in details_window.get_children():
                details_window.delete(row)
            detail_pane.update()
        except NameError:
            print("first time, panel not defined")

    def update_statusbar(self, message):
        status = Label(self.root, text=message, relief=SUNKEN, anchor=E)
        status.grid(row=5, column=2, columnspan=3, sticky=W + E)
        status.update()

    def resolve_price(self, data):
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

    def createdb(database):
        schema.create_tables(database)

    def create_widgets(self):
        #load configuration options
        config = ConfigParser()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, "settings.ini")
        # Use the config file
        config.read(config_file_path)
        self.application_title = config.get('main-section', 'application_title')
        self.output_directory = config.get('main-section', 'output_directory')
        self.price_limit = config.get('main-section', 'price_limit')
        self.database = config.get('main-section', 'database_name')

        #Instantiate utility classes
        self.utilObj.directory_name = self.application_title
        self.driveList = self.utilObj.find_drives()
        #TODO remove the drop table call when moving files is complete
        updatedatabase.dump()

        sort_order = True
        self.root.myLabel0 = Label(self.root, text = "Available Drives: ")
        var = StringVar()
        var.set(self.driveList[0])
        self.root.drop = OptionMenu(self.root, var, *self.driveList, command = self.dc)
        self.root.myLabel0.grid(row = 0, column = 0)
        self.root.drop.grid(row = 0, column = 2)
        self.root.myLabel3 = Label(self.root, text="Available Installations:")
        self.root.myLabel3.grid(row=1, column=0)
        self.root.myButton = Button(self.root, text = "Generate Files", padx = 0, pady = 5)
        self.root.dwButton = Button(self.root, text = "Data Window", padx = 0, pady = 5, command = self.create_window)
        self.root.myLabelFiller = Label(self.root, text="")
        self.root.myLabelFiller.grid(row=1, column=0)
        self.root.myButton.grid(row = 2, column = 0)
        self.root.dwButton.grid(row = 3, column = 0)
        self.update_statusbar("idle")

class Seller():
    """
    a class that builds the app based on the design of class::GUIDriver
    """
    def build(self):
        return GUIDriver()

if __name__ == "__main__":
    driver = GUIDriver()
    driver.run()

##########################
# author: Serge Hychko
#date: September 2024
##########################
