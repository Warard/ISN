import pygame
import settings

class Bird(): 


    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.velocity = 2
        #changement d'image si battement d'aile self.img_count = 0
        #self.img = self.image[0]
        self.image = pygame.image.load('imgs/bird1.png')
        self.window = window

    def show(self):
        self.window.blit(self.image,(self.x, self.y))
        self.y += (self.velocity **2) / 2

    def jump(self):
        self.y -= (self.velocity **2) * 10
        print('jumpppppp')

       
   