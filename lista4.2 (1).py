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

def brown(n: int, name_gif: str, destination: str, backup_cat: str):
    """a function that visualizes agent's random wandering and saves it as gif in given destination path. It stores pictures of each step in backup_cat
    @param n (int): a number of steps an agent is supposed to do
    @param name_gif (str): wanted name of generated gif
    @param destination (str): destination in which the gif is supposed to be saved 
    @param backup_cat (str): destination of catalog in which pictures of each step are supposed to be saved
    """
    n = int(n)
    x_axis = [0]
    y_axis = [0]
    x = y = 0

    for i in range(0, n):
        rad = float(random.randrange(0,360,90)) * np.pi / 180
        x = x + round(np.cos(rad)) 
        y = y + round(np.sin(rad))  
    
        if x > 6 or x < -6 or y > 6 or y < -6:
            n = i
            print("Attention! Outside borders in " + str(n))
            break 
        x_axis.append(x)
        y_axis.append(y)
        plt.xlim([-6,6])
        plt.ylim([-6,6])
        plt.plot(x_axis, y_axis, "mD:", linewidth = 1.5, alpha = 0.5)
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--n", required = True, type = int)
    args = parser.parse_args()
    name_gif = "brown_parser"
    destination = r"C:\Users\admin\OneDrive\Pulpit\\"
    backup_cat = r"C:\Users\admin\OneDrive\Pulpit\inflista4"
    brown(args.n, name_gif, destination, backup_cat)


