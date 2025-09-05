"""
Controls

A           - Attack
B           - Special
X, Y        - Jump

Triggers    - Shield
Bumper      - Grab

Tap Jump    - Off
Sensitivity - Normal
AB Smash    - On
"""
# Directions
LEFT = ("<", 0, 128)
RIGHT = ("<", 255, 128)
UP = ("<", 128, 0)
DOWN = ("<", 128, 255)


# Mappings
DEFAULT = {
    'w': UP,
    'a': LEFT,
    's': DOWN,
    'd': RIGHT,
    # Jump
    ' ': 'X',
    # Attack
    'Left': "A",
    # Right
    'Right': "B",
    # Grab
    "LShift": "L",
    # Shield
    "LControl": "ZL",
    # Specials
    'Up': None,
    'Down': None
}

KAZUYA = DEFAULT.copy()
KAZUYA['Left'] = 'LElectric'
KAZUYA['Right'] = 'RElectric'
KAZUYA['Up'] = 'B'

print(DEFAULT)
print(KAZUYA)