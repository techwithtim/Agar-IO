import socket
import pickle


class Network:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "10.50.120.202"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.name = name

    def connect(self):
        """
        connects to server and returns the id of the client that connected
        """
        self.client.connect(self.addr)
        self.client.send(str.encode(self.name))
        val = self.client.recv(8)
        return int(val.decode()) # can be int because will be an int id

    def disconnect(self):
        self.client.close()

    def send(self, data, pick=False):
        """
        :param data: str
        :return: str
        """
        try:
            if pick:
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))
            reply = self.client.recv(2048)
            try:
                reply = pickle.loads(reply)
            except Exception as e:
                print(e)
                self.connect()

            return reply
        except socket.error as e:
            print(e)
            self.connect()



