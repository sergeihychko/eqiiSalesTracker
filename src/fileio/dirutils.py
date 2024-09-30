"""
module of directory related functions
"""
import os
import re
from pathlib import Path

class Dirutils:
    """support for querying directories."""
    current_drive = ""
    directory_name = ""
    workingPath = ""
    server_name = ""
    generatePath = ""

    def directory_list(self, dir_to_search):
        """
        param dirToSearch: directory to search for files.
        returns: file List[] of all files under param1.
        """
        regex = ".*(.2024)"
        dir_list = []
        for i in os.listdir(dir_to_search):
            if re.match(regex, i):
                pass
            else:
                dir_list.append(i)
        return dir_list

    def find_drives(self):
        """
        finds all drives for current device
        :return: list of drives
        """
        return os.listdrives()

    def find_eqii(self, head_dir, dir_name):
        """
        Searches a selected drive for a specific directory
        :param head_dir: essentially the devices drive letter
        :param dir_name: the name being searched for
        :return:
        """
        output_list = []
        for root, dirs, files in os.walk(head_dir):
            for d in dirs:
                if d.upper() == dir_name.upper( ):
                    output_list.append(os.path.join (root, d))
        return output_list

    def find_eqii_server(self, head_dir):
        """
        gathers a list of n possible server names (folders) under a directory
        :param head_dir: the directory to query for list
        :return: a list of server (folder) names
        """
        d = head_dir + "\\" + "\\" + "logs" + "\\" + "\\"
        output_list = []
        file_path = Path(d)
        if file_path.exists():
            for filename in os.listdir(d):
                output_list.append(filename)
        return output_list
