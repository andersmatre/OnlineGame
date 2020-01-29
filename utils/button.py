
import pygame as pg


class Button:

    def __init__(self, x, y, width, height, color, map, font=None, text=None, screen_width=None):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.screen_width = screen_width

        self.image = pg.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        if font and text:
            self.text_surface = font.render(text, True, (255, 255, 255))
            self.map = map
        else:
            self.text_surface = None

    def handle_event(self, e):
        if e.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(e.pos):
                self.map()

    def draw(self, screen):
        screen.blit(self.image, (self.screen_width / 2 - self.width / 2, self.y))
        if self.text_surface:
            screen.blit(self.text_surface, (self.screen_width / 2 - self.text_surface.get_width() / 2,
                                            self.y + self.height / 2 - self.text_surface.get_height() / 2))
