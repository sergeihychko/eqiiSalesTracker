import os
import re
from pathlib import Path

class Dirutils:

    workingPath = ""

    def directoryList(self, dirToSearch):
        regex = ".*(.2024)"
        dirList = []
        for i in os.listdir(dirToSearch):
            #print(i)
            if re.match(regex, i):
                pass
            else:
                dirList.append(i)
        return dirList

    def findDrives(self):
        return os.listdrives()

    def findEQII(self, head_dir, dir_name):
        outputList = []
        for root, dirs, files in os.walk(head_dir):
            for d in dirs:
                if d.upper() == dir_name.upper( ):
                    outputList.append(os.path.join (root, d))
        return outputList

    def findEQIIServer(self, head_dir):
        print("findEQIIServer path :" + head_dir)
        d = head_dir + "\\" + "\\" + "logs" + "\\" + "\\"
        outputList = []
        filePath = Path(d)
        if filePath.exists():
            for filename in os.listdir(d):
                outputList.append(filename)
        return outputList