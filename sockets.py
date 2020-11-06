from socket import socket, gethostname, AF_INET, SOCK_STREAM, timeout
from select import select
from threading import Thread
from typing import Callable, Deque

STX = b'\x0A\x0D\x0A\x0D\x02\x02\x02\x0A\x0D\x0A\x0D'
STXL = len(STX)
ETX = b'\x0A\x0D\x0A\x0D\x03\x03\x03\x0A\x0D\x0A\x0D'
ETXL = len(ETX)

class Receiver(Thread):

    def __init__(self, port: int, listener: Callable[[bytes], None]=None):
        Thread.__init__(self, name=f"Receiver[{port}]")
        self.daemon = True
        self.host = gethostname()
        self.port = port
        self.running = False
        self.listener = listener

    def set_listener(self, listener: Callable[[bytes], None]):
        self.listener = listener

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(2)
        sock.bind((self.host, self.port))
        sock.listen(2)
        while self.running:
            try:
                conn, _ = sock.accept()
            except timeout:
                continue
            try:
                buffer = b''
                while self.running:
                    buffer += conn.recv(4096)
                    start = buffer.find(STX)
                    end = buffer.find(ETX)
                    if start != -1 and end != -1:
                        msg = buffer[start + STXL:end]
                        buffer = buffer[end + ETXL:]
                        print(msg)
                        self.listener(msg)
                        break
            finally:
                conn.shutdown(2)
                conn.close()
                pass


class Sender(Thread):

    def __init__(self, destination_addr: str, destination_port: int):
        Thread.__init__(self, name=f"Sender[{destination_port}]")
        self.daemon = True
        self.host = destination_addr
        self.port = destination_port
        self.running = False
        self.messages = Deque()

    def stop(self):
        self.running = False

    def send_bytes(self, message: bytes):
        self.messages.appendleft(message)

    def send_string(self, message: str, encoding="utf-8"):
        self.send_bytes(message.encode(encoding))

    def run(self):
        self.running = True
        while self.running:
            if len(self.messages) > 0:
                message = self.messages.pop()
                try:
                    sock = socket(AF_INET, SOCK_STREAM)
                    sock.connect((self.host, self.port))
                    sock.sendall(STX + message + ETX)
                    sock.shutdown(2)
                    sock.close()
                except:
                    self.messages.append(message)

