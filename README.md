# Switch Controller



## Usage

To build and flash the firmware:

```sh
make MCU=atmega32u4

sudo avrdude -patmega32u4 -cavr109 -P /dev/ttyACM0 -U flash:w:main.hex
```

- **MCU**: Chip name (e.g., atmega32u4)
- **-c**: AVR programmer type
- **-P**: Serial port where microcontroller is connected
- **-U**: Flash write file (`main.hex`)

---

## Inputs

All possible inputs are listed below. Some choices use single letters for simplicity.

### Stick
**Stick Positions:**

**x, y**: Values from `0-255` for left and right stick positions, for example

| Direction | (x, y)    |
|-----------|-----------|
| Left      | (0, 128)  |
| Right     | (255, 128)|
| Up        | (128, 0)  |
| Down      | (128, 255)|
| Neutral   | (128, 128)|


### Buttons

| Input | Button              |
|-------|---------------------|
| A     | A                   |
| B     | B                   |
| X     | X                   |
| Y     | Y                   |
| U     | Clicking Left Stick |
| I     | Clicking Right Stick|
| L     | Left Bumper         |
| R     | Right Bumper        |
| Z     | Left Trigger        |
| V     | Right Trigger       |
| P     | Plus                |
| M     | Minus               |
| H     | Home                |
| C     | Capture             |

### D-Pad

| Input | Direction |
|-------|-----------|
| 1     | Up        |
| 2     | Down      |
| 3     | Left      |
| 4     | Right     |
| D     | Center    |

### Commands

- `0`: Reset inputs to neutral

---

## Firmware Input Packets

**Structure:**

The arduinon expects a serial packet containing any new inputs (single charecters from above). Those inputs are pressed until a new input is received. If you press A then B, A will be released. Using the same encoding as from [`struct`](https://docs.python.org/3/library/struct.html); packing goes as follows;

`?[BB]?[BB]B[c...]`


- `?`: Move Left
  - `B` Left x
  - `B` Left y
- `?`: Move Right
  - `B` Right x
  - `B` Right y
- `B`: Number of Commands
  - `c` some number of commands (from above)
