import dirutils
import parser

class Driver:
    directory_name = ""
    server_name = ""
    output_dir = ""

    def generate_directory(self):
        utilObj = dirutils.Dirutils()
        directory_list_path = self.directory_name + "\\" + "\\" + "logs" + "\\" + "\\" + self.server_name
        fileList = utilObj.directoryList(directory_list_path)
        print(' '.join(fileList))

        myParser = parser.Parser()
        myParser.rootDir = directory_list_path
        myParser.outputFile = ""

        for logs in fileList:
            cName: ""
            cName = logs.partition("eq2log_")[2]
            myParser.fileToSearch = logs
            myParser.outputFile = self.output_dir + "sales" + cName
            print(" working on " + logs + " : " + "sales" + cName)
            myParser.parseLogFile()
