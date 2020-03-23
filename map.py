from settings import settings
import pygame
import random


class Background():
    """
    La classe Background permet d'afficher le fond et le sol du jeu à travers ses méthodes:
    - draw_brackground
    - draw_base
    - move_base
    """
    # Caractéristiques du futur objet
    def __init__(self, base_img, bg_img, window, x=0):
        """
        La méthode __init__ définie différentes variables:
        - x: la position horizontale du sol (utile pour le déffilement)
        - base_img: l'image du sol
        - bg_img: l'image de fond
        - window: la fenêtre ou on doit afficher nos éléments
        - speed: la vitesse à laquelle notre sol défille
        """
        self.x = 0
        self.base_img = base_img
        self.bg_img = bg_img
        self.window = window
        self.speed = settings['speed']

    # Affiche le fond
    def draw_background(self):
        """La méthode draw_background permet d'afficher l'image de fond"""
        self.window.blit(self.bg_img, (0, 0))

    # Affiche la base
    def draw_base(self):
        """La méthode draw_base permet d'afficher l'image de sol"""
        self.window.blit(self.base_img, (self.x, 512))
        # print('base  x position = ', self.x)

    # Déplace la base
    def move_base(self):
        """la méthode move_base permet de déplacer vers la gauche le sol à la même vitesse que les tuyaux"""
        self.x -= self.speed


class Pipes():
    """
    La classe Pipes permet de générer et d'afficher les tuyaux sur notre fenêtre à travers ses méthodes:
    - show
    - move
    """
    def __init__(self, pipe_img, x):
        """
        La méthode __init__ définie différentes variables:
        - x: la position horizontale des tuyaux
        - y: la hauteur aléatoire du tuyau supérieur
        - speed: la vitesse à laquelle se déplace les tuyaux vers la gauche
        - pipe_img_y_height: la taille de l'image à afficher, à soustraire à la position ou on souhaite l'afficher
        - vertical_space_btw_pipes: la taille de l'ouverture entre les deux tuyaux
        - pipe_inf: contient l'image du tuyau inférieur
        - pipe_sup: contient l'image du tuyau supérieur, qui est l'image du tuyau inférieur inversée
        """
        self.x = x
        self.y = random.randint(settings['min_random_y_pipe_spawn'], settings['max_random_y_pipe_spawn'])
        self.speed = settings['speed']

        # Les variables qui doivent être importées d'autres fichiers sont stockées dans des variables, pour des soucis de performance
        self.pipe_img_y_height = settings['pipe_img_y_height']
        self.vertical_space_btw_pipes = settings['vertical_space_btw_pipes']

        # Le tuyau inférieur est celui que nous importons, le supérieur doit subir une rotation horizontale
        self.pipe_inf = pipe_img
        self.pipe_sup = pygame.transform.flip(pipe_img, False, True)

    # Affiche le tuyeau
    def show(self, window):
        """La méthode show de la classe Pipes permet d'afficher le tuyau supérieur et le tuyau inférieur sur notre fenêtre"""
        window.blit(self.pipe_sup, (self.x, self.y - self.pipe_img_y_height))
        window.blit(self.pipe_inf, (self.x, self.y + self.vertical_space_btw_pipes))
        # print('showing new pipes in x= ', self.x, 'y=', self.y)

    # Déplace le tuyeau
    def move(self):
        """La méthode move de la classe Pipes permet de déplacer vers la gauche les deux parties du tuyau"""
        self.x -= self.speed
        # print('Pipes in movements !')
