import os
import re

class Dirutils:

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

    def findEQII(self):
        return ["abcd", "defg"]