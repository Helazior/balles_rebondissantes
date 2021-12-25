# balles_rebondissantes
Reproduction physique de balles rebondissantes qui peuvent rentrer en collision dans un espace à 2 dimensions.  
Démo : https://youtu.be/z-GAP2R4Dvg


Pour mieux comprendre les collisions, je me suis amusé à reproduire des balles rebondissantes qui peuvent rentrer en collision dans un espace à 2 dimensions. Ce programme est codé en python avec le module Pygame pour la 2D. J'ai tout repris de zéro sans regarder les algorithmes et solutions existantes sur Internet, pour vraiment pouvoir y réfléchir. Pour utiliser le programme: le programme commence dans le mode 1, pour changer de mode taper: 1, 2 ou 3 (mode 1, 2 et 3) mode 1: permet de lancer la première balle. Il suffit de cliquer sur l'écran, de maintenir le clique en bougeant la souris pour donner une direction et une vitesse puis de relâcher le clique. mode 2: permet de creuser dans le sol pour modifier l'environnement. Il faut maintenir le clique en bougeant la souris à l'endroit où l'on veut creuser. mode 3: rajouter de la matière. C'est l’opposé du mode 2. Même utilisation Appuyer sur '4' pour faire apparaître une nouvelle balle (la position en abscisse est aléatoire).

Pour changer les paramètres du jeu (taille des balles, rebond, vitesse du jeu etc. Il faut se rendre dans le main.py directement).

Cette version fonctionne, mais reste à rajouter:
-Les balles plus grosses doivent avoir un masse plus importante
-Pouvoir enregistrer le décor dans un fichier.
-Enregistrer la dernière modification pour pouvoir revenir en arrière.
-Mettre des frottements entre les balles.
-Implémenter d'autres formes géométriques.
