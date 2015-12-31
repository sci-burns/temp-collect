#!/usr/bin/python
import pyfirmata
import time
from datetime import datetime

fileName = "test.csv"
board = pyfirmata.Arduino('/dev/ttyUSB0')

# start an iterator thread so
# serial buffer doesn't overflow
iter8 = pyfirmata.util.Iterator(board)
iter8.start()

pin0 = board.get_pin('a:0:i')

while pin0.read() is None:
    pass

def get_temp():
    return (pin0.read() * 5 * 100 * 9 / 5 +32)

def cleanup():
    # clean up on exit
    board.exit()

while True:
    myFile = open(fileName, 'a')
    currTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp = get_temp()
    myFile.write(currTime + "," + str(temp) + "\n")
    myFile.close()
    time.sleep(10)

