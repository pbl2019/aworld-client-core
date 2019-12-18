import json
import time
import threading
from socket import socket, AF_INET, SOCK_DGRAM
from aworld_client_core.data import Data
from aworld_client_core import config


class Core:

    def __init__(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.data = Data()
        self.salt = int(round(time.time() * 1000))
        self.mutation_callback = None

    def send_key(self, button_name, is_pressed=True, parameter={}):
        msg = {
            "salt": self.salt,
            "character_id": str(self.data.character_id),
            "button_name": button_name,
            "status": is_pressed,
            "optional": parameter,
            }
        self.sock.sendto(json.dumps(msg).encode(),
                (config.control_host, config.control_port))

    def receive(self, secure=False):
        msg, addr = self.sock.recvfrom(config.receive_port)
        if secure and addr != config.data_host:
            print(addr)
            raise UserWarning
        msg = json.loads(msg.decode('utf-8'))
        mutations = self.data.update(**msg)
        if self.mutation_callback:
            (self.mutation_callback)(mutations)

    def close_socket(self):
        self.sock.close()

    def spawn_thread(self, daemon=True, secure=True):
        def _(secure):
            while True:
                self.receive(secure=secure)
        th = threading.Thread(target=_, daemon=daemon, args=(secure,))
        th.start()
        return th
