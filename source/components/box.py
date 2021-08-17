import pygame
from .. import tools,setup
from ..import constants as C


class Box(pygame.sprite.Sprite):
    def __init__(self,x,y,box_type):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.box_type=box_type

        self.frame_rects=[
            (384,0,16,16),
            (400,0,16,16),
            (416,0,16,16),
            (432,0,16,16),
        ]

        self.frames=[]
        for frame_rect in self.frame_rects:
            self.frames.append(tools.get_image(setup.GRAPHICS['tile_set'],*frame_rect,(0,0,0),C.BRICK_MULTI))
        self.frame_index=0
        self.image=self.frames[self.frame_index]
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

