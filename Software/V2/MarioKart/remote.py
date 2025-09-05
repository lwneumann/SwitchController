"""
96, 160
"""
import serial, struct, time


SERIAL_PORT = SERIAL_PORT = '/dev/ttyUSB0'
DEFAULT_PAUSE = 0.04

LEFT = (0, 128)
RIGHT = (255, 128)
UP = (128, 0)
DOWN = (128, 255)
NEUTRAL = (128, 128)

sLEFT = (96, 128)
sRIGHT = (160, 128)
sUP = (128, 96)
sDOWN = (128, 160)

sDRIGHT = (160, 160)
sDLEFT = (90, 160)


class Remote:
    def __init__(self):
        self.ser = serial.Serial(SERIAL_PORT, 9600)
        self.auto_release = True
        return

    def make_packet(self, inputs, l_stick=False):
        # Who up moving their sticks
        moving_l = l_stick is not False

        # Write Sticks
        packet = struct.pack("?", moving_l)
        if moving_l:
            packet += struct.pack("BB", l_stick[0], l_stick[1])

        # Mario Kart doesn't need C-Stick
        packet += struct.pack("?", False)

        # Write commands
        packet += struct.pack("B", len(inputs))
        for c in inputs:
            packet += struct.pack("c", c.encode())
        print(packet)
        return packet

    def press(self, inp, m=False):
        self.ser.write(self.make_packet(inp, m))
        if self.auto_release:
            time.sleep(0.05)
            self.reset()
        return

    def reset(self):
        self.ser.write(self.make_packet('0'))
        return

    def close_ser(self):
        self.ser.close()
        return

    def tilt(self, dir):
        self.press([], m=dir)
        return

    def reset_race(self):
        # Reset Time trial
        print('\n-- Reset Race')
        self.press("P")
        time.sleep(0.1)
        self.tilt(DOWN)
        time.sleep(0.05)
        self.reset()
        time.sleep(0.1)
        return

    def repair(self):
        self.press(['L', 'R'])
        time.sleep(1)
        self.press('A')
        self.press('A')
        return

    # Anti Cuts
    def royal_raceway(self):
        print('\n-- Starting Race')
        self.press('A')

        # Prep your engines
        time.sleep(9.05)
        print('-> 3.. 2.. 1..')
        self.auto_release = False
        self.press('A')

        # First Bend
        time.sleep(4)
        print('\n-- First AC')
        self.press(['R', 'A'], (40, 128))
        time.sleep(0.5)
        self.press(['R', 'A'], (180, 128))
        time.sleep(0.2)
        self.press(['R', 'A'], (20, 128))
        time.sleep(0.6)
        self.press(['R', 'A'], (180, 128))
        time.sleep(0.1)
        self.press(['R', 'A'], (0, 128))
        time.sleep(0.7)
        self.press(['R', 'A'], NEUTRAL)
        time.sleep(0.3)
        self.press('A', (255, 128))
        time.sleep(0.1)
        self.press(['A', 'R'], (255, 128))
        time.sleep(0.1)
        self.press('A')
        time.sleep(2)

        self.auto_release = True
        return


def royal_raceway_ac():
    r = Remote()
    r.reset()

    # Reset
    r.reset_race()
    r.press('A')
    print('-> Ensuring Loading Sync')
    time.sleep(12)
    r.reset_race()
    print('-> Synched Load')

    # Run
    r.royal_raceway()
    print('\n-- Rahhh')
    r.press('P')
    time.sleep(4)
    r.press('P')
    return

if __name__ == "__main__":
    royal_raceway_ac()
    # Remote().repair()
