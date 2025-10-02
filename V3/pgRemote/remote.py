"""
96, 160
"""
import serial, struct, time
import platform

if platform.system() == "Windows":
    SERIAL_PORT = 'COM3'
elif platform.system() == "Linux":
    SERIAL_PORT = '/dev/ttyUSB0'
else:
    raise SystemError("Unknown OS")
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

UP_B = [UP, "B"]

right_electric = [
    [[], sRIGHT],
    [[], sDOWN],
    [['A'], (160, 160)]
]
left_electric = [
    [[], sLEFT],
    [[], sDOWN],
    [['A'], (96, 160)]
]
right_grab = [
    [[], (160, 160)],
    [[], sDOWN],
    [['L'], (160, 160)]
]
left_grab = [
    [[], (96, 160)],
    [[], sDOWN],
    [['L'], (96, 160)]
]

MOVEMENT_KEYS = {'w', 'a', 's', 'd', 'q', 'e'}

RESET_TRAINING_MODE = [[['L', 'R', 'A'], False]]

MACRO_MAP = {
    'Left': left_electric,
    'Right': right_electric,
    'Backspace': RESET_TRAINING_MODE
    # 'K8': [[['B'], UP]],
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
        x_move = {'a': 0, 'd': 255, 'q': 96, 'e': 160}
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
            time.sleep(0.05)
            self.hit([], RIGHT)
            time.sleep(0.05)
        return

    def macro(self, m):
        if m in MACRO_MAP:
            for i in MACRO_MAP[m]:
                p = self.make_packet(i[0], l_stick=i[1])
                self.ser.write(p)
                time.sleep(DEFAULT_PAUSE)
        elif m in ("K7", 'K9'):
            self.kazuya_zero_to_death(m == 'K7')
        elif m in ('Up', 'Down'):
            if self.facing_right:
                k_dir = (160, 160) if m == 'Up' else (96, 160)
            else:
                k_dir = (96, 160) if m == 'Up' else (160, 160)
            self.hit(['A'], k_dir)
            time.sleep(0.05)
        elif m == 'Tab':
            self.dash_dance()
        elif m == 'KPE':
            if self.facing_right:
                for i in right_grab:
                    p = self.make_packet(i[0], l_stick=i[1])
                    self.ser.write(p)
                    time.sleep(DEFAULT_PAUSE)
            else:
                for i in left_grab:
                    p = self.make_packet(i[0], l_stick=i[1])
                    self.ser.write(p)
                    time.sleep(DEFAULT_PAUSE)
        return

    def hit(self, inp, mov=False):
        self.ser.write(self.make_packet(inp, mov))
        return
