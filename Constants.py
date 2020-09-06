import pygame

## Colors ##
white = (255,255,255)
black = (0,0,0)
grey = (195,195,195)
pink = (255,105,180)
red = (255,0,0)

## Window Size ##
win_width = 1000
win_height = 700

## Fonts ##
pygame.font.init()
title_font = pygame.font.SysFont("Comic Sans MS", 72)
button_font = pygame.font.SysFont("Comic Sans MS", 24)
counter_font = pygame.font.SysFont("Comic Sans MS", 128)

## Text (pygame.Surface) ##
title_text = title_font.render("A Mini Game", True, black)
title_text_x = (win_width - title_text.get_width())/2

## Game ##
gravity = 400 # pixel per second
rho = 0.3
ball_radius = 25
Sball_radius = 30 # Small ball radius for enemies
jump_v = 1200
jump_limit = 0.5 # second
move_speed = 200
bounce_limit = jump_limit * 0.6
descend_speed = 600
starting_alert_time = 2
starting_spawn_rate = 5
max_health = 3
