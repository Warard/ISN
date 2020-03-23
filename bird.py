import pygame
import settings

class bird: 

    image=pygame.image.load('imgs/bird1.png')


    def _init_(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.image[0]

    def jump(self):
        self.velocity = -10
        self.tick_count = 0
        self.height = self.y

   
   