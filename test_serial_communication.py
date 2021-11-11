import serial
import time

arduino = serial.Serial(port="/dev/ttyACM0",baudrate=115200,timeout=1) # open serial port "linux"
msg = 'Hello world'
counter = 0.08758831
while True:
    arduino.write(bytes(str(counter),'utf-8'))
    time.sleep(0.5)
