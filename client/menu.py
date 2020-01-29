
import pygame as pg
from utils import button, inputbox
from online import server
from online.network import Network
from game import player
import threading
import random


class Menu:

    def __init__(self, client):
        self.client = client
        self.font = pg.font.SysFont('comicsansms', 20)
        self.draw = True
        self.window = self.connect

        self.join_b = button.Button(self.client.width / 2 - 200 / 2, 300, 200, 50, (0, 100, 200),
                                    self.join, font=self.client.font, text='Join Server', screen_width=self.client.width)
        self.start_b = button.Button(self.client.width / 2 - 200 / 2, 360, 200, 50, (0, 100, 200),
                                     self.start, font=self.client.font, text='Start Server', screen_width=self.client.width)
        self.name_ib = inputbox.InputBox(100, 100, 150, 30, font=self.client.font, screen_width=self.client.width,
                                         text='Guest' + str(random.randint(1, 1000)))
        self.ip_ib = inputbox.InputBox(100, 200, 150, 30, font=self.client.font, screen_width=self.client.width,
                                       text='10.0.0.71:5555')

        self.ib = [self.name_ib, self.ip_ib]
        self.text = ['YOUR NAME', 'IPV4:PORT']
        self.buttons = [self.start_b, self.join_b]

    def login(self, ip, port, p_dict):
        network = Network(ip, port)
        player = network.connect(p_dict)
        return network, player

    def join(self):
        try:
            p_dict = {
                'name': self.name_ib.get_text(),
                'pos': (100, 100),
                'size': 20}
            creds = self.ip_ib.get_text().split(':')
            self.client.network, recieved = self.login(ip=creds[0], port=int(creds[1]),
                                                       p_dict=p_dict)
            if type(recieved) is bytes:
                print(recieved.decode('utf-8'))
            else:
                self.client.player = recieved
                self.window = self.lobby
        except IndexError:
            print('Input field should be IP:PORT.')
        except ConnectionRefusedError:
            print('No valid connection. Check if server is running.')

    def start(self):
        self.client.player = player.Player(100, 100, 20, name=self.name_ib.get_text(),
                                           color=(0, 100, 200))
        creds = self.ip_ib.get_text().split(':')
        self.client.server = server.Server(ip=creds[0], port=int(creds[1]), limit=4)
        self.client.server.player_class = self.client.player.__class__
        threading.Thread(target=self.client.server.start_server).start()
        self.join()

    def connect(self):
        for e in self.client.events:
            for ib in self.ib:
                ib.handle_event(e)
            for b in self.buttons:
                b.handle_event(e)

        for ib in self.ib:
            ib.draw(self.client.screen)
        for b in self.buttons:
            b.draw(self.client.screen)

        y = 70
        for text in self.text:
            label = self.font.render(text, True, (50, 50, 50))
            self.client.screen.blit(label, (self.client.width / 2 - label.get_width() / 2, y))
            y += 100

    def lobby(self):
        for event in self.client.events:
            if event.type == pg.KEYDOWN:
                # Start
                if event.key == getattr(pg, self.client.keybinds['start']):
                    self.client.network.send('start')

        lobby_label = self.font.render('Lobby', True, (0, 0, 0))
        self.client.screen.blit(lobby_label, (self.client.width / 2 - lobby_label.get_width() / 2, 50))

        if self.client.network:
            try:
                self.client.network.exchange('lobby', self.client.queue)
                y = 100
                queue = self.client.queue.get()
                for q in queue[0]:
                    label = self.font.render(q.name, True, q.color)
                    self.client.screen.blit(label, (100, y))
                    y += 30
                if queue[1]:
                    self.draw = False
                    print('Game starting ...')

            except ConnectionResetError:
                self.network, self.player = None, None
                self.window, self.draw = self.connect, True

    def draw_window(self):
        self.client.screen.fill((255, 255, 255))
        self.window()
        for e in self.client.events:
            if e.type == pg.KEYDOWN:
                if e.key == getattr(pg, self.client.keybinds['return']):
                    self.window = self.connect
