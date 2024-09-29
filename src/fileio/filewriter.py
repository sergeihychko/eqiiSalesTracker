"""
module to encompass file writing functionality
"""
import os

from src.data import salesitem


class Filewriter:
    """
    class to hold methods for outputting data to files
    """
    rootDir = ""
    outputFile = ""

    def write_rows(self, rows:list[salesitem]):
        """
        converts the contents of a dataclass object to a format,
        and writes it out to a file.
        :param rows: a list of salesitem dataclass objects
        :return: the status of attempting to write to the file
        """
        status = 0
        print("outputfile :" + self.outputFile)
        if os.path.exists(self.outputFile):
            os.remove(self.outputFile)
        with open(self.outputFile, "w+", encoding="utf-8") as output_file:
            for row in rows:
                output_file.write("test" + row.description + " for " + row.price +
                            "\\" + row.salesdate + "\n")
            return status
