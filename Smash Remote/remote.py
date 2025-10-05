"""
96, 160
"""
import serial, struct
from time import sleep
import platform

# This could change based on physical port remote is plugged into
if platform.system() == "Windows":
    SERIAL_PORT = 'COM3'
elif platform.system() == "Linux":
    SERIAL_PORT = '/dev/ttyUSB0'
else:
    raise SystemError("Unknown OS")
DEFAULT_PAUSE = 0.04

# Hard directions
LEFT = (0, 128)
RIGHT = (255, 128)
UP = (128, 0)
DOWN = (128, 255)
NEUTRAL = (128, 128)
DLEFT = (0, 255)
DRIGHT = (255, 255)
# Soft Directions
sLEFT = (96, 128)
sRIGHT = (160, 128)
sUP = (128, 96)
sDOWN = (128, 160)
sDLEFT = (96, 160)
sDRIGHT = (160, 160)


# Kazuya
right_electric = [
    [[], sRIGHT],
    [[], sDOWN],
    [['A'], sDRIGHT]
]
left_electric = [
    [[], sLEFT],
    [[], sDOWN],
    [['A'], sDLEFT]
]
right_grab = [
    [[], sDRIGHT],
    [[], sDOWN],
    [['L'], sDRIGHT]
]
left_grab = [
    [[], sDLEFT],
    [[], sDOWN],
    [['L'], sDLEFT]
]
# FGC
right_quarter = [
    [[], DOWN],
    [[], DRIGHT],
    [[], RIGHT]
]
left_quarter = [
    [[], DOWN],
    [[], DLEFT],
    [[], LEFT]
]
right_semi = [
    [[], sLEFT],
    [[], sDLEFT],
    [[], sDOWN],
    [[], sDRIGHT],
    [[], sRIGHT]
]
left_semi = [
    [[], sRIGHT],
    [[], sDRIGHT],
    [[], sDOWN],
    [[], sDLEFT],
    [[], sLEFT]
]
right_z = [
    [[], sRIGHT],
    [[], sDOWN],
    [[], sDRIGHT]
]
left_z = [
    [[], sLEFT],
    [[], sDOWN],
    [[], sDLEFT]
]

MOVEMENT_KEYS = {'w', 'a', 's', 'd', 'q', 'e'}

RESET_TRAINING_MODE = [[['L', 'R', 'A'], False]]

MACRO_MAP = {
    'Basic': {'Backspace': RESET_TRAINING_MODE},
    'Kazuya': {
        'KP1': left_electric,
        'KP3': right_electric,
        'Backspace': RESET_TRAINING_MODE
    },
    'FGC': {
        'Backspace': RESET_TRAINING_MODE
    }
}


class Remote:
    def __init__(self):
        self.ser = serial.Serial(SERIAL_PORT, 9600)
        self.facing_right = True
        return

    def make_packet(self, inputs, l_stick=False, r_stick=False):
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
        print(packet)
        return packet

    def reset(self):
        # Resets all held inputs
        self.ser.write(self.make_packet('0'))
        return

    def close_ser(self):
        # Closes connection
        self.ser.close()
        return

    def convert_inputs(self, inputs):
        # Seperates Left Joystick inputs from buttons
        movement = [x for x in inputs if x in MOVEMENT_KEYS]
        buttons = [x for x in inputs if x not in MOVEMENT_KEYS]

        if movement == []:
            movement = False

        return buttons, movement

    def get_movement(self, movements):
        # Moves left joystick
        x_move = {'a': 0, 'd': 255, 'q': 90, 'e': 166}
        y_move = {'w': 0, 's': 255, }

        x = 128
        y = 128

        for m in movements:
            if m in x_move:
                x = x_move[m] if x == 128 else 128
            if m in y_move:
                y = y_move[m] if y == 128 else 128

        # Update Facing
        if x < 128:
            self.facing_right = False
        elif x > 128:
            self.facing_right = True
        return x, y

    def press(self, inputs):
        if inputs == set():
            inputs = '0'
        buttons, movement = self.convert_inputs(inputs)
        
        if movement:
            movement = self.get_movement(movement)

        packet = self.make_packet(buttons, l_stick=movement)

        self.ser.write(packet)
        return

    # --- Macros

    def dash_dance(self, n=5):
        for i in range(n):
            self.hit([], LEFT)
            sleep(0.05)
            self.hit([], RIGHT)
            sleep(0.05)
        self.reset()
        return

    def run_macro(self, macro):
        for i in macro:
            p = self.make_packet(i[0], l_stick=i[1])
            self.ser.write(p)
            sleep(DEFAULT_PAUSE)
            self.reset()
        return

    def macro(self, m, mode):
        if m in MACRO_MAP.get(mode, 'Basic'):
            self.run_macro(MACRO_MAP.get(mode, 'Basic')[m])
        if m == 'Tab':
            self.dash_dance()
        # Kazuya
        elif mode == 'Kazuya':
            if m in ("K7", 'K9'):
                self.kazuya_zero_to_death(m == 'K7')
            elif m in ('KP5', 'KP2'):
                if self.facing_right:
                    k_dir = (160, 160) if m == 'KP5' else (96, 160)
                else:
                    k_dir = (96, 160) if m == 'KP5' else (160, 160)
                self.hit(['A'], k_dir)
                sleep(0.05)
                self.reset()
            elif m == 'KPE':
                if self.facing_right:
                    for i in right_grab:
                        p = self.make_packet(i[0], l_stick=i[1])
                        self.ser.write(p)
                        sleep(DEFAULT_PAUSE)
                else:
                    for i in left_grab:
                        p = self.make_packet(i[0], l_stick=i[1])
                        self.ser.write(p)
                        sleep(DEFAULT_PAUSE)
                self.reset()
        # Steve
        elif mode == "Steve":
            if m == 'F':
                self.steve_f()
        # FGC
        elif mode == "FGC":
            if m == "KP3":
                self.run_macro(right_quarter)
            elif m == "KP1":
                self.run_macro(left_quarter)
            elif m == "KP2":
                self.run_macro(right_semi if self.facing_right else left_semi)
        return

    def hit(self, inp, mov=False):
        self.ser.write(self.make_packet(inp, mov))
        return

    def tap(self, *args):
        if len(args) > 3:
            raise ValueError("tap() expects no more than 3 arguments: inputs, [movement], duration")

        inp = args[0]
        mov = args[1] if len(args) == 3 else False
        duration = args[-1] if len(args) > 1 and isinstance(args[-1], (int, float)) else 0.05

        self.hit(inp, mov)
        sleep(duration)
        self.reset()
        return

    def kazuya_zero_to_death(self, facing_right):
        diff = -1 if facing_right else 1
        soft_dir = (128 + 50*diff, 128)
        hard_dir = (min(128 + 128*diff, 255), 128)

        # dash
        self.hit([], hard_dir)
        sleep(0.06)
        self.hit('X')
        sleep(0.03)
        self.hit('A')
        sleep(0.06)
        self.reset()
        return
    
    def steve_f(self):
        self.tap('X', 0.4)
        self.tap('X', 0.4)
        self.tap('B')
        self.tap('', LEFT, 0.1)
        return
    
    def steve_nod(self, n=5):
        for i in range(n):
            pass
        return