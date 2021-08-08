import pygame
from . import constants as C
from . import tools

pygame.init()
pygame.display.set_mode((C.SCREEN_W,C.SCREEN_W))

GRAPHICS=tools.load_graphics('resources/graphics')