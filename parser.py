import os
import re
import sqlite3
import uuid


class Parser:
    rootDir = ""
    fileToSearch = ""
    outputFile = ""
    database = ""
    server = ""
    seller = ""

    def parseLogFile(self):
        conn = sqlite3.connect('eqiisales.db')
        c = conn.cursor()
        print("testing db ")
        print("outputfile :" + self.outputFile)
        if os.path.exists(self.outputFile):
            os.remove(self.outputFile)
        oFile = open(self.outputFile, "w+")
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
                        p = re.compile(r'bought [0-9]+')
                        match = p.search(line)
                        if match is not None:
                            bought_line = line
                            if len(bought_line) > 0:
                                if bought_line.find("You bought") is -1:
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
                                    dlm = bought_data.find(":") + 1
                                    details = bought_data[dlm:len(bought_data)]
                                    item = details[0:details.find("\\")]

                                    price = ""
                                    rawprice = bought_data[bought_data.find("for ") + 12:len(bought_data)-4]
                                    longpiece = rawprice.split(",")
                                    for i in longpiece:
                                        if price == "":
                                            price = i
                                        else:
                                            price = price + ("~" + i[9:12])
                                    #price = bought_data[bought_data.find("for ") + 12:len(bought_data)]
                                    #price = price[0:price.find("\\")]
                                    oFile.write(item + " for " + price + "\\" + datestamp + "\n")
                                    unique_id = str(uuid.uuid4())
                                    c.execute("INSERT INTO rawsales (id, server, seller, salesdate, description, price) VALUES (?, ?, ?, ?, ?, ?)", (unique_id, self.server, self.seller, datestamp, item, price))
                                    conn.commit()
                                    print("database insert successful")
        oFile.close()
        conn.close()

