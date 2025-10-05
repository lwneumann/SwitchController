"""
96, 160
"""
import serial, struct, time
from time import sleep
import platform


if platform.system() == "Windows":
    SERIAL_PORT = 'COM3'
elif platform.system() == "Linux":
    SERIAL_PORT = '/dev/ttyUSB0'
else:
    raise SystemError("Unknown OS")
DEFAULT_PAUSE = 0.04


class Remote:
    def __init__(self):
        self.ser = serial.Serial(SERIAL_PORT, 9600)
        return

    def make_packet(self, inputs=[], l_stick=False, r_stick=False):
        # Writes serial command to serial

        # Who up moving their sticks
        moving_l = l_stick is not False
        moving_r = r_stick is not False

        # Write Sticks
        packet = struct.pack("?", moving_l)
        if moving_l:
            packet += struct.pack("BB", l_stick[0], l_stick[1])

        packet += struct.pack("?", moving_r)
        if moving_r:
            packet += struct.pack("BB", r_stick[0], r_stick[1])

        # Write commands
        packet += struct.pack("B", len(inputs))
        for c in inputs:
            packet += struct.pack("c", c.encode())
        
        return packet

    def close_ser(self):
        # Closes connection
        self.ser.close()
        return
    
    def reset(self):
        # Resets all held inputs
        self.ser.write(self.make_packet('0'))
        return

    def wakeup(self):
        # Wakeup the switch
        self.press('H')
        sleep(4)
        self.reset()
        return

    def get_movement(self, movements):
        # Moves left joystick
        x_move = {
            'q': 0,
            'e': 255,
            'a': 0,
            'd': 255,
            'z': 0,
            'c': 255
            }
        y_move = {
            'q': 0,
            'w': 0,
            'e': 0,
            'z': 255,
            'x': 255,
            'c': 255
            }

        x = 128
        y = 128

        for m in movements:
            if m in x_move:
                x = x_move[m] if x == 128 else 128
            if m in y_move:
                y = y_move[m] if y == 128 else 128

        return x, y

    def press(self, buttons=[], movement=[]):
        movement = self.get_movement(movement)
        packet = self.make_packet(buttons, l_stick=movement)
        self.ser.write(packet)
        return

    def move(self, *args):
        """
        Accepts move(x, y) or move((x, y))
        """
        if len(args) == 1 and isinstance(args[0], (tuple, list)) and len(args[0]) == 2:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        else:
            raise ValueError("move() requires either (x, y) or ((x, y))")
        packet = self.make_packet(l_stick=(x, y))
        self.ser.write(packet)
        return

    def tap(self, movement=[], buttons=[], delay=0.1):
        self.press(buttons=buttons, movement=movement)
        sleep(delay)
        self.reset()
        return