#main.py
"""
à rajouter:
    -Faire des balles de différente masse selon la taille
    -Enregistrer les décores dans un fichier
    -Enregistrer dernières modif
    -Frottements entre balles
    -Choisir la balle qu'on lance
"""

import pygame               #bibliothèque pour le 2d
from pygame.locals import *
from random import randint  #pour poper la balle aléatoirement
from math import *

pygame.init()

from objet import *

import sys, os
pathname = os.path.dirname(sys.argv[0])
os.chdir (os.path.abspath(pathname))
try:
    os.chdir ("ressources")
except:
    pass

clock = pygame.time.Clock() #initialise une horloge pour gerer le temps et les fps

#variables:
perte_energie = True    #False pour des balles qui rebondissent à l'infini, perte_energie comprend la rebond et les frottements
taille_dig = 70	#taille en pixel d'un mur qu'on rajoute ou qu'on retire
taille_mur = 1 	#les murs font 1 pixel
vitesse_tir = 100 #En pourcent
vitesse_balle_max = 6 #vitesse maximum au lancé avec la souris
quitter = False	#pour sortir du jeu
fps = 128 	#modifier le nombre de frame per seconde. Permet d'être plus précis, moins de tremblement, plus stable mais plus lent lorsqu'on l'augmente
m = 360 #coefficiant vitesse balle. Plus il est élevé, plus la balle saute de pixels à chaque déplacement, le jeu paraît donc accelerer.
fenetreX = 1830	#taille en pixels de la fenêtre
fenetreY = 1000
tailleFenetre = (fenetreX,fenetreY)
nbCasesX = fenetreX//taille_mur
nbCasesY = fenetreY//taille_mur
souris_clique = False
rayon = 33	#rayon de la balle, en pixel.
precision = 64	#nombre de points autour de la balle pour calculer les collisions avec les murs. entre les balles pas besoin)
liste_point_collision = []

for i in range(precision):
    liste_point_collision.append([rayon*cos(2*pi*i/precision),rayon*sin(2*pi*i/precision)])#on place les points tout autour de la balle

move =  True	#savoir si on bouge la souris lorsque l'on rajoute en enlève des murs
mode = 1	#mode 1: lancer la balle, 2: enlever des murs, 3: en rajouter, 4: rajouter des balles
dig = False	#on n'enlève et rajoute pas encore de mur

#map
grille_obstacle = make_grille(nbCasesY, nbCasesX)#on fait le font et on place les murs
   

#init objets
tab_balle = list()	#liste des balles


#Creation de la fenetre:
fenetre = pygame.display.set_mode(tailleFenetre)#on crée notre fenêtre


pygame.event.pump()#pour ne pas avoir de "ne répond plus"
fond = pygame.image.load("fond.png").convert()#on charge les images
fond = pygame.transform.scale(fond, tailleFenetre)#on met le fond à la taille de la fenêtre
mur2 = pygame.image.load("mur.png").convert()
mur = pygame.transform.scale(mur2, (taille_mur, taille_mur))
balleImage = pygame.image.load("balle.png").convert_alpha()#on charge la balle avec le transparant

fenetre.blit(fond, (0,0))#on affiche le fond
petitfond = pygame.transform.scale(fond, (taille_dig, taille_dig))#pour creuser
mur_remplacement = pygame.transform.scale(mur2, (taille_dig, taille_dig))#pour remettre les murs
image_fond = [petitfond, mur_remplacement]#permettra de creuser ou remettre les murs dans la même fonction
for i in range(nbCasesX):
    for j in range(nbCasesY):
        if grille_obstacle[j][i] == 1:
            fenetre.blit(mur, (taille_mur*i,taille_mur*j))#on affiche les murs à partir de la matrice
            

fenetre_fond = pygame.display.get_surface().copy() #Copy du fond pour effacer la balle

#________________main________________:

