from typing import Deque
from cv2 import imdecode
from urllib.request import urlopen
import cv2
from threading import Thread
import numpy as np
from time import sleep

"""
This module is responsible for creating live-datasources.

The interface for a data source is as follows:
- get_data() -> np.ndarray
- enable()
- disable()
- is_enabled() -> bool

"""

class MJPEG:
    """
    Encapsulates an MJPEG stream.
    The stream is constantly polled by a background process.
    """

    def read_stream(self):
        stream = cv2.VideoCapture(self.stream_url)
        print("opened stream")
        while self.running:
            _, frame = stream.read()
            print("found frame!")
            self.frames.append(frame)
        stream.release()

    def get_data(self) -> np.ndarray:
        data = []
        while len(self.frames) < self.buff_len:
            # Wait
            pass
        for i in range(self.buff_len):
            data.append(self.frames.pop())
        
        return np.array(data)

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

    def __init__(self, stream_url, max_buffered=4):
        self.stream_url = stream_url
        self.bytes = ''
        self.buff_len = max_buffered
        self.running = False
        self.frames = Deque(maxlen=4)
        self.thread = None

