from data_sources import MJPEG
from time import sleep

ds = MJPEG("http://192.168.1.134:8080/stream/video.mjpeg", max_buffered=1)
ds.enable()

while True:
    data = ds.get_data()
    print(f"data shape: {data.shape}")
