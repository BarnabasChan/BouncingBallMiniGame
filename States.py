import pygame
import random

from Constants import *
from Widgets import *
from Game import *

class State:
    def __init__(self, controller): self.ctrl = controller
    def draw(self, window): window.fill(black)
    def handle(self, event): pass
    def update(self, dt): pass

class MenuState(State):
    def __init__(self, controller):
        self.buttons = [
            Button((400,350,200,60), "Start", self._start),
            Button((400,420,200,60), "Options", self._option),
            Button((400,490,200,60), "Quit", self._quit)
        ]
        self.selected = 0
        self.ctrl = controller
    def draw(self, window):
        window.fill(white)

        window.blit(title_text, (title_text_x,100))
        for button in self.buttons:
            button.draw(window)
        self.buttons[self.selected].selected(window)

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: self.select(-1)
            elif event.key == pygame.K_DOWN: self.select(1)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z: self.buttons[self.selected].cmd()
        elif event.type == pygame.JOYHATMOTION:
            self.select(-event.value[1])
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                self.buttons[self.selected].cmd()


    def select(self, move):
        self.selected += move
        if self.selected < 0: self.selected = 2
        elif self.selected > 2: self.selected = 0

    def _start(self):
        self.ctrl.state = self.ctrl.playState
    def _option(self):
        self.ctrl.state = self.ctrl.optionState
    def _quit(self):
        self.ctrl.running = False

class PlayState(State):
    def __init__(self, controller):
        self.ctrl = controller
    def draw(self, window):
        window.fill(white)
        level.draw(window)

    def update(self, dt):
        level.update(dt)

    def handle(self, event):
        ######### key press ##########
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                player.jump = True
            elif event.key == pygame.K_LEFT:
                level.actions.append("left")
            elif event.key == pygame.K_RIGHT:
                level.actions.append("right")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                if player.jump:
                    player.jump = False
                    if player.jump_count < jump_limit:
                        player.dy += 200
            elif event.key == pygame.K_LEFT and "left" in level.actions:
                level.actions.remove("left")
            elif event.key == pygame.K_RIGHT and "right" in level.actions:
                level.actions.remove("right")

        ########## joystick button press ##########
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0: # joystick button for "A" in xbox one controller
                player.jump = True
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 0 and player.jump:
                player.jump = False
                if player.jump_count < jump_limit:
                    player.dy += 200
            if event.button in level.actions:
                level.joyButtonDown.remove(event.button)
        elif event.type == pygame.JOYHATMOTION:
            print(event.value[0])
            if event.value[0] == -1:
                level.actions.append("left")
                if "right" in level.actions: level.actions.remove("right")
            elif event.value[0] == 1:
                level.actions.append("right")
                if "left" in level.actions: level.actions.remove("left")
            if event.value[0] == 0:
                level.actions.clear()

class OptionState(State):
    pass

class StateController:
    def __init__(self):
        self.menuState = MenuState(self)
        self.playState = PlayState(self)
        self.optionState = OptionState(self)

        self.state = self.menuState
        self.running = True
        self.time_last = 0
        self.active = True
    def draw(self, window):
        self.state.draw(window)
    def handle(self, event):
        self.state.handle(event)

    def update(self):
        time = pygame.time.get_ticks()
        dt = (time - self.time_last)/1000
        self.state.update(dt)
        self.time_last = time
