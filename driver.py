import parser
from fileio import dirutils


class Driver:
    directory_name = ""
    server_name = ""
    output_dir = ""
    db_name = ""

    def generate_directory(self):
        utilObj = dirutils.Dirutils()
        directory_list_path = self.directory_name + "\\" + "\\" + "logs" + "\\" + "\\" + self.server_name
        fileList = utilObj.directoryList(directory_list_path)
        print(' '.join(fileList))

        myParser = parser.Parser()
        myParser.rootDir = directory_list_path
        myParser.database = self.db_name
        myParser.server = self.server_name
        myParser.outputFile = ""

        for logs in fileList:
            cName: ""
            cName = logs.partition("eq2log_")[2]
            sName = logs.partition("eq2log_")[2].split(".")[0]
            myParser.fileToSearch = logs
            myParser.outputFile = self.output_dir + "sales" + cName
            myParser.seller = sName
            print(" working on " + logs + " : " + "sales" + cName)
            myParser.parseLogFile()
