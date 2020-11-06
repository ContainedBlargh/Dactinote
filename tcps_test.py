from time import sleep
from data_sources import TCPSource
from sockets import Sender, gethostname
from pickle import dumps
import numpy as np

def print_ndarray(arr: np.ndarray):
    print("received messages")
    print(arr.shape)

port = 38759

tcps = TCPSource(port, listener=print_ndarray)
tcps.enable()

src = Sender(gethostname(), port)
src.start()

arr = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

arr_bytes = dumps(arr)
print(f"bytes to send: {arr_bytes}")
src.send_bytes(arr_bytes)
print("sent bytes")

sleep(5)

"""
Okay, so, Pickle uses the ASCII control characters all willy nilly, making it super hard to identify start and end of messages.
So, instead, I'll be packing multiple control bytes to start and end.
But, there's probably no guarantees when it comes to pickle.
It would be better to base64 encode the pickled data before sending it, since this guarantees that none of my precious control characters get manhandled.
"""
