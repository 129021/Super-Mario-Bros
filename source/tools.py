#工具和游戏主控

import pygame
import random
import os

class Game:
    def __init__(self):

        self.screen=pygame.display.get_surface()
        self.clock=pygame.time.Clock()

    def run(self,GRAPHICS):

        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.display.quit()
                elif event.type==pygame.KEYDOWN:
                    self.keys=pygame.key.get_pressed()
                elif event.type==pygame.KEYUP:
                    self.keys=pygame.key.get_pressed()
            self.screen.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            image=get_image(GRAPHICS['mario_bros'],145,32,16,16,(0,0,0),5)
            self.screen.blit(image,(300,300))
            pygame.display.update()
            self.clock.tick(60)


def load_graphics(path,accept=('jpg','png','bmp','gif')):
    graphics={}
    for pic in os.listdir(path):
        name,ext=os.path.splitext(pic)
        if ext.lower()in accept:
            img=pygame.image.load(os.path.join(path,pic))
            if img.get_alpha():
                img=img.convert_alpha()
            else:
                img=img.convert()
            graphics[name]=img
    return graphics

def get_image(sheet,x,y,width,height,colorkey,scale):
    image=pygame.Surface((width,height))
    image.blit(sheet,(0,0),(x,y,width,height)) #0,0代表画到哪个位置,x,y,w,h代表sheet里哪个区域要被取出来
    image.set_colorkey(colorkey)
    image=pygame.tranform.scale(image,(int(width*scale),int(height*scale)))
    return image


