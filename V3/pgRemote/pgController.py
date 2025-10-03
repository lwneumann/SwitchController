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
        pygame.font.init()

        # --- Get internals
        # Remote Connection
        self.remote = remote.Remote()
        # Lists of active buttons
        self.held_keys = set()
        self.last_input = set()
        self.modes = [
            "Basic",
            "Kazuya",
            "Steve"
            ]
        self.mode_i = 0
        self.mode = self.modes[self.mode_i]
        self.font = pygame.font.SysFont('Arial', 24)
        
        # --- Make things
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        pygame.display.set_caption(SCREEN_TITLE)
        icon = pygame.image.load('../favicon.ico')
        pygame.display.set_icon(icon)
        self.draw()
        return

    def draw(self):
        self.screen.fill((0, 0, 0))
        mode_text = self.font.render(f"Mode: {self.mode}", True, (255, 255, 255))
        self.screen.blit(mode_text, (20, 20))
        pygame.display.update()
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
            pygame.K_t: 'R',
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
            "Basic": {
                pygame.K_TAB: 'Tab',
                pygame.K_BACKSPACE: 'Backspace'
            },
            "Kazuya": {
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
            },
            "Steve": {
                pygame.K_TAB: 'Tab',
                pygame.K_BACKSPACE: 'Backspace',
                pygame.K_f: 'F'
            }
        }

        while running:
            # --- Events and other keystrokes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Key downs
                elif event.type == pygame.KEYDOWN:
                    event.key == pygame.K_ESCAPE
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Prioritize Macros
                    elif event.key in macro_map.get(self.mode, "Basic"):
                        self.remote.macro(macro_map.get(self.mode, "Basic")[event.key], self.mode)
                    # Normal Presses
                    elif event.key in key_map:
                        self.held_keys.add(key_map[event.key])
                    # Toggle Mode
                    elif event.key == pygame.K_F1:
                        self.mode_i = (self.mode_i + 1)%len(self.modes)
                        self.mode = self.modes[self.mode_i]
                        self.draw()
                    elif event.key == pygame.K_F2:
                        self.mode_i = (self.mode_i - 1)%len(self.modes)
                        self.mode = self.modes[self.mode_i]
                        self.draw()
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
