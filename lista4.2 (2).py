#napisz program, który będzie symulował błądzenie losowe jednego agenta na siatce kwadratowej. Program ten ma zrzucać obraz siatki do pliku graficznego (w
#formacie jpg, eps lub png) w zadanych odstępach czasowych, a następnie wygenerować z tych plików film w formacie avi lub gif1

import numpy as np
import random
import matplotlib.pyplot as plt
import shutil
import os
import sys
import imageio
import argparse

def brown(n: int, size = 6, name_gif = "brown_gif", destination = r"C:\Users\admin\OneDrive\Pulpit\\", backup_cat = r"C:\Users\admin\OneDrive\Pulpit\inflista4\\"):
    """a function that visualizes agent's random wandering and saves it as gif in given destination path. It stores pictures of each step in backup_cat
    @param n (int): a number of steps an agent is supposed to do
    @param k (int): a size of the board (it should be around 5-10 to see well how the agent moves)
    @param name_gif (str): wanted name of generated gif
    @param destination (str): destination in which the gif is supposed to be saved (by default on Desktop, it should be changed while using on different device) 
    @param backup_cat (str): destination of catalog in which pictures of each step are supposed to be saved (by default on Desktop, it should be changed while using on different device) 
    """

    n = int(n)
    size = int(size)
    if n <= 0:
        raise ValueError("number of steps should be higher than 0")
    elif size <= 0:
        raise ValueError("the board should be bigger than 0x0")
    elif not os.path.exists(destination) or not os.path.exists(backup_cat):
        raise ValueError("catalog(s) doesn't exist, try again")
        
    x_axis = [0]
    y_axis = [0]
    x = y = 0

    for i in range(0, n):
        rad = float(random.randrange(0,360,90)) * np.pi / 180
        x = x + round(np.cos(rad)) 
        y = y + round(np.sin(rad))  
    
        if x == (size + 1) :
            x = size - 1
        elif x == (-size - 1):
            x = -size
        if y == (size + 1):
            y = size
        elif y == (-size - 1):
            y = -size

        x_axis.append(x)
        y_axis.append(y)
        plt.xlim([-size,size])
        plt.ylim([-size,size])
        plt.plot(x_axis, y_axis, "mD:", linewidth = 1.5, alpha = 0.3)
        plt.title("Brown's moves")
        plt.grid(True)
        plt.savefig(str(i))
       
    name = destination + name_gif + ".gif"
    
    with imageio.get_writer(name, fps = 3) as writer:
        for i in range(0, n):
            name = str(i) + ".png"
            image = imageio.imread(name)
            writer.append_data(image)
            try:
                shutil.move(name, backup_cat)
            except:
                shutil.rmtree(backup_cat)
                os.mkdir(backup_cat)
                shutil.move(name, backup_cat)
    return


if __name__== "__main__":
    if len(sys.argv) == 2:
        brown(sys.argv[1])
    elif len(sys.argv) == 3:
        brown(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        brown(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        brown(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) == 6:
        brown(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        raise ValueError("not enough arguments, try again")
     


