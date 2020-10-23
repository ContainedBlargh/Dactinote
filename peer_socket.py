from socket import socket, gethostname
from threading import Thread
from typing import Callable
from time import sleep
from random import random

class PeerSocket:

    STX = b'0x02'
    ETX = b'0x03'

    def send(self, message: str):
        if not self.keep_alive:
            raise Exception("Cannot send: socket disconnected!")
            
        pass

    def __listen(self):
        while self.keep_alive:
            self.scin.listen(5)
            conn, addr = self.scin.accept()
            self.scin_open = True
            buffer = b''
            while self.scin_open:
                with conn as target:
                    buffer += conn.recv(1024)
                    start = buffer.find(PeerSocket.STX)
                    end = buffer.find(PeerSocket.ETX)
                    if start != -1 and end != -1:
                        msg = buffer[start + 1:end]
                        buffer = buffer[end+1:]
                        msg = msg.decode('utf-8')
                        self.listener(msg)
                    pass

    def __connect(self):
        while not self.connected:
            try:
                self.scout.connect((self.ex_addr, self.ex_port_in))
                self.scin.connect((self.ex_addr, self.ex_port_out))
                self.connected = True
            except Exception as e:
                print("Connection attempt failed")
                print(e)
                sleep(random() * 3)
                
                
        self.scin_thread = Thread(target=self.__listen)
        self.scin_thread.daemon = True
        self.scin_thread.start()


    def connect(self, external_address: str, external_port_in: int, external_port_out: int):
        if self.listener is None:
            print(f"warning: no listener registered for PeerSockets [{self.host}:{self.port_in}:{self.port_out}] <-> [{external_address}:{external_port_in}:{external_port_out}]")
        
        self.connected = False
        self.ex_addr = external_address
        self.ex_port_in = external_port_in
        self.ex_port_out = external_port_out

        self.connector = Thread(target=self.__connect)
        self.connector.start()
        pass

    def disconnect(self):
        self.scin_open = False
        self.keep_alive = False
        if self.scin_thread is not None:
            self.scin_thread.join()
            self.scin_thread = None

    def set_message_listener(self, listener: Callable[[str], None]):
        self.listener = listener


    def __init__(self, port_in: int, port_out: int):
        self.host = gethostname()
        self.port_in = port_in
        self.port_out = port_out
        self.listener = None
        self.scin = socket()
        self.scin.bind((self.host, port_in))
        self.scin_open = False
        self.keep_alive = False
        self.connected = False
        self.scin_thread = None
        self.scout = socket()
        self.scout.bind((self.host, port_out))
        pass