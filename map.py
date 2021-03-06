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
    def __init__(self, bg_img, window):
        """
        La méthode __init__ définie différentes variables:
        - x: la position horizontale du sol (utile pour le déffilement)
        - x_background: la position horizontale du fond de l'écran
        - base_img: l'image du sol
        - bg_img: l'image de fond
        - window: la fenêtre ou on doit afficher nos éléments
        - speed: la vitesse à laquelle notre sol défille
        """
        self.x = 0
        self.x = 0
        self.bg_img = bg_img
        self.window = window
        self.speed = settings['speed']

    # Affiche le fond
    def draw_background(self):
        """La méthode draw_background permet d'afficher l'image de fond"""
        self.window.blit(self.bg_img, (self.x, 0))

    # Déplace le fond
    def move_background(self):
        """La méthode move_background permet de faire déffiler l'image de fond"""
        self.x -= 0.1 * self.speed


class Base():
    def __init__(self, base_img, window):
        """
        La méthode __init__ définie différentes variables:
        - x: la position horizontale du sol (utile pour le déffilement)
        - x_background: la position horizontale du fond de l'écran
        - base_img: l'image du sol
        - bg_img: l'image de fond
        - window: la fenêtre ou on doit afficher nos éléments
        - speed: la vitesse à laquelle notre sol défille
        """
        self.x = 0
        self.base_img = base_img
        self.window = window
        self.speed = settings['speed']

    # Affiche la base
    def draw_base(self):
        """La méthode draw_base permet d'afficher l'image de sol"""
        self.window.blit(self.base_img, (self.x, 512))
        # print('base  x position = ', self.x)

    # Déplace la base
    def move_base(self):
        """La méthode move_base permet de déplacer vers la gauche le sol à la même vitesse que les tuyaux"""
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
        self.PIPE_BOTTOM = pipe_img
        self.top = 0
        self.bottom = 0

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

    def collide(self, bird, win):
        """
        returns if a point is colliding with the pipe
        :param bird: Bird object
        :return: Bool
        """
        bird_mask = bird.get_mask()
        mask_pipe_sup = pygame.mask.from_surface(self.pipe_sup)
        mask_pipe_bottom = pygame.mask.from_surface(self.pipe_inf)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(mask_pipe_bottom, bottom_offset)
        t_point = bird_mask.overlap(mask_pipe_sup, top_offset)

        if b_point or t_point:
            return True
        return False
