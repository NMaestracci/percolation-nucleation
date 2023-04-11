# Code python pour implémenter la percolation dans une grille bidimensionnelle aléatoire avec ou sans convolution
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def randomGrid(N,solidity):
    """Grille aléatoire 0 ou 100.
    0 représente un obstacle, 100 représente une case libre pour le liquide"""
    return np.random.choice([0, 100], N * N,p=[solidity, 1 - solidity]).reshape(N, N)

def update(frameNum, img, grid, N, frame, maxframes=10, convolutionFactor=10):

    #Pour 'maxframes' images, faire une convolution (moyenne locale)
    if frameNum < maxframes :
        grid = mean(grid,2,convolutionFactor)

    #Eclaircir le système en 0 et 100
    elif frameNum == maxframes :
        grid = round(grid,N)

    #Faire couler le fluide parfait
    else:
        percolation(grid,N)

    #Mettre a jour la grille animée
    img.set_data(grid)

    return img


def percolate(grid,N,saving=False,convolutionFactor=10):
    frame = 0
    maxframes = 5
    frameNum = 0
    fig, ax = plt.subplots()      

    if saving == True:
        f = "percolation2.png" 
        writergif = animation.PillowWriter()

    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, frame, maxframes, convolutionFactor),
                                  frames=2*N,
                                  interval=1,
                                  # save_count=50, 
                                  repeat=False,
                                  blit = False)

    #Soit on sauvegarde, soit on montre l'animation
    if saving == True:
        print('sauvegarde de l\'animation...')

        ani.save(f, writer=writergif)
        print('animation sauvegardée.')
    else:
        plt.show(block=False)
        plt.pause(100)
        plt.close()

    return percolation(grid,N)
    

def mean(grid,N,convolutionFactor=1000):
    """
    Moyenne locale. On utilise des conditions aux limites ouvertes. Techniquement cette géométrie est équivalent à un Tore pour ce qui est de la moyenne, mais à un plan fini en ce qui concerne le liquide.
    """
    N = len(grid[0])
    copygrid = grid
    for i in range(N):
        for j in range(N):

            total =     (copygrid[i, (j - 1) % N] + copygrid[i, (j + 1) % N] +
                         copygrid[(i - 1) % N, j] + copygrid[(i + 1) % N, j] +
                         copygrid[(i - 1) % N, (j - 1) % N] + copygrid[(i - 1) % N, (j + 1) % N] +
                         copygrid[(i + 1) % N, (j - 1) % N] + copygrid[(i + 1) % N, (j + 1) % N])
            grid[i,j] = grid[i, j] + (total - 400) / convolutionFactor
            if copygrid[i,j] >= 100:
                grid[i,j] = 100
            elif copygrid[i,j] <= 0:
                grid[i,j] = 0
    return grid


def round(grid,N):
    """ On arrondi à 0 ou 100 pour faciliter le calcul sur percolation() """
    for i in range(0,N):
        for j in range(0,N):
            if grid[i,j] >= 30:
                grid[i,j] = 100
            else:
                grid[i,j] = 0
    return grid

def percolation(grid,N):
    """ On fait mouvoir le liquide depuis le haut de la grille, une case par une case, si une case adjacente est libre. """
    Nmax = 0
    for i in range(0,N):
        #premiere ligne 0
        grid[0,i] = 0
        grid[1,i] = 50

        #premiere et derniere colonne zero
        # grid[i][0] == 0
        # grid[i][N-1] == 0
    count = 0
    for i in range(1,N-1):
        for j in range(1,N-1):
            if grid[i,j] == 50:
                Nmax = max(Nmax,i)
            if grid[i,j] >= 90:
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
    if Nmax > N-3 or count == 0:
    	plt.close()
    return Nmax

def simulation(iterations,N,solidity,convolutionFactor=1000,save=False,retour_texte=False,):
    """ Simple boucle pour exécuter l'animation plusieurs fois"""
    Liste = []

    for i in range(iterations):
        maxframes = 5
        percole = False
        frame = 0
        Nmax = 1
        grid = randomGrid(N,solidity)
        newGrid = grid
        p = percolate(grid,N,save,convolutionFactor)
        if p >= N-3:
            Liste.append(1)
        else:
            Liste.append(0)
        print(i,"/",iterations,end='\r')
    print()
    print(Liste)
    file = open("data.txt", "w")
    file.writelines(str(100*solidity) + "\t" + str(convolutionFactor) + "\t" + str(sum(Liste)/iterations))
    print("opacity% | convolution | percolation%")
    print(100*solidity," | ",convolutionFactor ," | ",sum(Liste)/iterations)
    file.close()

for i in range(1,8):
    for j in range(0,9):
        simulation(40,200,(39+j+i)/100,convolutionFactor=64/2**i,save=False)
