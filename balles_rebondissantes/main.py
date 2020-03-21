import pygame
from pygame.locals import *
from random import randint
from math import *
from time import *

pygame.init()

from objet import *

import sys, os
pathname = os.path.dirname(sys.argv[0])
os.chdir (os.path.abspath(pathname))
try:
    os.chdir ("ressources")
except:
    pass

clock = pygame.time.Clock() #initialise une horloge pour gerer le temps

#variables:
perte_energie = True
taille_dig = 70
taille_mur = 1 
vitesse_tir = 100 #En pourcent
vitesse_balle_max = 5
quitter = False
fps = 128 
m = 330 #coefficiant vitesse balle.
fenetreX = 1830#1230
fenetreY = 1000#630
tailleFenetre = (fenetreX,fenetreY)
nbCasesX = fenetreX//taille_mur
nbCasesY = fenetreY//taille_mur
souris_clique = False
rayon = 33
precision = 64
liste_point_collision = []

move =  True 
mode = 1
dig = False

for i in range(precision):
    liste_point_collision.append([rayon*cos(2*pi*i/precision),rayon*sin(2*pi*i/precision)])

#map
grille_obstacle = make_grille(nbCasesY, nbCasesX)
   

#init objets
tab_balle = list()
#temps = Gestion_du_temps()


#Creation de la fenetre:
fenetre = pygame.display.set_mode(tailleFenetre)


pygame.event.pump()
fond = pygame.image.load("fond.png").convert()
fond = pygame.transform.scale(fond, tailleFenetre)
mur2 = pygame.image.load("mur.png").convert()
mur = pygame.transform.scale(mur2, (taille_mur, taille_mur))
balleImage = pygame.image.load("balle.png").convert_alpha()

fenetre.blit(fond, (0,0))
petitfond = pygame.transform.scale(fond, (taille_dig, taille_dig))
mur_remplacement = pygame.transform.scale(mur2, (taille_dig, taille_dig))
image_fond = [petitfond, mur_remplacement]
for i in range(nbCasesX):
    for j in range(nbCasesY):
        if grille_obstacle[j][i] == 1:
            fenetre.blit(mur, (taille_mur*i,taille_mur*j))
            

fenetre_fond = pygame.display.get_surface().copy() #Copy du fond pour effacer la balle

#______________main____________:

while quitter == False:
    tab_balle = [Balle(rayon, 370, 50, perte_energie)]
    balleImage = pygame.transform.scale(balleImage, (tab_balle[0].taille*2, tab_balle[0].taille*2))
    #tab_balle[0].__init__(rayon, 370, 70)
    #temps.__init__()

    balle = tab_balle[0]
    fenetre.blit(balleImage, (balle.position_X-balle.taille,balle.position_Y-balle.taille))
    pygame.display.flip()
    pygame.event.pump()

    testArret = 0
    replay = False
    while quitter == False and testArret < 232 and replay == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter = True

            if mode == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    souris_clique = True
                    souris_clique1_X = event.pos[0]
                    souris_clique1_Y = event.pos[1]

                if souris_clique == True and event.type == pygame.MOUSEBUTTONUP and not(event.pos[0] == souris_clique1_X and event.pos[1] == souris_clique1_Y):
                    souris_clique = False
                    souris_clique2_X = event.pos[0]
                    souris_clique2_Y = event.pos[1]

                    
                    vitesse_X = souris_clique2_X-souris_clique1_X
                    vitesse_Y = souris_clique1_Y-souris_clique2_Y

                    balle = tab_balle[0]#changer en la balle la plus proche lors du premier clique (algo dans tower defender)
                    balle.vitesse = sqrt(vitesse_X**2+vitesse_Y**2)
                    balle.direction = atan2(vitesse_Y/balle.vitesse,vitesse_X/balle.vitesse)

                    balle.vitesse *= 0.0001*vitesse_tir
                    if balle.vitesse > vitesse_balle_max:
                        balle.vitesse = vitesse_balle_max
                            
            elif mode == 2 or mode == 3: # 2: creuser; 3: rajouter de la matière
                if event.type == pygame.MOUSEMOTION:
                    move = True
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
                elif event.key == K_3 or event.key == K_QUOTEDBL:
                    mode = 3
                    dig = False
                    move = True
                    print("rajouter mur")
                elif event.key == K_4 or event.key == K_QUOTE:
                    tab_balle.append(Balle(rayon, randint(200, fenetreX - 200), 50, perte_energie))

                elif event.key == K_ESCAPE: #recommencer
                    replay = True
        if dig and move and mode >= 2:
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
            
        if event.type == pygame.QUIT:
            quitter = True 
        """        
        if abs(cos(balle.direction)*balle.vitesse) < 0.005 and abs(sin(balle.direction)*balle.vitesse) < 0.25:
            testArret += 1
        else:
            testArret = 0
        """
        
        num = 1
        longueur = len(tab_balle)
        for balle in tab_balle:
            balle.gravite(m, 1/fps)
            balle.deplacement(m, 1/fps)
            try:
                #Collision
                testCollision = False
                for num_balle in range(num, longueur):
                    if (balle.position_X - tab_balle[num_balle].position_X)**2 + (balle.position_Y - tab_balle[num_balle].position_Y)**2 < (balle.taille + tab_balle[num_balle].taille)**2 and se_rapproche(balle, tab_balle[num_balle], 1/fps, m):
                        start = (balle.position_X, balle.position_Y)
                        start2 = (tab_balle[num_balle].position_X, tab_balle[num_balle].position_Y)

                        end, end2 = collision_balles(balle, tab_balle[num_balle]) #collision entre 2 balles

                        #pygame.draw.line(fenetre, (0,255,0), start, end, 5)
                        #pygame.draw.line(fenetre, (0,0,255), start2, end2, 5)

                        
                        #pygame.display.flip()
                        #input()
                num += 1
                for i in range(precision):
                    if grille_obstacle[int((balle.position_Y+liste_point_collision[int(i)][1])/taille_mur)][int((balle.position_X+liste_point_collision[int(i)][0])/taille_mur)] != 0:
                        testCollision = True
                if testCollision == True:
                    collision_mur(balle, grille_obstacle, liste_point_collision, m, precision, taille_mur, fenetreX)
            except IndexError:
                posx = balle.position_X
                posy = balle.position_Y
                if posx < balle.taille or posx > fenetreX - balle.taille or posy < balle.taille or posy > fenetreY - balle.taille:#on supprime la balle si elle est sortie de l'écran
                    tab_balle.remove(balle)

                if tab_balle == []:
                    replay = True
                        
        fenetre.blit(fenetre_fond, (0,0))
        for balle in tab_balle:
            fenetre.blit(balleImage, (balle.position_X-balle.taille, balle.position_Y-balle.taille))
               
        pygame.display.flip()
        clock.tick(fps)                    

pygame.quit()
