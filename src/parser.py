"""
module to contain functionality related to parsing log files,
and outputting the data to the database and flatfile
"""
import os
import re

from data import salesitem
from fileio import filewriter
from sql import updatedatabase


class Parser:
    """
    class encapsulating functionality for parsing log files and outputting matched rows
    """
    rootDir = ""
    fileToSearch = ""
    outputFile = ""
    database = ""
    server = ""
    seller = ""

    def parseLogFile(self):
        """
        parses a file for matching sales detail lines and stores them in a list,
        then outputs the list to the database and a file
        :return:
        """
        rows = []
        outputwriter = filewriter.Filewriter()
        outputwriter.outputFile=self.outputFile

        for rel_path, dirs,files in os.walk(self.rootDir):
            if self.fileToSearch in files:
                full_path = os.path.join(self.rootDir,rel_path,self.fileToSearch)
                print("input file :" +full_path)
                with open(full_path,"r", encoding="utf-8") as inputfile:
                    #TODO investigate reason for failure parsing input file
                    try:
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
                                        sitem = salesitem.SalesItem(self.server, self.seller, datestamp, item, price, price, num_bought)
                                        rows.append(sitem)
                    except Exception as e:
                        print("An exception occured processing file : " + inputfile)
                        continue
        print("calling outputwriter with rows")
        outputwriter.write_rows(rows)
        print("calling dbupdate with rows")
        updatedatabase.update(rows)


