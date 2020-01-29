
import pygame as pg
from pygame import gfxdraw
from game import projectile


class Player:

    def __init__(self, x, y, size, name, color=(0, 100, 200), health=10):

        self.x, self.y = x, y
        self.size = size

        self.color = color
        self.name = name
        self.vel = 0.2
        self.health = health
        self.alive = True

        self.projectiles = []
        self.hit = {}

    def shoot(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                self.projectiles.append(projectile.Projectile(self.x, self.y, pg.mouse.get_pos()))

    def move(self, dt, keybinds):
        keys = pg.key.get_pressed()
        if keys[getattr(pg, keybinds['move_left'])]:
            self.x -= self.vel * dt
        if keys[getattr(pg, keybinds['move_right'])]:
            self.x += self.vel * dt
        if keys[getattr(pg, keybinds['move_up'])]:
            self.y -= self.vel * dt
        if keys[getattr(pg, keybinds['move_down'])]:
            self.y += self.vel * dt

    def update(self, client):
        self.move(client.dt, client.keybinds)

        self.hit = {}
        self.shoot(client.events)
        for p in self.projectiles:
            p.update(client, self.projectiles)

    def draw(self, screen, font):
        # Name.
        if self.alive:
            label = font.render(str(self.name), True, (0, 0, 255))
        else:
            label = font.render(str(self.name) + ' (dead)', True, (255, 0, 0))
        screen.blit(label, (self.x - label.get_width() / 2, self.y - 50))

        # Character.
        gfxdraw.aacircle(screen, round(int(self.x)), round(int(self.y)), 20, self.color)
        gfxdraw.filled_circle(screen, round(int(self.x)), round(int(self.y)), 20, self.color)

        for p in self.projectiles:
            p.draw(screen)
