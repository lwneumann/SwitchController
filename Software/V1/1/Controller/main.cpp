#include <Arduino.h>
#include <HID.h>

static const uint8_t _desc_data[] PROGMEM = {
    0x05, 0x01,
    0x09, 0x05,
    0xa1, 0x01,

    0x15, 0x00,
    0x25, 0x01,
    0x35, 0x00,
    0x45, 0x01,

    0x75, 0x01,
    0x95, 0x10,
    0x05, 0x09,
    0x19, 0x01,
    0x29, 0x10,

    0x81, 0x02,
    0x05, 0x01,
    0x25, 0x07, 0x46,
    0x3b, 0x01,
    0x75, 0x04,
    0x95, 0x01,
    0x65, 0x14,
    0x09, 0x39,

    0x81, 0x42,
    0x65, 0x00,
    0x95, 0x01,

    0x81, 0x01, 0x26,
    0xff, 0x00, 0x46,
    0xff, 0x00,
    0x09, 0x30,
    0x09, 0x31,
    0x09, 0x32,
    0x09, 0x35,
    0x75, 0x08,
    0x95, 0x04,

    0x81, 0x02, 0x06,
    0x00, 0xff,
    0x09, 0x20,
    0x95, 0x01,

    0x81, 0x02, 0x0a,
    0x21, 0x26,
    0x95, 0x08,
    0x91, 0x02,

    0xc0
};
static HIDSubDescriptor _desc{_desc_data, sizeof(_desc_data)};

class HIDWithoutReportID : public HID_ {
    public:
        int send_report(const void* data, size_t len) {
            // the switch does not use report ids
            return USB_Send(pluggedEndpoint | TRANSFER_RELEASE, data, len);
        }
};

typedef enum {
    BUTTON_Y       = 0x01,
    BUTTON_B       = 0x02,
    BUTTON_A       = 0x04,
    BUTTON_X       = 0x08,
    BUTTON_L       = 0x10,
    BUTTON_R       = 0x20,
    BUTTON_ZL      = 0x40,
    BUTTON_ZR      = 0x80,
    BUTTON_MINUS   = 0x100,
    BUTTON_PLUS    = 0x200,
    BUTTON_LCLICK  = 0x400,
    BUTTON_RCLICK  = 0x800,
    BUTTON_HOME    = 0x1000,
    BUTTON_CAPTURE = 0x2000,
} Buttons_t;

#define DPAD_TOP          0x00
#define DPAD_TOP_RIGHT    0x01
#define DPAD_RIGHT        0x02
#define DPAD_BOTTOM_RIGHT 0x03
#define DPAD_BOTTOM       0x04
#define DPAD_BOTTOM_LEFT  0x05
#define DPAD_LEFT         0x06
#define DPAD_TOP_LEFT     0x07
#define DPAD_CENTER       0x08

#define STICK_MIN      0
#define STICK_CENTER 128
#define STICK_MAX    255

typedef struct {
    uint16_t button;
    uint8_t dpad;
    uint8_t lx;
    uint8_t ly;
    uint8_t rx;
    uint8_t ry;
    uint8_t _unused;
} Report_t;

void reset_report(Report_t* report) {
    // Neutral joystick position
    report->lx = 128;
    report->ly = 128;
    report->rx = 128;
    report->ry = 128;
    // No buttons pressed
    report->button = 0;
}

