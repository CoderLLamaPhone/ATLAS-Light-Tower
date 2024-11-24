#! /usr/bin/python -u
#from lib.StupidArtnet import StupidArtnet
from stupidArtnet import StupidArtnet
import time
import random
import os

# THESE ARE MOST LIKELY THE VALUES YOU WILL BE NEEDING
target_ip = os.getenv('ARTNET_TARGET_IP', '127.0.0.1')
universe = 0  # see docs
packet_size = 10            # it is not necessary to send whole universe

LT_RED = 0
LT_GREEN = 1
LT_BLUE = 2

# CREATING A STUPID ARTNET OBJECT
# SETUP NEEDS A FEW ELEMENTS
# TARGET_IP   = DEFAULT 127.0.0.1
# UNIVERSE    = DEFAULT 0
# PACKET_SIZE = DEFAULT 512
# FRAME_RATE  = DEFAULT 30
a = StupidArtnet(target_ip, universe, packet_size)

# MORE ADVANCED CAN BE SET WITH SETTERS IF NEEDED
# NET         = DEFAULT 0
# SUBNET      = DEFAULT 0

# CHECK INIT
print(a)

# YOU CAN CREATE YOUR OWN BYTE ARRAY OF PACKET_SIZE
packet = bytearray(packet_size)      # create packet for Artnet
a.set(packet)                        # only on changes

# TO SEND PERSISTANT SIGNAL YOU CAN START THE THREAD
a.start()                            # start continuos sendin

# AND MODIFY THE DATA AS YOU GO

while True:
    red, green, blue = 0, 0, 0
    max_color = random.choice(['red', 'green', 'blue'])
    if max_color == 'red':
        red = 255
        green = random.randint(0, 185)
        blue = random.randint(0, 185)
    elif max_color == 'green':
        green = 255
        red = random.randint(0, 185)
        blue = random.randint(0, 185)
    else:
        blue = 255
        red = random.randint(0, 185)
        green = random.randint(0, 185)

    for i in range(0, 100, 10):
        packet[LT_RED] = i * red // 100
        packet[LT_GREEN] = i * green // 100
        packet[LT_BLUE] = i * blue // 100
        print(f"Red: {packet[LT_RED]}, Green: {packet[LT_GREEN]}, Blue: {packet[LT_BLUE]}")
        a.set(packet)
        time.sleep(0.05)
    for i in range(100, 0, -10):
        packet[LT_RED] = i * red // 100
        packet[LT_GREEN] = i * green // 100
        packet[LT_BLUE] = i * blue // 100
        print(f"Red: {packet[LT_RED]}, Green: {packet[LT_GREEN]}, Blue: {packet[LT_BLUE]}")
        a.set(packet)
        time.sleep(0.05)
time.sleep(1)



#a.blackout()

# ... REMEMBER TO CLOSE THE THREAD ONCE YOU ARE DONE
a.stop()

# CLEANUP IN THE END
del a
