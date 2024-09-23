from tkinter import *
import dirutils

root = Tk()
root.geometry("300x200")
root.minsize(300, 200)
root.maxsize(600, 400)

def myClick():
    myLabel2 = Label(root, text="Generating the files from the logs.")
    myLabel2.grid(row=3, columnspan = 2, column=0)

def dc(event):
    myLabel3 = Label(root, text="Available Installations:")
    myLabel3.grid(row=1, column=0)
    var = StringVar()
    folderList = utilObj.findEQII()
    var.set(folderList[0])
    drop = OptionMenu(root, var, *folderList, command=dc)
    drop.grid(row=1, column=1)


root.title("Everquest II Seller monitor")

utilObj = dirutils.Dirutils()
driveList = utilObj.findDrives()
#driveList = ["C:", "F:", "H:"]
myLabel0 = Label(root, text = "Available Drives: ")
var = StringVar()
var.set(driveList[0])
drop = OptionMenu(root, var, *driveList, command = dc)
myLabel0.grid(row = 0, column = 0)
drop.grid(row = 0, column = 1)

#root.winfo_width(500)
myButton = Button(root, text = "Generate Files", padx = 20, pady = 5, command = myClick)
myLabel = Label(root, text = "Status", padx = 50, pady = 50)
myLabelFiller = Label(root, text="")
myLabelFiller.grid(row=1, column=0)
myButton.grid(row = 2, column = 0)
myLabel.grid(row = 3, column = 0)

root.mainloop()