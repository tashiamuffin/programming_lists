#Napisz program, który rozpakuje „archiwum” z poprzedniego zadania.

import shutil
import sys
import os

def main(catalog: str, destination = r"C:\Users\admin\OneDrive\Pulpit"):
    """a function that takes a archive catalog containing text documents and unpacks it. 
    It optionally takes also a destination path, by default it's set to catalog with the function in it (to make it easier).
    @param catalog: a path to the archive catalog that is about to be unpacked
    @param destination: an optional path to the destination catalog, where the files are supposed to be unpacked 
                        (set by default on Desktop, it should be modified while using the function on different device though).
    """

    if os.path.exists(destination) == False:
        raise FileNotFoundError("your destination path doesn't exist, try again")

    if not os.path.isdir(catalog) or not os.path.exists(catalog):
        raise FileNotFoundError("a path is damaged or doesn't exist")

    paths = []

    for root, dirs, files in os.walk(catalog):
        for filename in files: 
            file = os.path.join(root, filename) 
            paths.append(file)
	
  	
    for file in paths:
        name = file[:-19] + ".txt"
        try:
            shutil.copyfile(file, name)
            shutil.move(name, destination)
        except shutil.Error:
            os.remove(name)
            print(("there is already a file {} in this destination, it was omitted while unpacking, \ncheck manually which one do you want to save").format(file))
            pass
 

if __name__ == "__main__":
    
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 3:
        raise ValueError("too many variables")
    elif len(sys.argv) < 2:
        raise ValueError("not enough variables")
    else:
        main(sys.argv[1])