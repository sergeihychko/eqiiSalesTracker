import os
import re

class Parser:
    rootDir = ""
    fileToSearch = ""
    outputFile = ""

    def parseLogFile(self):
        print("outputfile :" + self.outputFile)
        if os.path.exists(self.outputFile):
            os.remove(self.outputFile)
        oFile = open(self.outputFile, "w+")
        print("begin")
        for relPath,dirs,files in os.walk(self.rootDir):
            if self.fileToSearch in files:
                fullPath = os.path.join(self.rootDir,relPath,self.fileToSearch)
                print("input file :" +fullPath)
                with open(fullPath,"r") as inputfile:
                    data = inputfile.readlines()
                    for line in data:
                        if len(line) > 38:
                            datetime = line[13:37]
                            datestamp = datetime[4:10] + ", " + datetime[20:24]
                        else:
                            datetime = ""
                        if 'bought ' in line:
                            bought_line = line
                            if len(bought_line) > 0:
                                if bought_line.find("You bought") is -1:
                                    #print("gotcha" + str(bought_line.find("You bought")))
                                    bought_data = bought_line.split("bought ",1)[1]
                                else:
                                    bought_data =""
                                if len(bought_data) > 0:
                                    print(bought_data)
                                    num_bought = 0
                                    try:
                                        num_bought = re.search(r'\d+', bought_data).group()
                                    except Exception:
                                        pass
                                    print("Number bought: " + str(num_bought))
                                    dlm = bought_data.find(":") + 1
                                    details = bought_data[dlm:len(bought_data)]
                                    item = details[0:details.find("\\")]
                                    price = bought_data[bought_data.find("for ") + 12:len(bought_data)]
                                    price = price[0:price.find("\\")]
                                    print(item + " for " + price)
                                    oFile.write(item + " for " + price + "\\" + datestamp + "\n")
        oFile.close()