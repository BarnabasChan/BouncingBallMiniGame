import pygame
import random
import math

from Constants import *

heart = pygame.image.load("assets\\heart_red.png")
grey_heart = pygame.image.load("assets\\heart_grey.png")

class Player:
    gravity = 400
    bounce_count = 0
    health = max_health
    dx, dy = 0, 0
    def __init__(self):
        self.inAir = True
        self.jump_count = 0
        self.jump = False
        self.bounce = False
    def draw(self, window):
        if self.bounce:
            color = pink
        else:
            color = red
        pygame.draw.circle(window, color, (int(self.x), int(self.y)), ball_radius)
    def update(self, dt):
        # jump
        if self.jump and not self.inAir:
            self.dy = -400
            self.inAir = True
        else:
            self.dy += gravity * dt
        self.y += self.dy * dt
        # collision
        if ground.collide():
            if self.dy >= gravity * rho:
                self.bounce = True
                print("bounce")
                self.dy *= -rho
            else:
                self.dy = 0
                self.inAir = False
                self.jump_count = 0
                self.bounce_count = 0
                self.bounce = False
            self.y = ground.y - ball_radius -1
        # get hit
        for enemy in self.level.enemies:
            if enemy.collide():
                self.lose_health()
                if self.health > 0:
                    enemy.destroy()
        # move
        if "left" in level.actions and "right" not in level.actions:
            self.dx = -move_speed
        elif "right" in level.actions and "left" not in level.actions:
            self.dx = move_speed
        elif "left" not in level.actions and "right" not in level.actions:
            if not self.inAir:
                self.dx = 0
            elif self.dx > 0:
                self.dx -= move_speed * 0.2 * dt
                if self.dx < 0: self.dx = 0
            elif self.dx < 0:
                self.dx += move_speed * 0.2 * dt
                if self.dx > 0: self.dx = 0
        self.x += self.dx * dt
        # handle falling out of platform
        if self.y > win_height * 1.5:
            self.x, self.y = 500, 400
            self.dx, self.dy = 0, 0
            self.lose_health()
    def lose_health(self):
        self.health -= 1

player = Player()

class Obstacle:
    def __init__(self, rect):
        self.x, self.y, self.w, self.h = self.rect = rect
    def draw(self, window):
        pygame.draw.rect(window, grey, self.rect)
    def collide(self):
        if (self.x <= player.x <= self.x + self.w and player.y + ball_radius >= self.y):
            return True

ground = Obstacle((50, 600, 900, 50))

########## Enemies ##########
class Enemy:
    y = -100
    dy = 0
    state = 1 # 1:descend  2:alert  3:move  4:destroy
    alert = 0
    inAir = True
    radius = ball_radius
    color = black
    def __init__(self, level):
        self.level = level
    def update(self, dt):
        if self.state == 1:
            self.y += descend_speed * dt
            if self.y >= self.alert_height:
                self.y = self.alert_height
                self.state = 2
        elif self.state == 2:
            if self.alert < self.level.alert_time:
                self.alert += dt
            else:
                self.state = 3
        elif self.state == 4:
            self.radius -= dt * 10
            if self.radius < 1:
                self.level.enemies.remove(self)
    def destroy(self):
        self.state = 4
        self.color = grey

class Bomb(Enemy):
    alert_height = 500
    g_matter = 400
    leg_len = 10
    look = 0 # switch of two diffent look
    radius = Sball_radius
    def __init__(self, level):
        self.facing = random.choice(("left", "right"))
        if self.facing == "left":
            self.x = 900
            self.dx = -150
        elif self.facing == "right":
            self.x = 100
            self.dx = 150
        self.level = level
    def update(self, dt):
        if self.state == 3:
            if not self.inAir:
                self.x += self.dx * dt
                if self.x + self.radius < ground.x or \
                    self.x - self.radius > ground.x + ground.w:
                    self.inAir = True
                    self.dy = 150
            else:
                self.dy += self.g_matter * dt
                self.y += self.dy * dt
                if self.y - self.radius > win_height:
                    self.level.enemies.remove(self)
                elif self.ground_collide():
                    self.y = ground.y - self.radius - self.leg_len - 1
                    self.dy = 0
                    self.inAir = False

        super().update(dt)

    def draw(self, window):
        if self.state < 3:
            pygame.draw.line(window, black, (self.x, self.y), (self.x, 0))
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), int(self.radius))
        if self.state != 4:
            # this part can be replace by simply bliting images, but I want to draw it with codes
            if self.look == 0:
                l1 = ((self.x - 15, self.y + 15),
                    (self.x - 25, self.y + self.radius + self.leg_len))
                l2 = ((self.x + 15, self.y + 15),
                    (self.x + 25, self.y + self.radius + self.leg_len))
            elif self.look == 1:
                l1 = ((self.x - 15, self.y + 15),
                    (self.x - 25, self.y + self.radius + self.leg_len))
                l2 = ((self.x + 15, self.y + 15),
                    (self.x + 15, self.y + self.radius + self.leg_len))
            elif self.look == 2:
                l1 = ((self.x - 15, self.y + 15),
                    (self.x - 15, self.y + self.radius + self.leg_len))
                l2 = ((self.x + 15, self.y + 15),
                    (self.x + 25, self.y + self.radius + self.leg_len))
            else:
                l1 = ((self.x - 15, self.y + 15),
                    (self.x - 15, self.y + self.radius + self.leg_len))
                l2 = ((self.x + 15, self.y + 15),
                    (self.x + 25, self.y + self.radius + self.leg_len))
            pygame.draw.line(window, black, *l1, 2)
            pygame.draw.line(window, black, *l2, 2)
    def ground_collide(self):
        if (ground.x <= self.x <= ground.x + ground.w and \
            self.y + self.radius + self.leg_len >= ground.y):
            return True
    def collide(self):
        if self.state != 4:
            dx, dy = abs(self.x - player.x), abs(self.y - player.y)
            distance = math.sqrt(dx**2 + dy**2) # distance between bomb and player
            if distance <= Sball_radius + ball_radius:
                print(distance)
                return True
            else:
                return False

enemy_types = [Bomb]



class Level:
    bgcolor = white
    actions = []
    def __init__(self):
        self.enemies = [Bomb(self)]
        player.x = 500
        player.y = 400
        player.level = self
        self.alert_time = starting_alert_time
        self.spawn_rate = starting_spawn_rate
        self.spawn_count = 0
        self.score = 0
    def draw(self, window):
        ground.draw(window)
        for enemy in self.enemies:
            enemy.draw(window)
        player.draw(window)
        for i in range(max_health):
            if player.health >= i + 1:
                window.blit(heart, (i*70, 0))
            else:
                window.blit(grey_heart, (i*70, 0))
    def update(self, dt):
        if player.health > 0:
            # TODO: handle joysticks axes

            for enemy in self.enemies:
                enemy.update(dt)
            self.spawn_count += dt
            if self.spawn_count >= self.spawn_rate:
                self.enemies.append(random.choice(enemy_types)(self))
                self.spawn_count = 0
            player.update(dt)

level = Level()
