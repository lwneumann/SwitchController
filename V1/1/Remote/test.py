from config import *
import serial
import struct
from time import sleep


class Input:
    def __init__(self, data):
        # Default values
        self.symbol = '0'
        self.x = 128
        self.y = 128
        self.duration = 0.1
        
        if len(data) == 1:
            self.symbol = data[0]
        elif len(data) == 2:
            self.symbol = data[0]
            self.duration = data[1]
        elif len(data) == 3:
            self.symbol = data[0]
            self.x = data[1]
            self.y = data[2]
        elif len(data) == 4:
            self.symbol = data[0]
            self.x = data[1]
            self.y = data[2]
            self.duration = data[3]
        
        self.release = self.symbol.lower()
        return

    def __str__(self):
        return f"({self.symbol}, {self.release}, {self.x}, {self.y}, {self.duration})"


def make_input_list(l):
    for i in range(len(l)):
        if type(l[i]) in (list, tuple, str):
            l[i] = Input(l[i])
    return l


def get_packet(inputs, x=0, y=0, r=False):
    if isinstance(inputs, Input):
        inputs = [inputs]

    packet = struct.pack("B", len(inputs))
    for i in inputs:
        s = i.release if r else i.symbol
        if s in ("<" or ">") and r:
            x = 128
            y = 128
        else:
            x = i.x
            y = i.y
        packet += struct.pack("cBB", s.encode(), x, y)
    print(packet)
    return packet


def quick_p(b, x=0, y=0):
    packet = struct.pack("B", 1)
    packet += struct.pack("cBB", b.encode(), x, y)
    print(packet)
    return packet


def main():
    inps = [
        ('A'),
        ('<', 255, 0),
        0.5,
        ('A'),
        0.5,
        ('0')
    ]

    with serial.Serial(SERIAL_PORT, 9600) as ser:
        for i in make_input_list(inps):
            print(i)
            if isinstance(i, Input):
                p, r = get_packet(i), get_packet(i, True)
                ser.write(p)
                print(p)
                sleep(i.duration)
                ser.write(r)
                print(r)
            else:
                sleep(float(i))
    return


def reset_training_mode():
    return get_packet(make_input_list(["L", "R", "A"]))


def dash_dance(ser, count=25, delay=0.075):
    # Clouds 0.07
    # No clouds 0.05
    LEFT = Input(("<", 0, 128))
    RIGHT = Input(("<", 255, 128))

    lp = get_packet(LEFT)
    rp = get_packet(RIGHT)


    for dd in range(count):
        sleep(delay)
        ser.write(rp)
        sleep(delay)
        ser.write(lp)

    ser.write(quick_p('0'))
    return


def tea_bag(ser, count=5):
    DOWN = Input(("<", 0, 255))

    dp = get_packet(DOWN)
    rp = quick_p("<", 128, 128)

    for i in range(count):
        sleep(0.09)
        ser.write(dp)
        sleep(0.09)
        ser.write(rp)

    ser.write(quick_p('0'))
    return

if __name__ == "__main__":
    ser = serial.Serial(SERIAL_PORT, 9600)
    ser.write(quick_p('0'))

    tea_bag(ser, 5)
    dash_dance(ser)
    ser.write(quick_p('0'))

    sleep(1)
    #ser.write(reset_training_mode())
    ser.close()