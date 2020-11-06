from time import sleep
from sockets import gethostname, Receiver, Sender

receiver = Receiver(36258, listener=lambda m: print(f"s1 received: '{m.decode('utf-8')}'"))
receiver.start()
sender = Sender(gethostname(), 36258)
sender.start()

for i in range(10):
    sender.send_string(f"i={i}")
    
sleep(2)
receiver.stop()
sender.stop()
exit()