void make_report(Report_t* report, char command, uint8_t x, uint8_t y) {
    // This retains button presses from input to input allowing for
    // continuous inputs like holding right while pressing other buttons
    // along the way.
    // This does mean that inputs need to be reset manually by the external
    // program.
    
    switch (command) {
        // Left joystick
        case '<':
            report->lx = x;
            report->ly = y;
            break;
        // Right joystick
        case '>':
            report->rx = x;
            report->ry = y;
            break;

        // --- Button Presses ---
        case 'A':
            report->button |= BUTTON_A;
            break;
        case 'a':
            report->button &= ~BUTTON_A;
            break;
        case 'B':
            report->button |= BUTTON_B;
            break;
        case 'b':
            report->button &= ~BUTTON_B;
            break;
        case 'X':
            report->button |= BUTTON_X;
            break;
        case 'x':
            report->button &= ~BUTTON_X;
            break;
        case 'Y':
            report->button |= BUTTON_Y;
            break;
        case 'y':
            report->button &= ~BUTTON_Y;
            break;
        
        // Triggers
        case 'Z':
            report->button |= BUTTON_ZL;
            break;
        case 'z':
            report->button &= ~BUTTON_ZL;
            break;
        case 'V':
            report->button |= BUTTON_ZR;
            break;
        case 'v':
            report->button &= ~BUTTON_ZR;
            break;
        // Bumpers
        case 'L':
            report->button |= BUTTON_L;
            break;
        case 'l':
            report->button &= ~BUTTON_L;
            break;
        case 'R':
            report->button |= BUTTON_R;
            break;
        case 'r':
            report->button &= ~BUTTON_R;
            break;

        // -- Joy Stick --
        case 'U':
            report->button |= BUTTON_LCLICK;
            break;
        case 'u':
            report->button &= ~BUTTON_LCLICK;
            break;
        case 'I':
            report->button |= BUTTON_RCLICK;
            break;
        case 'i':
            report->button &= ~BUTTON_RCLICK;
            break;

        // D-Pad
        case '1':
            report->dpad |= DPAD_TOP;
            break;
        case '5':
            report->dpad &= ~DPAD_TOP;
            break;
        case '2':
            report->dpad |= DPAD_BOTTOM;
            break;
        case '6':
            report->dpad &= ~DPAD_BOTTOM;
            break;
        case '3':
            report->dpad |= DPAD_LEFT;
            break;
        case '7':
            report->dpad &= ~DPAD_LEFT;
            break;
        case '4':
            report->dpad |= DPAD_RIGHT;
            break;
        case '8':
            report->dpad &= ~DPAD_RIGHT;
            break;


        // --- Other Buttons ---
        case 'P':
            report->button |= BUTTON_PLUS;
            break;
        case 'p':
            report->button &= ~BUTTON_PLUS;
            break;
        case 'M':
            report->button |= BUTTON_MINUS;
            break;
        case 'm':
            report->button &= ~BUTTON_MINUS;
            break;
        case 'H':
            report->button |= BUTTON_HOME;
            break;
        case 'h':
            report->button &= ~BUTTON_HOME;
            break;
        case 'C':
            report->button |= BUTTON_CAPTURE;
            break;
        case 'c':
            report->button &= ~BUTTON_CAPTURE;
            break;
        
        // --- Commands ---
        case '0':
            reset_report(report);
            break;
                
    }
}

uint8_t serial_read_blocking() {
    // Wait until serial is ready
    while (!Serial1.available());
    return Serial1.read();
}

int main() {
    init();

    USBDevice.attach();

    HIDWithoutReportID hid;
    hid.AppendDescriptor(&_desc);

    // classic baud amiright
    Serial1.begin(9600);

    Report_t report;
    reset_report(&report);

    uint8_t x = 0;
    uint8_t y = 0;
    while (true) {
        if (Serial1.available()) {
            // Read the number of commands in the packet
            uint8_t num_commands = serial_read_blocking();

            // This allows for multiple commands per packet so you can
            // press something like down and B at the same time.
            for (uint8_t i = 0; i < num_commands; i++) {
                // Button / stick
                char command = serial_read_blocking();
                // x
                uint8_t x = serial_read_blocking();
                // y
                uint8_t y = serial_read_blocking();

                make_report(&report, command, x, y);
            }
            // Send report after compiling all inputs
            hid.send_report(&report, sizeof(Report_t));
        }
    }
}