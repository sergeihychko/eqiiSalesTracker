import os
import re

class Filereader:
    rootDir = ""
    fileToSearch = ""

    def getRows(self):
        return_rows = []
        for relPath,dirs,files in os.walk(self.rootDir):
            if self.fileToSearch in files:
                fullPath = os.path.join(self.rootDir,relPath,self.fileToSearch)
                print("input file :" +fullPath)
                with open(fullPath,"r") as input_file:
                    data = input_file.readlines()
                    for line in data:
                        print("adding row")
                        return_rows.append(line)
        return return_rows