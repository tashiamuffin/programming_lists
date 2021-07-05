#Napisz program, który. . .
#Zad. 1 . . . dla podanego (jako argument wywołania) roku wyliczy datę niedzieli wielkanocnej. (Wskazówka: algorytm Meeusa/Jonesa/Buchera).
#Zad. 2 . . . generuje miniaturę obrazu w formacie jpg. Nazwę oryginalnego pliku, rozmiary miniatury i nazwę pliku wyjściowego należy podać jako parametr
#wywołania programu. (Wskazówka: Python Imaging Library, PIL).
#Zad. 3 . . . tworzy kopie bezpieczeństwa, zapisując wybrane katalogi do archiwów zip. Nazwy tych archiwów powinny zawierać aktualną datę jako przedrostek. (Wskazówka: moduł zipfile).
#Zad. 4 . . . generuje roczne statystyki modyfikacji plików z wybranych katalogów na Twoim komputerze. (Wskazówka: os.walk).




import math as m
import datetime
from PIL import Image
import zipfile
import shutil
import os
from zipfile import ZipFile 
import os 
from datetime import date, timedelta
from datetime import datetime as dt

def compute_Easter_date(year:int):  
    """
    A function that calculates the date of Easter Sunday for given year
    :param year: integer for which we want to calculate Easter's date
    :return: Easter's date
    """
    if year < 0:
        raise ValueError("Jesus has not been born yet, year should be a positive number")
  
    a = year%19
    b = m.floor(year/100)
    c = year%100
    d = m.floor(b/4)
    e = b%4
    f = m.floor((b + 8) / 25)
    g = m.floor((b - f + 1) / 3)
    h = (19*a + b - d - g + 15)%30
    i = m.floor(c / 4)
    k = c%4
    l = (32 + 2*e + 2*i - h -k)%7
    n = m.floor((a + 11*h + 22*l)/451)
    p = (h + l - 7*n + 114)%31

    day = p + 1
    month = m.floor((h + l - 7*n + 114)/31)

    date = datetime.datetime(year, month, day)
    date = '{} {} {}'.format(day, date.strftime("%B"),year)

    return date

def generate_miniature_jpg(name:str,size:list,new_name:str):
    """
    a function that takes a photo in jpg and changes it into a thumbnail in desired size and name (taken as arguments), then new photo is shown
    :param name: a path of a original photo (a raw string)
    :param size: desirable size of a thumbnail (a list) 
    :param new_name: new name for a generated thumbnail (a raw string)
    :return: shows a thumbnail if the original file exists and the size is appropriate, if not error is raised
    """
    size = tuple(size) 
    
    if os.path.exists(name):
        
        imag = Image.open(name)
        
        for n in (0,1):
            if im.size[n] < size[n]:
                raise ValueError("picture should be smaller than the original")

        new_im = imag.resize(size)
        new_im.save(new_name)
        new_im.show()
        
    else:
        raise FileNotFoundError("file doesn't exist")

def generate_zip_copy(catalog:str): 
    """
    a function that takes a catalog (its path) and creates a zip archive for all the files in it.
    :param catalog: path for the directory as raw string
    """
    
    path = catalog.split("\\")
    cat_name = path[-1]
    
    name = (date.today()).strftime("%b-%d-%Y") + "_" + cat_name + "_archive.zip"
    
    paths = [] 
    
    for root, dirs, files in os.walk(catalog): 
        for filename in files: 
            file = os.path.join(root, filename) 
            paths.append(file)

    with ZipFile(name,'w') as archive:
        for file in paths: 
            archive.write(file)     
    

def generate_stats(catalog:str):
    """
    a function that takes a catalog and generates year long statistics of modifications of its files
    :param catalog: path for the catalog as raw string
    """
    for root, dirs, files in os.walk(catalog, topdown = False):
        for name in files:
            file = str(os.path.join(root, name))
            stat_help(file,name)
        for name in dirs:
            file = str(os.path.join(root, name))
            stat_help(file,name)
            
def stat_help(file,name):
    """
    a function that generates, formats and prints year long statistics of modifications of given file
    :param file: path of the file as string
    :param name: name of the file as string
    :return: prints statistics for each file
    """
    stats = os.stat(file)
    creat_time = dt.fromtimestamp(stats[-1])
    mod_time = dt.fromtimestamp(stats[-2])
    
    if (dt.now() - mod_time) < timedelta(days = 365):
        text = "file {} last modified {}".format(name, mod_time)
        print(text, "\n", 50 * "-")
                
    elif (dt.now() - creat_time) < timedelta(days = 365):
        text = "file {} created {}".format(name, creat_time)
        print(text, "\n", 50 * "-")
    

def generate_stats1(catalog:str):
    """
    a function that takes a catalog and generates year long statistics of modifications of its files
    :param catalog: path for the catalog as raw string
    :return: printed statistics of each file
    """
    
    with os.scandir(catalog) as it:
        
        for file in it:
            
            stats = file.stat()
            mod_time = dt.fromtimestamp(stats[-2])
            creat_time = dt.fromtimestamp(stats[-1])
            
            if file.is_dir():
                generate_stats1(file.path)
                
            if (dt.now() - mod_time) < timedelta(days = 365):
                text = "file {} last modified {}".format(file.name, mod_time)
                print(text, "\n", 50 * "-")
                
            elif (dt.now() - creat_time) < timedelta(days = 365):
                text = "file {} created {}".format(file.name, creat_time)
                print(text, "\n", 50 * "-")
                       
