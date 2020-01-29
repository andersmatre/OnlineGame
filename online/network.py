
import socket
import pickle


class Network:

    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)

    def connect(self, p_dict):
        self.client.connect(self.addr)
        self.client.send(pickle.dumps(p_dict))
        return pickle.loads(self.client.recv(1024))

    def exchange(self, data, queue):
        self.client.send(pickle.dumps(data))
        try:
            queue.put(pickle.loads(self.client.recv(2048)))
        except socket.error:
            raise ConnectionResetError

    def send(self, data):
        self.client.send(pickle.dumps(data))
