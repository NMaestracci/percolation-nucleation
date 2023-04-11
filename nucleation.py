# Python code to implement homogeneous nucleation in a medium

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random

#Nombre maximum d'images dans l'animaiton
maxframes = 150

frame = 0
solidity = 0.5
N = 200
Nmax=1
updateInterval = 1
convolutionFactor = 2
Ec = 30
percolation = 0.40


def Grid(N):
    """Fait une grille de N*N 0"""
    return np.array([[0]*N]*N)

def update(frameNum, img, grid, N):
    """Mets a jour la grille.
    frameNum, img: paramètres de funcAnimation
    grid: array numpy de N*N,
    N: la taille de la grille
    seuil: int, densité finale de la grille en nucléation
    p: float, probabilité d'augmenter la valeur d'une case en phase de nucléation"""

    somme = 0
    for i in range(N):
        for j in range(N):
            if grid[i,j] > 80:
                somme += 1
    somme = somme/N**2
    print(somme)
    if somme <= percolation:
        energy_var()
    img.set_data(grid)
    grid[:] = newGrid[:]
    print('frame = ',frameNum,end='\r')
    return img


def nucleate():
    fig, ax = plt.subplots()
    f = "nucleation.gif" 
    img = ax.imshow(grid, interpolation='bilinear',cmap='inferno',vmin=0, vmax=100)
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N),
                                      frames=maxframes,
                                      blit=False,
                                      interval=updateInterval,
                                      save_count=50, 
                                      repeat=False)

    plt.show(block=False)
    ani.save(f, writer=writergif)


def energy_var():
    """ Calcule des gains aléatoires d'énergie """

    #Soit on gagne un quanta d'énergie/le rayon (ici 2) soit on divise l'énergie/le rayon par 2. Ici, si on choisit l'analogie de l'énergie, bien que ce soit 2 elle serait physiquement négative.
    Max = 0
    for i in range(0,N):
        for j in range(0,N):
            if grid[i,j] > Max:
                Max = grid[i,j]

            if grid[i,j] < Ec:
                if random() > solidity:
                    grid[i,j] += 2
                else:
                    grid[i,j] = grid[i,j]/2
                    
            elif grid[i,j] >= Ec:
                grid[i,j]=80
                grid[(i+1)%N,j]+=5
                grid[(i-1)%N,j]+=5
                grid[i,(j+1)%N]+=5
                grid[i,(j-1)%N]+=5

                grid[(i+1)%N,(j+1)%N]+=5
                grid[(i+1)%N,(j-1)%N]+=5
                grid[(i-1)%N,(j+1)%N]+=5
                grid[(i-1)%N,(j-1)%N]+=5
    if Max < 100:
        print(Max)

grid = Grid(N)
newGrid = grid

nucleate()

file = open("data.txt", "w")

file.write(str(grid))

file.close()