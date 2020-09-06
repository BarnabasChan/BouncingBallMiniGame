from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from States import *
from Constants import *

pygame.init()

state = StateController()

joystick_count = 0
level.joysticks = []

window = pygame.display.set_mode((win_width, win_height))

while state.running:

    # event handle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.running = False
        else:
            state.handle(event)

    # detect for new joystick
    new_count = pygame.joystick.get_count()
    if new_count > joystick_count:
        for i in range(joystick_count, new_count):
            new_joystick = pygame.joystick.Joystick(i)
            new_joystick.init()
            level.joysticks.append(new_joystick)
            print(new_joystick)
            joystick_count = new_count

    state.update() # TODO: see if update and draw can be merge together

    state.draw(window)
    pygame.display.update()

pygame.quit()
