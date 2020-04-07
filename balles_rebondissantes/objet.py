from math import *
import sys, os

pathname = os.path.dirname(sys.argv[0])
os.chdir (os.path.abspath(pathname))
try:
    os.chdir ("ressources")
except: #idle a un comportement bizarre avec ça, alors je préfère couvrir tous les cas, même si je ne l'utilise pas souvent.
    pass


def prod_scal(u,v):
    return sum([x * y for x, y in zip(u, v)])

def norm(u):
    return sqrt(prod_scal(u,u))

#map
def make_grille(nbCasesY, nbCasesX):
    grille_obstacle = [0]*nbCasesY
    for i in range (nbCasesY):
        grille_obstacle[i] = [0]*nbCasesX
    
    for i in range(nbCasesX):
        for j in range(nbCasesY):
            #pour modifier le fond au début
            grille_obstacle[j][i] = ((i-nbCasesX//2)**2>-500*j+400000) #parabole
            #grille_obstacle[j][i] = 100 < j

    return grille_obstacle
    
    
def sgn(x):
    return 1- 2*(x<0) - (x==0)

class Balle():
    acceleration = 9.81
    def __init__(self, rayon, posx, posy, perte_energie):
        self.rebond = 1 - 0.1*perte_energie  #coefficiant rebond
        self.frottement = 0.1*perte_energie
        self.vitesse = 0
        self.position_X = posx 
        self.position_Y = posy
        self.direction = 0
        self.taille = rayon

    def deplacement(self, m, temps): 
        self.position_X += cos(self.direction)*self.vitesse*temps * m
        self.position_Y -= sin(self.direction)*self.vitesse*temps* m

    def gravite(self,m,temps):
        vx = cos(self.direction)*self.vitesse
        vy = sin(self.direction)*self.vitesse
        vy -= self.acceleration * temps        

        self.vitesse = norm((vx,vy))
        self.direction = (atan2(vy/self.vitesse,vx/self.vitesse) + pi) % (2*pi) - pi
  
    def frot_rebond(self, angle_vecteur_collision): #perte d'energie lorsd'une collision contre un mur
        coeff = abs(cos(angle_vecteur_collision - self.direction))  #la perte d'energie varie selon l'écrasement de la balle, donc selon l'angle avec lequel elle frappe le mur
        vx = cos(angle_vecteur_collision)*self.vitesse
        vy = sin(angle_vecteur_collision)*self.vitesse

        if abs(((1 - coeff)*self.frottement)*sgn(vx)*(1+abs(vy))) < abs(vx):
            vx -= ((1 - coeff)*self.frottement)*sgn(vx)*(1+abs(vy))
        else:
            vx*=0.9
        vy *= (self.rebond + (1 - self.rebond)*coeff)*self.rebond
        self.vitesse = norm((vx,vy))
        new_angle = atan2(vy,vx)

        self.direction = self.direction + angle_vecteur_collision - new_angle


def se_rapproche(balle, balle2, temps, m):
    #si les balles s'éloignent ne pas faire de collision 
    posx = balle.position_X
    posy = balle.position_Y
    posx2 = balle2.position_X
    posy2 = balle2.position_Y

    nposx = posx + cos(balle.direction)*balle.vitesse*temps * m
    nposy = posy - sin(balle.direction)*balle.vitesse*temps* m
    nposx2 = posx2 + cos(balle2.direction)*balle2.vitesse*temps * m
    nposy2 = posy2 - sin(balle2.direction)*balle2.vitesse*temps* m

    dist = norm((posx - posx2, posy - posy2))
    ndist = norm((nposx - nposx2, nposy - nposy2))

    return ndist < dist

###________________Collisions balles___________________:
def collision_balles(balle, balle2):
    #de la balle 1 vers la balle 2:
    vect_collision = (balle.position_X - balle2.position_X, balle.position_Y - balle2.position_Y)
    angle_balle = balle.direction
    angle_balle2 = balle2.direction
    angle_collision =  - ((atan2(vect_collision[1], vect_collision[0])+pi) % (2*pi) - pi)
    #angle a = l'angle entre le vecteur directeur de la balle et le vecteur qui relie le centre des 2 balles
    cosa = cos(angle_balle - angle_collision)
    p_balle = balle.vitesse #p_balle = puissance de la balle; à rajouter: puissance transmis P = 1/2*mv² au lieu de = v
    p_t = cosa * p_balle * sqrt(balle.rebond) #puissance transmise = projection de la puissance de balle1 sur le vecteur collision
    b = angle_collision #angle cercle trigo en radian du vecteur de balle 1 à balle 2
    vx = cos(angle_balle) * balle.vitesse
    avx = vx
    vx -= cos(b)*p_t #ça sera modifié selon la masse des 2 balles
    vy = sin(angle_balle)*balle.vitesse
    
    avy = vy
    vy -= sin(b)*p_t
    
    vx2 = cos(angle_balle2)*balle2.vitesse
    avx2 = vx2
    vx2 += cos(b)*p_t
    vy2 = sin(angle_balle2)*balle2.vitesse
    avy2 = vy2
    vy2 += sin(b)*p_t

    #de la balle 2 vers la balle 1:
    angle_collision2 = (b + 2*pi) %(2*pi) - pi 
    
    cosa = cos(angle_balle2 - angle_collision2)
    p_balle2 = balle2.vitesse
    p_t = cosa * p_balle2
    b = angle_collision2
    vx2 -= cos(b)*p_t
    vy2 -= sin(b)*p_t
    vx += cos(b)*p_t
    vy += sin(b)*p_t
    
    balle.vitesse = norm((vx, vy))
    balle2.vitesse = norm((vx2, vy2))
    balle.direction = atan2(vy,vx)
    balle2.direction = atan2(vy2,vx2)

    #on corrige la position des balles qui sont en collision en les décollants
    dist = norm((balle.position_X - balle2.position_X, balle.position_Y - balle2.position_Y))
    enfoncement = balle.taille - 0.5 * dist
    enfoncement2 = balle2.taille - 0.5 * dist
    
    tpx = cos(angle_collision)*enfoncement
    tpy = sin(angle_collision)*enfoncement
    tpx2 = cos(angle_collision2)*enfoncement2
    tpy2 = sin(angle_collision2)*enfoncement2
    
    balle.position_X += tpx
    balle.position_Y -= tpy
    balle2.position_X += tpx2
    balle2.position_Y -= tpy2


###____________________Collision mur____________________:
def collision_mur(balle, grille_obstacle,liste_point_collision, m, precision, taille_mur, fenetreX):

    points_collision = []
    nombreDePointsCollision = 0
    for i in range(-1,len(liste_point_collision)-1):
        
        if grille_obstacle[int((balle.position_Y+liste_point_collision[i][1])/taille_mur)][int((balle.position_X+liste_point_collision[i][0])/taille_mur)] + grille_obstacle[int((balle.position_Y+liste_point_collision[i+1][1])/taille_mur)][int((balle.position_X+liste_point_collision[i+1][0])/taille_mur)] == 1:  #si un point autour de la balle est en collision avec le mur
            points_collision.append([.5*(liste_point_collision[i][0]+liste_point_collision[i+1][0]),.5*(liste_point_collision[i][1]+liste_point_collision[i+1][1])])    #on rajoute ce point à la liste

        if grille_obstacle[int((balle.position_Y+liste_point_collision[i][1])/taille_mur)][int((balle.position_X+liste_point_collision[i][0])/taille_mur)] == 1:
            nombreDePointsCollision += 1
    enfoncement = balle.taille * nombreDePointsCollision/len(liste_point_collision)
    if len(points_collision) >= 2:
        #vecteur directeur:
        vecteur_collision = [0,0]
        vecteur_collision[0] = points_collision[-1][0]-points_collision[0][0]
        vecteur_collision[1] = points_collision[-1][1]-points_collision[0][1]
        angle_vecteur_collision = pi - atan2(vecteur_collision[1],vecteur_collision[0])
        direction = balle.direction
        #change de direction et ralentir la balle:
        balle.direction = (2*angle_vecteur_collision - balle.direction)


        if angle_vecteur_collision >= pi:
            angle_vecteur_collision -= pi

        direction -= angle_vecteur_collision

        angle_vecteur_tp = 0
        if direction > -pi and direction < 0:
            angle_vecteur_tp = angle_vecteur_collision + pi/2
 
        elif direction < -pi or direction > 0:
            angle_vecteur_tp = angle_vecteur_collision - pi/2

        if direction != 0 and direction != pi:
            #tp hors du mur:
            balle.position_X += enfoncement*cos(angle_vecteur_tp)
            balle.position_Y -= enfoncement*sin(angle_vecteur_tp)
        
        balle.frot_rebond(angle_vecteur_collision)
        balle.vitesse *= (balle.vitesse > 0)

    elif len(points_collision) != 0:
        print("erreur, len(points_collision) <  2")
        print(points_collision)

    else:
        #dans le mur
        #trouver le chemin le plus court pour sortir et sortir
        precision = balle.taille
        succes = False
        for rayon in range (2*balle.taille, fenetreX, 2*balle.taille):
            for i in range (int(precision*rayon**(1/4))):
                x = int(balle.position_X + rayon*cos(2*pi*i/precision))
                y = int(balle.position_Y + rayon*sin(2*pi*i/precision))
                try:
                    if x >= 0 and y >= 0 and grille_obstacle[y//taille_mur][x//taille_mur] == 0:
                        balle.position_X = x
                        balle.position_Y = y
                        succes = True
                        break
                except:
                    pass

            if succes == True:
                break
        if succes == False:
            print("fail")


    testCollision = True 
    repet = 0


