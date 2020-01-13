from oscpy.client import OSCClient
import time
address = "127.0.0.1"
port = 9001


osc = OSCClient(address, port)
for i in range(10):
    osc.send_message(b'/ping', [i])
    time.sleep(1)
    print ('sleeping', i)

