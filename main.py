# Code python pour implémenter la percolation d'un milieu créé par nucléation.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random

#Arrêter l'animation si elle prend un temps anormal
maxframes = 450

#Temps entre les images
updateInterval = 1

#Energie de seuil de nucléation
Ec = 30

def Grid(N):
    """Fait une grille de N*N 0"""
    return np.array([[0]*N]*N)

def update(frameNum, img, grid, N, seuil,p):
    """Mets a jour la grille.
    frameNum, img: paramètres de funcAnimation
    grid: array numpy de N*N,
    N: la taille de la grille
    seuil: int, densité finale de la grille en nucléation
    p: float, probabilité d'augmenter la valeur d'une case en phase de nucléation"""

    global Reversed
    global somme

    #Dans une première étape, on calcule la proportion du milieu qui a cristallisé 
    if Reversed == False:
        somme = 0
        for i in range(N):
            for j in range(N):
                if grid[i,j] > 80:
                    somme += 1
        somme = somme/N**2
    
    #Si cette proportion est sous seuil, on applique la nucléation
    if somme <= seuil:
        energy_var(grid,p,N)

    #Sinon, on passe en mode percolation
    elif Reversed == False:
        Reversed = True
        for i in range(N):
            for j in range(N):
                if grid[i,j] >= Ec:
                    grid[i,j] = 100
                else:
                    grid[i,j] = 0

    else:    
    	percolation(grid,N)

    #Mettre à jour la grille à afficher
    img.set_data(grid)
    return img


def nucleate(seuil,p,N,saving=False):
    """ Affichage de l'animation"""

    fig, ax = plt.subplots()

    if saving == True:
        f = "nucleation2.gif" 
        writergif = animation.PillowWriter(fps=30)

    #Calculer les updates avec FuncAnim
    img = ax.imshow(grid, interpolation='bilinear',cmap='viridis_r',vmin=0, vmax=100)
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, seuil,p),
                                      frames=maxframes,
                                      blit=False,
                                      interval=updateInterval,
                                      save_count=50, 
                                      repeat=False)

    #Soit on sauvegarde, soit on montre l'animation
    if saving == True:
        print('sauvegarde de l\'animation...')

        ani.save(f, writer=writergif)
        print('animation sauvegardée.')

    else:
        plt.show(block=False)
        plt.pause(100)
        plt.close()

    #On retourne une instancee de percolation pour connaitre Nmax, et savoir si le système a percolé
    return percolation(grid,N)


def energy_var(grid,p,N):
    """ Calcule des gains aléatoires d'énergie """

    #Soit on gagne un quanta d'énergie/le rayon (ici 2) soit on divise l'énergie/le rayon par 2. Ici, si on choisit l'analogie de l'énergie, bien que ce soit 2 elle serait physiquement négative.

    Max = 0
    for i in range(0,N):
        for j in range(0,N):
            if grid[i,j] > Max:
                Max = grid[i,j]

            if grid[i,j] < Ec:
                if random() < p:
                    grid[i,j] += 2
                else:
                    grid[i,j] = grid[i,j]/2
                    
            elif grid[i,j] >= Ec:
                grid[i,j]=80

                #Cette répartition d'énergie fait croitre des cristaux quasi circulaires. Changer quelles cases adjacentes gagnent de l'énergie change la forme des cristaux.
                grid[(i+1)%N,j]+=5
                grid[(i-1)%N,j]+=5
                grid[i,(j+1)%N]+=5
                grid[i,(j-1)%N]+=5

                grid[(i+1)%N,(j+1)%N]+=5
                grid[(i+1)%N,(j-1)%N]+=5
                grid[(i-1)%N,(j+1)%N]+=5
                grid[(i-1)%N,(j-1)%N]+=5


def percolation(grid,N):
    """ Code très similaire à percolation.py :
    On fait couler un fluide parfait très grossièrement dans le système et
    on voit si il atteint le bas de la grille depuis le sommet."""
    
    #Chemin vertical parcouru au maximum par le fluide
    Nmax = 0

    #conditions aux limites
    for i in range(0,N):
        #premiere ligne 0
        grid[0,i] = 0
        grid[1,i] = 50

    count = 0 #On compte les changements et on recalcule Nmax
    for i in range(1,N-1):
        for j in range(1,N-1):
            if grid[i,j] == 50:
                Nmax = max(Nmax,i)
            if grid[i,j] <= Ec:
                if grid[i+1,j] == 50:
                    grid[i,j] = 50
                    count = count + 1
                elif grid[i-1,j] == 50:
                    grid[i,j] = 50
                    count = count + 1
                elif grid[i,j+1] == 50:
                    grid[i,j] = 50
                    count = count + 1
                elif grid[i,j-1] == 50:
                    grid[i,j] = 50
                    count = count + 1
    if Nmax > N-3 or count == 0: #Si Nmax atteint sa valeur maximale ou qu'il n'y a aucun changement, on arrete le processus.
    	plt.close()

    return Nmax

def simulation(iterations,N,seuil,p,saving=False,retour_texte=False):
    """Simple boucle de reccurence pour jouer plusieurs animations afin de
    faire des statistiques
    """
    Liste = []
    global Reversed
    global somme
    global grid
    global newGrid
    global bounds
    #On réinitialise le système à chaque cycle
    for i in range(iterations):
        Reversed = False
        maxframes = 5
        somme = 0
        Nmax = 1
        grid = Grid(N)
        newGrid = grid
        bounds = np.array([[0]*N]*N)
        Nmax = nucleate(seuil,p,N,saving=False)
        if Nmax >= N-3:
            Liste.append(1)
        else:
            Liste.append(0)
        print(i,"/",iterations,end='\r')
    print()
    print(Liste)
    file.writelines(str(100*seuil) + "\t" + str(sum(Liste)/iterations) + '\r')
    print("seuil% | Chance% | percolation%")
    print(np.round(100*seuil,decimals=2)," | ", p ," | ",sum(Liste)/iterations)

#On imprime le résultat
file = open("data.txt", "w")
for i in range(2):
    simulation(5,50,40/100,80/100,saving=False)
file.close()
