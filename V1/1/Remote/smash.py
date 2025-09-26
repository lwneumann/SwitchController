"""
Horizontal Movement
32-64: slow walk
65-91: walk
92- : slow run

Turning around need to be at least pm 32 (96, 160)


"""
from config import *
from time import sleep
import struct
import serial


def get_packet(inputs):
	# Get packet for series of inputs be excecuted at once
	if inputs[0] in ("<", ">"):
		inputs = [inputs]

	packet = struct.pack("B", len(inputs))
	for i in inputs:
		if i[0] not in ("<", ">"):
			s = i
			x = 0
			y = 0
		else:
			s = i[0]
			x = i[1]
			y = i[2]
		packet += struct.pack("cBB", s.encode(), x, y)
	return packet


LEFT = ("<", 0, 128)
DOWN = ("<", 128, 255)
RIGHT = ("<", 255, 128)
NEUTRAL = ("<", 128, 128)
LOOK_LEFT = ("<", 96, 128)
LOOK_RIGHT = ("<", 160, 128)

neutral_p = get_packet([NEUTRAL])
reset_p = get_packet(['0'])


def horz(v):
	"""
	-1 <-> 1
	Moves horizontally from max left to max right parameteraized by v
	"""
	return ("<", int(128 + (128 * v)), 128)


class Remote:
	def __init__(self):
		self.ser = serial.Serial(SERIAL_PORT, 9600)
		return

	def quit(self):
		self.ser.close()
		return


	def press(self, inp, wait=0.1, after_inp=reset_p, pause=0.5):
		self.ser.write(get_packet(inp))
		sleep(wait)
		if after_inp == reset_p:
			self.ser.write(after_inp)
		else:
			self.ser.write(get_packet(after_inp))
		sleep(pause)
		return


	def test_movement(self):
		i = 128
		while i < 256:
			self.ser.write(get_packet(("<", i, 128)))
			x = input(f"{i} ({i-128}) - ")
			if x != '':
				i = 128 + int(x)
			else:
				i += 1
		return


	def turnip_loop(self):
		# Peach to DK in training mode
	
		# Reset Training Mode
		self.press(["L", "R", "A"])

		# Turnip
		self.press([DOWN, "B"])

		# Walkup turnaround
		self.press(horz(0.5), pause=0.4)
		self.press(LOOK_LEFT)

		sleep(1)
		reset()
		self.quit()
		return


if __name__ == "__main__":
	Remote().test_movement()