import random
import pygame
from settings import settings

class Pipes():
    def __init__(self, pipe_img):
        self.x = 400
        self.y = random.randint(0, 150)
        self.speed = 50

        
        self.pipe_sup = pygame.transform.flip(pipe_img, False, True)
        self.pipe_inf = pipe_img      
        
        
    def show(self, window):
        window.blit(self.pipe_sup, (self.x + self.speed, self.y-150))
        window.blit(self.pipe_inf, (self.x + self.speed, self.y + settings['free_space_btw_pipes']))
        
      
