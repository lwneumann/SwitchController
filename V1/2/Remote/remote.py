"""
USING VERSION 1

Minimum input
96, 160
"""
import serial, struct, time

SPF = 0.05
DEFAULT_DURATION = 0

LEFT = ("<", 0, 128)
RIGHT = ("<", 255, 128)
UP = ("<", 128, 0)
DOWN = ("<", 128, 255)

sLEFT = ("<", 96, 128)
sRIGHT = ("<", 160, 128)
sUP = ("<", 128, 96)
sDOWN = ("<", 128, 160)

UP_B = [UP, "B"]

right_electric = [
    [sRIGHT, SPF],
    [sDOWN, SPF],
    [[("<", 160, 160), "A"], SPF],
    ['0']
]
left_electric = [
    [sLEFT, SPF],
    [sDOWN, SPF],
    [[("<", 96, 160), "A"], 0.05],
    ['0']
]


def get_packet(inputs):
    """
    Inputs should be single input or list of inputs seen in notes.txt Inputs.
    These inputs are to be pressed simultaneously.

    When using joy stick movement-
        <, > for left and right but should be an interable with x, y
        EX:
            ("<", 0, 128)
            (">", 255, 128)

    
    Examples:
        # Down B
        - get_packet(
            [("<", 128, 255),
            "B"]
        )

        # A
        - get_packet("A")
        
        # Up on both sticks
        - get_packet(
            [("<", 128, 0),
            (">", 128, 0)]
        )
    """
    # Get packet for series of inputs be excecuted at once
    print(inputs)
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


# Just linux atm. Change for OS
# Randomly changed to 1 idk why >:(
SERIAL_PORT = '/dev/ttyUSB0'
# Useful Packet
RESET_PACKET = get_packet('0')


class Remote:
    def __init__(self):
        # Setup serial
        self.ser = serial.Serial(SERIAL_PORT, 9600)
        return

    def close_ser(self):
        self.ser.close()
        return

    def press(self, inputs):
        self.ser.write(get_packet(inputs))
        return

    def reset(self):
        self.ser.write(RESET_PACKET)
        return

    def do_input(self, inps, tap=False, auto_endcap=True):
        """
        inps is list of inputs for press with pause and tap
        For inputs see the documentiation for that in like get_packet or something

        pause               - time until next input
        duration (optional) - hold input
        """
        if inps[0] in ("<", ">"):
            inps = [inps[:3]]

        d_tap = tap
        for i in inps:
            tap = d_tap
            duration = DEFAULT_DURATION
            pause = SPF
            if i[0] not in ("<", ">"):
                if len(i) == 3:
                    duration = i.pop(3)
                    tap = True
                if len(i) > 1:
                    pause = i.pop(1)

            if i[0] in ("<", ">"):
                i = [i]
            for I in i:
                self.press(I)
            time.sleep(duration)
            if tap:
                self.reset()
            time.sleep(pause)
        return