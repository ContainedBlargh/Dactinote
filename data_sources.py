from sockets import Receiver
from typing import Callable, Deque
from cv2 import imdecode
from urllib.request import urlopen
import cv2
from threading import Thread
import numpy as np
from time import sleep
from pickle import UnpicklingError, loads
from abc import ABC, abstractmethod

"""
This module is responsible for creating live-datasources.

The interface for a data source is as follows:
- set_listener(listener: Callable[[np.ndarray], None])
- enable()
- disable()
- is_enabled() -> bool

The listener attached to a datasource is then fed the data as it appears.
"""
class DataSource(ABC):
    @abstractmethod
    def set_listener(listener: Callable[[np.ndarray], None]):
        pass
    
    @abstractmethod
    def enable():
        pass

    @abstractmethod
    def disable():
        pass

    @abstractmethod
    def is_enabled() -> bool:
        pass


class MJPEG(ABC):
    """
    Encapsulates an MJPEG stream.
    The stream is constantly polled by a background process.
    """

    def read_stream(self):
        stream = cv2.VideoCapture(self.stream_url)
        while self.running:
            _, frame = stream.read()
            self.frames.appendleft(frame)
            if len(self.frames) == self.buff_len:
                data = []
                for _ in range(self.buff_len):
                    data.append(self.frames.pop())
                if self.listener is not None:
                    self.listener(np.array(data))
        stream.release()

    def enable(self):
        self.running = True
        self.thread = Thread(target=self.read_stream)
        self.thread.daemon = True
        self.thread.start()

    def disable(self):
        self.running = False
        self.thread.join()

    def is_enabled(self) -> bool:
        return self.running

    def set_listener(self, listener: Callable[[np.ndarray], None]):
        self.listener = listener

    def __init__(self, stream_url, max_buffered=4, listener: Callable[[np.ndarray], None] = None):
        self.listener = listener
        self.stream_url = stream_url
        self.bytes = ''
        self.buff_len = max_buffered
        self.running = False
        self.frames = Deque(maxlen=4)
        self.thread = None


class TCPSource(ABC):
    """
    A data source that receives pickled numpy arrays over a TCP port.
    """

    def convert_listener(self, listener: Callable[[np.ndarray], None]) -> Callable[[bytes], None]:
        
        def parse_bytes(bytes):
            self.raw_buffer += bytes
            try:
                arr:np.ndarray = loads(data=self.raw_buffer)
                self.raw_buffer = b''
                listener(arr)
            except UnpicklingError:
                print("unsuccessful unpickle attempt")
                pass
        return parse_bytes
        
    def enable(self):
        self.running = True
        self.receiver = Receiver(self.port, self.convert_listener(self.listener))
        self.receiver.start()

    def disable(self):
        self.running = False
        self.receiver.stop()
        self.receiver = None

    def is_enabled(self) -> bool:
        return self.running


    def set_listener(self, listener: Callable[[np.ndarray], None]):
        self.listener = listener
        pass

    def __init__(self, port: int, max_buffered=1, listener: Callable[[np.ndarray], None] = None):
        self.raw_buffer = b''
        self.port = port
        self.max_buffered = max_buffered
        self.listener = listener
        self.running = False
        self.receiver = None
