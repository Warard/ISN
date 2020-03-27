import pygame
import settings

class Bird():
    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        # Changement d'image si battement d'aile self.img_count = 0
        # self.img = self.image[0]
        self.image = pygame.image.load('imgs/bird1.png')
        self.window = window

        # Caractéristiques de l'oiseau
        self.isJumping = False
        self.velocity = 5
        self.mass = 2
        

    def show(self):
        if self.isJumping:
            # On calcule la force F, F = 0.5 * masse * vitesse^2
            F = 0.5 * self.mass * (self.velocity ** 2)

            # On applique à la hauteur la force F et on ralentit la vitesse durant la montée
            self.y -= F
            self.velocity = self.velocity - 1

            # Si la vitesse atteint son maximum, on inverse la masse pour commencer à descendre
            if self.velocity < 0:
                self.mass = -2

            # Si la vitesse revient à son état original-1 (car on enlève 1 à chaque itération), alors on ré-initialise les variables
            if self.velocity == -6:
                self.isJumping = False
                self.velocity = 5
                self.mass = 2

        # Et enfin on affiche l'oiseau
        self.window.blit(self.image,(self.x, self.y))

    def jump(self):
        self.isJumping = True
        
    def get_mask(self):
        """
        gets the mask for the current image of the bird
        :return: None
        """
        return pygame.mask.from_surface(self.image)
        


