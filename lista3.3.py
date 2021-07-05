## Napisz program, który szuka plików o zadanych rozszerzeniach w pewnych katalogach i tworzy kopie zapasowe tych zmodyfikowanych w ostatnich trzech dniach do
#katalogu Backup/copy-X (lub Backup\copy-X pod Windows), gdzie X to aktualna data.

import os
import sys
import datetime
from datetime import date
from datetime import datetime as dt
from datetime import timedelta
from zipfile import ZipFile
import glob
import shutil

def main(folder: str, type_ext: str, destination = r"C:\Users\admin\OneDrive\Pulpit"):
    """a function that searches for files that are in given catalog, with given extensions and that has been modified in the last three days 
    and archives them in zip catalog with current date in catalog Backup in optional destination path (set by default on Desktop, it should be modified while using the function on different device).
    @param folder: a path to the catalog with files to search in
    @param type: a wanted extension
    @param destination: an optional path to the destination catalog in which files are supposed to be archived
    return: list of the files that meets the requirements 
    """

    if os.path.exists(destination) == False:
        raise FileNotFoundError("your destination path doesn't exist, try again")

    if not os.path.isdir(folder) or not os.path.exists(folder):
        raise FileNotFoundError("a path is damaged or doesn't exist")

    text = str(folder) + "\\**\\*." + str(type_ext)
    right_extensions = glob.glob(text, recursive = True)
    catalog_name = destination + r"\Backup12"
    archive_name = catalog_name + r"\copy-" + str(date.today().strftime("%b-%d-%Y"))
    files = []

    try:
        os.mkdir(catalog_name)
    except FileExistsError:
        pass

    try:
        os.mkdir(archive_name)
    except FileExistsError:
        pass

    for file in right_extensions:
        stats = os.stat(file)
        mod_time = dt.fromtimestamp(stats[-2])
        if (dt.now() - mod_time) < timedelta(days = 3):
            files.append(file)
    
    if len(files) == 0:
        print("no such file was found, check your spelling or ignore it")
        return False

    for file in files:
        var = len(type_ext) + 1
        name = file[:-var] + "-copy." + type_ext
        try:
            shutil.copyfile(file, name)
            shutil.move(name, archive_name)
        except shutil.Error:
            os.remove(name)
            print(("there is already a file {} in this destination, it was omitted while saving, \ncheck manually which one do you want to save").format(file))
            pass

    return files


if __name__ == "__main__":

    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) > 4:
        raise ValueError("too many variables")
    elif len(sys.argv) < 3:
        raise ValueError("not enough variables")
    else:
	    main(sys.argv[1], sys.argv[2])