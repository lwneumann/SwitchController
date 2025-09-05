import remote
import pygame, sys


SCREEN_TITLE = ':)'
SCREEN_SIZE = (500, 500)
FPS = 60


class Window:
    def __init__(self):
        self.setup()
        self.run()
        return

    def setup(self):
        # --- Setup
        pygame.init()

        # --- Make things
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        pygame.display.set_caption(SCREEN_TITLE)
        self.screen.fill((0, 0, 0))
        pygame.display.update()

        # --- Get internals
        # Remote Connection
        self.remote = remote.Remote()
        # Lists of active buttons
        self.held_keys = set()
        self.last_input = set()
        return

    def run(self):
        running = True
        clock = pygame.time.Clock()

        key_map = {
            # Basic
            pygame.K_w: 'w',
            pygame.K_a: 'a',
            pygame.K_s: 's',
            pygame.K_d: 'd',
            pygame.K_SPACE: 'X',
            pygame.K_LSHIFT: 'V',
            pygame.K_LCTRL: 'L',
            pygame.K_KP0: '0',
            pygame.K_KP4: 'A',
            pygame.K_KP6: 'B',
            pygame.K_h: 'H',
            pygame.K_p: 'P',
            pygame.K_y: 'Y',
            pygame.K_c: 'C'
        }
        macro_map = {
            pygame.K_COMMA: ',',
            pygame.K_PERIOD: '.',
            pygame.K_SLASH: '/',
            pygame.K_KP1: 'Left',
            pygame.K_KP3: 'Right',
            pygame.K_KP5: 'Up',
            pygame.K_KP2: 'Down',
            pygame.K_KP7: 'K7',
            pygame.K_KP9: 'K9',
            pygame.K_KP8: 'K8',
            pygame.K_l: 'mL',
            pygame.K_BACKSPACE: 'Backspace',
            pygame.K_QUOTE: "'",
            pygame.K_SEMICOLON: ';',
            pygame.K_TAB: 'Tab',
            pygame.K_RSHIFT: 'RShift',
            pygame.K_KP_ENTER: 'KPE'
        }

        while running:
            # --- Events and other keystrokes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Key downs
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Prioritize Macros
                    elif event.key in macro_map:
                        self.remote.macro(macro_map[event.key])
                    # Normal Presses
                    elif event.key in key_map:
                        self.held_keys.add(key_map[event.key])
                elif event.type == pygame.KEYUP:
                    if event.key in key_map:
                        self.held_keys.discard(key_map[event.key])

            # Update
            if self.held_keys != self.last_input:
                self.remote.press(self.held_keys)
                self.last_input = self.held_keys.copy()
            # Maintain FPS
            clock.tick(FPS)

        # Close
        self.remote.close_ser()
        pygame.quit()
        return


if __name__ == "__main__":
    Window()
