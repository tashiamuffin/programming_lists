#rozwiąże równanie ruchu wahadła matematycznego z tłumieniem zapisane w pliku lista4.pdf

from matplotlib import pyplot as plt
from scipy.integrate import odeint
import numpy as np
import argparse
from fractions import Fraction

def f(u,t,Q, w, A):
  """ a function that creates an integral equation from given variables
  @param u (int): some needed variable
  @param t (int): a variable representing period of time
  @param Q (int): a variable
  @param w (int): another variable
  @param A (int): yet another variable
  @return: the equation
  """
  return (u[1], -u[1]/Q - np.sin(u[0]) + A*np.cos(w*t))


def draw(Q, w, A, th, v):
  """ a function that solves the integral equation and visualizes the result
  @param Q (int): a variable
  @param w (int): another variable
  @param A (int): yet another variable
  @param th (int): some variable
  @param v (int): the last variable
  """

  y0=[th,v]
  t = np.linspace(0,100,2000)
  us=odeint(f, y0 , t, args=(Q,w,A))
  ys=us[:,0]
  vs=us[:,1]
  plt.plot(t,ys,"-")
  plt.plot(t,vs,"-")
  plt.show()

if __name__ == "__main__":
  
    parser = argparse.ArgumentParser()
    parser.add_argument('-th', "--th", required = True, type = float, help = "theta argument")
    parser.add_argument('-Q', "--Q", required = True, type = float, help = "Q argument")
    parser.add_argument('-w', "--w", required = True, type = str, help = "w argument")
    parser.add_argument('-A', "--A", required = True, type = float, help = "A argument")
    parser.add_argument('-v', "--v", required = True, type = float, help = "v argument")
    args = parser.parse_args()

    args.w = Fraction(args.w)

    draw(args.Q, args.w, args.A, args.th, args.v)