from config import *
from time import sleep
import serial
import struct


if __name__ == "__main__":
	with serial.Serial(SERIAL_PORT, 9600) as ser:
		ser.write(b'\x010\x00\x00')
		sleep(0.1)
		# L + R + A
		ser.write(b'\x03L\x80\x80R\x80\x80A\x80\x80')