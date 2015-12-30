#!/usr/bin/python
import pyfirmata
from Tkinter import *
import time

board = pyfirmata.Arduino('/dev/ttyUSB0')

# start an iterator thread so
# serial buffer doesn't overflow
iter8 = pyfirmata.util.Iterator(board)
iter8.start()

pin0 = board.get_pin('a:0:i')

while pin0.read() is None:
    pass

def get_temp():
    label_text = "Temp: %6.1f F" % (
    pin0.read() * 5 * 100 * 9 / 5 +32)
    return label_text

def cleanup():
    # clean up on exit
    board.exit()

while True:
    print get_temp()
    time.sleep(10)
