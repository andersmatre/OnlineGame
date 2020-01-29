
import socket
import threading
import pickle


class Server:

    def __init__(self, ip, port, limit):
        self.ip = ip
        self.port = port
        self.limit = limit
        self.socket = None
        self.online = []

        self.done = False
        self.player_class = None
        self.colors = [(0, 100, 200), (200, 0, 0), (0, 200, 0)]
        self.game_started = False

    def start_server(self):

        # Bind the port to the IP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((self.ip, self.port))
        except socket.error:
            return

        # Listen for connections
        self.socket.listen(self.limit)
        print('Server started, waiting for a connection ...')

        while not self.done:
            try:
                conn, addr = self.socket.accept()
            except socket.error:
                break
            print('Connected to: ', addr)
            threading.Thread(target=self.client_connection, args=(conn,)).start()

    def disconnect_connection(self, conn, name):
        for i, p in enumerate(self.online):
            if p.name == name:
                del self.online[i]
                print('Player ' + str(name) + ' disconnected.')
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()

    def client_connection(self, conn):
        # Try to create a player instance
        p_dict = pickle.loads(conn.recv(1024))
        name = p_dict['name']
        player = self.player_class(p_dict['pos'][0], p_dict['pos'][1], p_dict['size'], name, color=self.colors[len(self.online)])

        # Check if username is taken
        for p in self.online:
            if p.name == name:
                conn.send(pickle.dumps(str.encode('Username ' + name + ' already in use on ip: ' + str(self.ip))))
                self.disconnect_connection(conn, name)
                return

        # Set the player as online
        self.online.append(player)
        print('Player ' + str(name) + ' connected.')

        # Send player instance back to the connection
        for i, p in enumerate(self.online):
            if p.name == name:
                conn.send(pickle.dumps(player))

        while True:
            try:
                if self.done:
                    break

                data = pickle.loads(conn.recv(2048))

                # Start the game
                if data == 'start':
                    self.game_started = True
                    continue

                # Get all player that are online
                if data == 'lobby':
                    conn.sendall(pickle.dumps([self.online, self.game_started]))
                    continue

                if type(data) is dict:
                    for i, p in enumerate(self.online):
                        # Update health of hit players
                        for hit in data['hit']:
                            if hit.name == p.name:
                                self.online[i].health -= data['hit'][hit]

                        if p.health <= 0:
                            p.alive = False

                        # Update self and get others except self back
                        if p.name == name:
                            p_index = self.online[i]
                            p_index.x = data['pos'][0]
                            p_index.y = data['pos'][1]
                            p_index.projectiles = data['projectiles']

                            _online = self.online[:i]+self.online[i+1:]
                            conn.sendall(pickle.dumps([_online, p_index]))

            except (EOFError, ConnectionResetError, socket.error) as e:
                print(e)
                break

        self.disconnect_connection(conn, name)
        return
