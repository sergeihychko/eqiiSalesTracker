"""
module to encompass file reading functionality
"""
import os

class Filereader:
    """
    class to hold methods for retrieving data from files
    """
    rootDir = ""
    fileToSearch = ""

    def get_rows(self):
        """
        pulls the input lines from a file into an object,
        where the root dir is self.rootDir and the file to search is self.fileToSearch
        :return: list of lines from the file.
        """
        return_rows = []
        for rel_path,files in os.walk(self.rootDir):
            if self.fileToSearch in files:
                full_path = os.path.join(self.rootDir,rel_path,self.fileToSearch)
                print("input file :" +full_path)
                with open(full_path,"r", encoding="utf-8") as input_file:
                    data = input_file.readlines()
                    for line in data:
                        return_rows.append(line)
        return return_rows
