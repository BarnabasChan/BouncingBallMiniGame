import pygame
import pygame.gfxdraw
from Constants import *

class Button:
    def __init__(self, rect, text, command):
        self.x, self.y, self.w, self.h = self.rect = rect
        self.text = button_font.render(text, True, black)
        self.tx = self.x + (self.w - self.text.get_width())/2
        self.ty = self.y + (self.h - self.text.get_height())/2
        self.cmd = command
        self.p1 = (
            (self.x-50, self.y),
            (self.x-50, self.y+self.h),
            (self.x-10, self.y+self.h/2)
        )
        self.p2 = (
            (self.x+self.w+50, self.y),
            (self.x+self.w+50, self.y+self.h),
            (self.x+self.w+10, self.y+self.h/2)
        )

    def draw(self, window):
        pygame.draw.rect(window, white, self.rect)
        pygame.draw.rect(window, black, self.rect, 2)
        window.blit(self.text, (self.tx, self.ty))

    def selected(self, window):
        pygame.gfxdraw.filled_polygon(window, self.p1, red)
        pygame.gfxdraw.filled_polygon(window, self.p2, red)
