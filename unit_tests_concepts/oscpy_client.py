from oscpy.client import OSCClient
import time
address = "127.0.0.1"
port = 9001
import random

osc = OSCClient(address, port)
for i in range(10):
    osc.send_message(b'/ping', [i,i,i+1])
    osc.send_message(b'/rot',[10*random.random(),10*random.random(),10*random.random()])
    time.sleep(1)
    print ('slee', [i,i,i+1])
