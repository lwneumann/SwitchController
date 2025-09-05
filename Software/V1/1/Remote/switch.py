"""
------------------------------------------------
- Inputs                                       -
------------------------------------------------

Here are all inputs. Note that for the sake of not doing something like +, = or -, _ some choices are note as clear as they could have been.

Stick -
    x, y

Buttons -
    [Press], [Release] - Input

    A, a - A
    B, b - B
    X, x - X
    Y, y - Y

    U, u - Clicking Left Joystick
    I, i - Clicking Right Joystick

    L, l - Left Bumper
    R, r - Right Bumper
    Z, z - Left Trigger
    V, v - Right Trigger

    P, p - Plus
    M, m - Minus

    H, h - Home
    C, c - Capture

D-Pad - 
    1, 5 - Up
    2, 6 - Down
    3, 7 - Left
    4, 8 - Right

Commands -
    0 - Reset inputs to neutral
"""
import time, struct


SERIAL_PORT = '/dev/ttyUSB0'


def make_packet(inps):
    """
    inps:
        - Single input
        - List of inputs to all be pressed at once
    """
    packet = struct.pack("B", len(inps))
    for m in inps:
        if m in ("<", ">"):
            x = m[1]
            y = m[2]
        else:
            x = 0
            y = 0
        packet += struct.pack("cBB", m[0].encode(), x, y)
    return packet


class Remote:
    def __init__(self):
        # Serial
        self.ser = serial.Serial(SERIAL_PORT, 9600)
        
        # Defaults
        self.default_duration = 0.1
        self.default_pause = 0.1

        # Common packets
        self.reset_packet = make_packet('0')
        return

    def close_ser(self):
        # Close serial just to be nice.
        # Probably often won't get called due to a crash
        self.ser.close()
        return

    def reset(self):
        self.ser.write(self.reset_packet)
        return

    def press(self, buttons, x=0, y=0):
        """
        buttons:
            - Single input
            - List of inputs to all be pressed at once
        """
        p = make_packet(buttons)
        self.ser.write(p)
        return 

    def input_sequence(self):
        """
        Sequence is a list of inputs to be run through.
        
        Each input has:
            - input (same as defined above)
            - duration (how long until it is released)
            - pause (how long before the next input is pressed)

        Example: (
                # Press A, default duration and pause used
            ["A"],
                # Press B, duration of 2, default pause
            ["B", 2],
                # Press up (Left) and B for two seconds, default pause
            [[["<", 128, 255], "B"], 2],
                # Flick left on right stick
            [">", 0, 128]
        )
        """

        return

if __name__ == "__main__":
    pass
