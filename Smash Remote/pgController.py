import remote
import pygame, sys


SCREEN_TITLE = ':)'
SCREEN_SIZE = (400, 600)
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
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 12)
        self.key_map = {
            # Basic controls
            pygame.K_w: 'w',
            pygame.K_a: 'a',
            pygame.K_s: 's',
            pygame.K_d: 'd',
            pygame.K_q: 'q',
            pygame.K_e: 'e',
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
        self.macro_map = {
            "Basic": {
                pygame.K_TAB: 'Tab',
                pygame.K_BACKSPACE: 'Backspace'
            },
            "Kazuya": {
                pygame.K_TAB: 'Tab',
                pygame.K_BACKSPACE: 'Backspace',
                pygame.K_KP1: 'KP1',
                pygame.K_KP2: 'KP2',
                pygame.K_KP3: 'KP3',
                pygame.K_KP5: 'KP5',
                pygame.K_KP7: 'K7',
                pygame.K_KP9: 'K9',
                pygame.K_KP8: 'K8',
                pygame.K_KP_ENTER: 'KPE',
            },
            "Steve": {
                pygame.K_TAB: 'Tab',
                pygame.K_BACKSPACE: 'Backspace',
                pygame.K_f: 'F'
            },
            "FGC": {
                pygame.K_TAB: 'Tab',
                pygame.K_BACKSPACE: 'Backspace',
                pygame.K_KP1: 'KP1',
                pygame.K_KP3: 'KP3'
            }
        }
        self.modes = list(self.macro_map.keys())
        self.mode_i = 0
        self.mode = self.modes[self.mode_i]

        # --- Make things
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        pygame.display.set_caption(SCREEN_TITLE)
        icon = pygame.image.load('../favicon.ico')
        pygame.display.set_icon(icon)
        self.draw()
        return

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Keys
        key_header = self.font.render("Controls", True, (92, 184, 223))
        self.screen.blit(key_header, (25, 10))
        key_w = 0
        for k_i, k in enumerate(self.key_map):
            key_text = self.font.render(pygame.key.name(k) + ': ' + self.key_map[k], True, (255, 255, 255))
            h = key_text.get_height()
            self.screen.blit(key_text, (25, 40 + (h+2)*k_i))
            this_w = key_text.get_width()
            if this_w > key_w:
                key_w = this_w

        # Modes
        mode_header = self.font.render("Modes", True, (92, 184, 223))
        self.screen.blit(mode_header, (30 + key_w, 10))
        mode_w = 0
        for m_i, m in enumerate(self.modes):
            mode_text = self.font.render(m, True, (255, 255, 255))
            h = mode_text.get_height()
            self.screen.blit(mode_text, (30 + key_w, 40 + (h+2)*m_i))

            w = mode_text.get_width()
            if w > mode_w:
                mode_w = w
            if self.mode_i == m_i:
                selector = self.font.render('>', True, (123, 229, 255))
                self.screen.blit(selector, (30 + key_w - selector.get_width(), 40 + (h+2)*m_i))


        # Macros
        macro_header = self.font.render("Macros", True, (92, 184, 223))
        self.screen.blit(macro_header, (50 + key_w + mode_w, 10))
        for m_i, mac in enumerate(self.macro_map[self.mode].values()):
            mac_text = self.font.render(mac, True, (255, 255, 255))
            h = mac_text.get_height()
            self.screen.blit(mac_text, (50 + key_w + mode_w, 40 + (h+2)*m_i))

        pygame.display.update()
        return

    def run(self):
        running = True
        clock = pygame.time.Clock()

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
                    elif event.key in self.macro_map.get(self.mode, "Basic"):
                        self.remote.macro(self.macro_map.get(self.mode, "Basic")[event.key], self.mode)
                    # Normal Presses
                    elif event.key in self.key_map:
                        self.held_keys.add(self.key_map[event.key])
                    # Toggle Mode
                    elif event.key == pygame.K_F1:
                        self.mode_i = (self.mode_i - 1)%len(self.modes)
                        self.mode = self.modes[self.mode_i]
                        self.draw()
                    elif event.key == pygame.K_F2:
                        self.mode_i = (self.mode_i + 1)%len(self.modes)
                        self.mode = self.modes[self.mode_i]
                        self.draw()
                elif event.type == pygame.KEYUP:
                    if event.key in self.key_map:
                        self.held_keys.discard(self.key_map[event.key])

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
