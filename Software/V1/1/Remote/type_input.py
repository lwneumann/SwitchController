import serial
import struct
from time import sleep


SERIAL_PORT = '/dev/ttyUSB0'

def get_packet(commands, x=0, y=0):
    packet = struct.pack("B", len(commands))
    for c in commands:
        packet += struct.pack("cBB", c.encode(), x, y)
    print(packet)
    return packet


def run():
    i = 0
    with serial.Serial(SERIAL_PORT, 9600) as ser:
        while i != 'exit':
            i = input('')
            i = i.split(' ')

            if i[0] != 'exit':
                if len(i) in (3, 4):
                    p = get_packet(i[0], int(i[1]), int(i[2]))
                else:
                    p = get_packet(i[0])
                ser.write(p)

                if len(i) in (2, 4):
                    sleep(float(i[-1]))
                    print('Waiting', i[-1])
                else:
                    sleep(0.1)

                if len(i) in (1, 2):
                    p = get_packet(i[0].lower())
                else:
                    p = get_packet('0')
                ser.write(p) 
    return 0


if __name__ == '__main__':
    raise SystemExit(run())
