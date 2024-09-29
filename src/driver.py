"""
module to wrap functionality for parsing input files
"""
import parser
from fileio import dirutils


class Driver:
    """
    class to wrap methods for generating output files after parsing
    """
    directory_name = ""
    server_name = ""
    output_dir = ""
    db_name = ""

    def generate_directory(self):
        """
        drives the parsing of the raw input files to create the output
        directories and create the files in it
        :return:
        """
        status=0
        util_obj = dirutils.Dirutils()
        directory_list_path = (self.directory_name + "\\" + "\\" +
                               "logs" + "\\" + "\\" + self.server_name)
        file_list = util_obj.directory_list(directory_list_path)
        print(' '.join(file_list))

        parser_obj = parser.Parser()
        parser_obj.rootDir = directory_list_path
        parser_obj.database = self.db_name
        parser_obj.server = self.server_name
        parser_obj.outputFile = ""

        for logs in file_list:
            char_name: ""
            char_name = logs.partition("eq2log_")[2]
            seller_name = logs.partition("eq2log_")[2].split(".")[0]
            parser_obj.fileToSearch = logs
            parser_obj.outputFile = self.output_dir + "sales" + char_name
            parser_obj.seller = seller_name
            print(" working on " + logs + " : " + "sales" + char_name)
            parser_obj.parseLogFile()
        return status
