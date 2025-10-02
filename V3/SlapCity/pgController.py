import remote
import pygame, sys


SCREEN_TITLE = ':)'
SCREEN_SIZE = (250, 70)
FPS = 60


class Window:
    def __init__(self, verbose):
        self.verbose = verbose
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
            pygame.K_SPACE: ' ',
            pygame.K_LEFT: 'Left',
            pygame.K_RIGHT: 'Right',
            pygame.K_LSHIFT: "LShift",
            pygame.K_LCTRL: "LControl",
            # Special
            pygame.K_UP: 'Up',
            pygame.K_DOWN: 'Down'
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
            if self.held_keys != self.last_input:
                if self.verbose:
                    print('p ', self.held_keys)
                self.remote.press(self.held_keys)
                self.last_input = self.held_keys.copy()
            # Maintain FPS
            clock.tick(FPS)

        # Close
        pygame.font.quit()
        pygame.quit()
        return


if __name__ == "__main__":
    Window("-p" in sys.argv)
