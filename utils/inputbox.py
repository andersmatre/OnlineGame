
import pygame as pg


class InputBox:

    def __init__(self, x, y, width, height, font, screen_width=None, text=None):
        self.width = width
        self.rect = pg.Rect(x, y, width, height)
        self.screen_width = screen_width

        self.color = (0, 0, 0)
        self.text = text
        self.font = font
        self.active = False

        if self.text:
            self.text_surface = self.font.render(text, True, self.color)
            self.rect.width = self.text_surface.get_rect().width

    def handle_event(self, e):
        if e.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(e.pos):
                self.active = not self.active
            else:
                self.active = False
        if e.type == pg.KEYDOWN:
            if self.active:
                if e.key == pg.K_RETURN:
                    pass
                elif e.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 25:
                        self.text += e.unicode
                self.text_surface = self.font.render(self.text, True, self.color)

    def get_text(self):
        return self.text

    def update(self):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.color = (0, 100, 200) if self.active else (0, 0, 0)
        self.rect.width = max(self.width, self.text_surface.get_width() + 10)

        if self.screen_width:
            self.rect.x = self.screen_width / 2 - self.rect.width / 2

    def draw(self, screen):
        self.update()
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y))
        pg.draw.rect(screen, (0, 0, 0), self.rect, 2)
