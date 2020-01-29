
import pygame as pg
import queue
from client import menu


class GameClient:

    def __init__(self):
        pg.init()
        pg.display.set_caption('')
        self.font = pg.font.SysFont('comicsansms', 20)

        self.screen = pg.display.set_mode((500, 500))
        self.width, self.height = pg.display.get_surface().get_size()

        self.keybinds = self.get_keybinds()
        self.menu = menu.Menu(self)
        self.clock = pg.time.Clock()
        self.fps = 0
        self.dt = self.clock.tick(self.fps)

        self.queue = queue.Queue()
        self.get_queue = None

        self.events = None
        self.done = False

        self.server = None
        self.network = None
        self.player = None

    def get_keybinds(self):
        kb = {}
        try:
            with open('./keybindings.txt', 'r') as k:
                lines = k.read().splitlines()
                for line in lines:
                    if line == '*':
                        break
                    else:
                        split = line.split(' = ')
                        kb.update({split[0]: 'K_' + split[1]})
        except IOError:
            print('File ' + k + ' does not exist.')
            return None
        return kb

    def process_events(self):
        self.events = pg.event.get()
        for e in self.events:
            # Exit application if 'X' is clicked.
            if e.type == pg.QUIT:
                self.done = True

            if e.type == pg.KEYDOWN:
                # Exit to menu.
                if e.key == getattr(pg, self.keybinds['return']):
                    self.network, self.player = None, None
                    self.menu.window, self.menu.draw = self.menu.connect, True

                # Stop server.
                if e.key == getattr(pg, self.keybinds['stop_server']):
                    if self.server:
                        self.server.done = True

    def main(self):
        while not self.done:
            # Set a caption.
            if self.player:
                pg.display.set_caption(self.player.name + '  FPS: ' + str(int(round(self.clock.get_fps()))))
            else:
                pg.display.set_caption('FPS: ' + str(int(round(self.clock.get_fps()))))

            # Handle keyboard and mouse events.
            self.process_events()

            # Draw menu if the menu object is set to draw = True.
            if self.menu.draw:
                self.dt = self.clock.tick(60)
                self.menu.draw_window()
                pg.display.update()

            # Else draw the game.
            else:
                self.dt = self.clock.tick(self.fps)
                self.screen.fill((255, 255, 255))

                # Draw and update the player on the client.
                self.player.draw(self.screen, self.font)
                if self.player.alive:
                    self.player.update(self)

                # Exchange information with the server.
                try:
                    data = {
                        'pos': (self.player.x, self.player.y),
                        'projectiles': self.player.projectiles,
                        'hit': self.player.hit}
                    self.network.exchange(data, self.queue)
                    self.get_queue = self.queue.get()
                    self.player = self.get_queue[1]
                    for q in self.get_queue[0]:
                        q.draw(self.screen, self.font)
                except ConnectionResetError:
                    # Exit to the menu if the server connection is lost.
                    self.network, self.player = None, None
                    self.menu.window, self.menu.draw = self.menu.connect, True
                    print('Lost connection to the server.')

                pg.display.update()

        # Stop the code when the loop is terminated.
        if self.server:
            self.server.done = True
            self.server.socket.close()
        pg.quit()
        exit()
