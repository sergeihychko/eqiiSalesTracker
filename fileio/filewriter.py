import os

from data import salesitem


class Filewriter:
    rootDir = ""
    outputFile = ""

    def writeRows(self, rows:list[salesitem]):
        status = 0
        print("outputfile :" + self.outputFile)
        if os.path.exists(self.outputFile):
            os.remove(self.outputFile)
        oFile = open(self.outputFile, "w+")
        for row in rows:
            oFile.write("test" + row.description + " for " + row.price + "\\" + row.salesdate + "\n")
        return status