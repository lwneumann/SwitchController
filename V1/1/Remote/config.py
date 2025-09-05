import serial


SERIAL_PORT = '/dev/ttyUSB1'


def reset():
	with serial.Serial(SERIAL_PORT, 9600) as ser:
		ser.write(b'\x010\x00\x00')


if __name__ == "__main__":
	reset()