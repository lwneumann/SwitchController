import remote
import pygame


SCREEN_TITLE = ':)'
SCREEN_SIZE = (250, 70)
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
        icon = pygame.image.load('../favicon.ico')
        pygame.display.set_icon(icon)

        # --- Get internals
        # Remote Connection
        self.remote = remote.Remote()
        # Lists of active buttons
        self.held_keys = set()
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

        while running:
            # --- Events and other keystrokes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break
                    elif event.key in key_map:
                        self.held_keys.add(key_map[event.key])
                elif event.type == pygame.KEYUP:
                    if event.key in key_map:
                        self.held_keys.discard(key_map[event.key])

            # Update
            self.remote.press(self.held_keys)

            # Maintain FPS
            clock.tick(FPS)

        # Close
        pygame.font.quit()
        pygame.quit()
        return


if __name__ == "__main__":
    Window()