while quitter == False:
    tab_balle = [Balle(rayon, 600, 50, perte_energie)]#pour l'instant on a qu'une balle
    """
    #pour poser une tour de 15 balles (sur sol plat c'est mieux)
    for i in range(3):
        for j in range(5):
            tab_balle.append(Balle(rayon, 1400 + 2*rayon*i,600 - 2*rayon*j, perte_energie))
    """
    balleImage = pygame.transform.scale(balleImage, (tab_balle[0].taille*2, tab_balle[0].taille*2))#on modifie la taille de l'image balle

    balle = tab_balle[0]
    fenetre.blit(balleImage, (balle.position_X-balle.taille,balle.position_Y-balle.taille))
    pygame.display.flip()#on rafraichit la fenêtre pour afficher les images qui étaient dans le buffer

    replay = False #pour recommencer
    while quitter == False and replay == False: #boucle de jeu, on sort pour recommencer ou quitter
        for event in pygame.event.get():    #on parcourt tous les évènements pygame (souris, clavier etc) pour savoir si on est intervenu
            if event.type == pygame.QUIT:   #si on clique sur la croix ça quitte
                quitter = True

            if mode == 1:                   #mode pour lance la première balle
                if event.type == pygame.MOUSEBUTTONDOWN:#si on clique
                    souris_clique = True
                    souris_clique1_X = event.pos[0] #on prend les coordonnés de la souris
                    souris_clique1_Y = event.pos[1]

                if souris_clique == True and event.type == pygame.MOUSEBUTTONUP and not(event.pos[0] == souris_clique1_X and event.pos[1] == souris_clique1_Y): #si on relache le clique à un endroit différent:
                    souris_clique = False
                    souris_clique2_X = event.pos[0]
                    souris_clique2_Y = event.pos[1]

                    vitesse_X = souris_clique2_X - souris_clique1_X #on calcule la différence entre le clique et le relachement
                    vitesse_Y = souris_clique1_Y - souris_clique2_Y

                    balle = tab_balle[0]#changer en la balle la plus proche lors du premier clique (algo dans tower defender)
                    balle.vitesse = norm((vitesse_X,vitesse_Y))#on calcule la vitesse va la norme (sqrt(x**2 + y**2))
                    if balle.vitesse:#normalement la balle a toujours une vitesse mais au où
                        balle.direction = atan2(vitesse_Y/balle.vitesse,vitesse_X/balle.vitesse)#angle de la balle

                    balle.vitesse *= vitesse_tir/8192   #on réduit
                    if balle.vitesse > vitesse_balle_max:#si on a tiré trop fort on est limité
                        balle.vitesse = vitesse_balle_max
                            
            elif mode == 2 or mode == 3: # 2: creuser; 3: rajouter de la matière
                if event.type == pygame.MOUSEMOTION:
                    move = True #on bouge la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dig = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    dig = False


            if event.type == pygame.KEYDOWN:
                if event.key == K_1 or event.key == K_AMPERSAND: #appuie sur 1 ou & (1 sans maj)
                    mode = 1
                    print("propulser la balle.")
                elif event.key == K_2 or event.key == 233: #appuie sur 2 ou é
                    mode = 2
                    dig = False
                    move = True
                    print("creuser")
                elif event.key == K_3 or event.key == K_QUOTEDBL: #3 ou "
                    mode = 3
                    dig = False
                    move = True
                    print("rajouter mur")
                elif event.key == K_4 or event.key == K_QUOTE: #4 ou '
                    tab_balle.append(Balle(rayon, randint(200, fenetreX - 200), 50, perte_energie)) #on crée une nouvelle balle

                elif event.key == K_ESCAPE: #recommencer
                    replay = True
        if dig and move and mode >= 2:  #creuser ou rajouter des murs
            try:
                fenetre.blit(fenetre_fond,(0,0))
                x,y = event.pos
                fenetre.blit(image_fond[mode - 2],(x-taille_dig//2,y-taille_dig//2))
                for i in range(taille_dig):
                    for j in range(taille_dig):
                        grille_obstacle[(y+j-taille_dig//2)//taille_mur][(x+i-taille_dig//2)//taille_mur] = mode - 2 
                fenetre_fond = pygame.display.get_surface().copy() #Copy du fond pour effacer la balle
                move = False
            except:#en dehors de la fenetre
                pass
            
        num = 1
        longueur = len(tab_balle)
        for balle in tab_balle: #pour chaque balle
            balle.gravite(m, 1/fps) #on applique la gravité
            balle.deplacement(m, 1/fps) #on la déplace
            try:
                #Collision
                testCollision = False
                for num_balle in range(num, longueur):#on teste chaque couple qu'une fois
                    if (balle.position_X - tab_balle[num_balle].position_X)**2 + (balle.position_Y - tab_balle[num_balle].position_Y)**2 < (balle.taille + tab_balle[num_balle].taille)**2 and se_rapproche(balle, tab_balle[num_balle], 1/fps, m):#si les balles se touchent et se rapprochent
                        collision_balles(balle, tab_balle[num_balle]) #collision entre 2 balles
                num += 1
                for i in range(precision):
                    if grille_obstacle[int((balle.position_Y+liste_point_collision[int(i)][1])/taille_mur)][int((balle.position_X+liste_point_collision[int(i)][0])/taille_mur)] != 0:  #on regarde si la balle est en collision avec un mur
                        testCollision = True
                if testCollision == True:
                    collision_mur(balle, grille_obstacle, liste_point_collision, m, precision, taille_mur, fenetreX) #on traite la collision
            except IndexError:#le balle sort de l'écran, ne fonctionne qu'à droite et en bas à  cause des indices négatifs dans les listes, faudra le changer
                posx = balle.position_X
                posy = balle.position_Y
                if posx < balle.taille or posx > fenetreX - balle.taille or posy < balle.taille or posy > fenetreY - balle.taille:#on supprime la balle si elle est sortie de l'écran (condition non utile)
                    tab_balle.remove(balle)

                if tab_balle == []: #si plus de balle on recommence
                    replay = True
        #____________________________
        fenetre.blit(fenetre_fond, (0,0))   #on affiche le fond
        for balle in tab_balle: #on affiche chaque balle
            fenetre.blit(balleImage, (balle.position_X-balle.taille, balle.position_Y-balle.taille))
               
        pygame.display.flip()   #on rafraîchit
        clock.tick(fps)         #on modère les fps
        #ça serait peut-être plus interessant de ne pas limiter les fps et de calculer la vitesse de la balle. On serait ainsi plus précis avec peu de balles et on pourrait avoir plus de balles. Seul problème, le processeur risque de ne pas aimer.

pygame.quit()   #on quitte pygame pour sortir proprement
