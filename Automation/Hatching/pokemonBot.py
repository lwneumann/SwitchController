"""
Sword and Shield
"""
from time import sleep
from alive_progress import alive_bar
import remote, shinyChecker

# Some directions
LEFT = (0, 128)
RIGHT = (255, 128)
UP = (128, 0)
DOWN = (128, 255)
NEUTRAL = (128, 128)


class Trainer:
    def __init__(self):
        self.controller = remote.Remote()
        self.delay = 0.05
        return
    
    # ==================
    # ==== Movement ====
    # ==================
    def up(self, delay=None):
        self.controller.move(UP)
        if delay is not None:
            sleep(delay)
            self.reset()
        return
    
    def left(self, delay=None):
        self.controller.move(LEFT)
        if delay is not None:
            sleep(delay)
            self.reset()
        return

    def right(self, delay=None):
        self.controller.move(RIGHT)
        if delay is not None:
            sleep(delay)
            self.reset()
        return

    def down(self, delay=None):
        self.controller.move(DOWN)
        if delay is not None:
            sleep(delay)
            self.reset()
        return

    def stop(self, delay=None):
        self.controller.move(NEUTRAL)
        if delay is not None:
            sleep(delay)
            self.reset()
        return

    def tap_up(self):
        self.up()
        sleep(self.delay)
        self.reset()
        return

    def tap_down(self):
        self.down()
        sleep(self.delay)
        self.reset()
        return

    def tap_left(self):
        self.left()
        sleep(self.delay)
        self.reset()
        return

    def tap_right(self):
        self.right()
        sleep(self.delay)
        self.reset()
        return

    def tap(self, inputs, delay=0.1):
        self.controller.tap(buttons=inputs, delay=delay)
        return
    
    def move(self, *args):
        if len(args) == 1 and isinstance(args[0], (tuple, list)) and len(args[0]) == 2:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        else:
            raise ValueError("move() requires either (x, y) or ((x, y))")
        self.controller.move(x, y)
        return

    def reset(self):
        self.controller.reset()
        return

    # =================
    # ==== Actions ====
    # =================
    def reload_game(self):
        print('> Rebooting')
        self.tap('H')
        sleep(0.5)
        self.tap('X')
        sleep(0.5)
        self.tap('A')
        sleep(3)
        self.tap('A')
        sleep(19)
        self.tap('A')
        sleep(10)
        self.tap('X')
        sleep(0.5)
        self.tap_down()
        sleep(0.3)
        self.tap('B')
        sleep(2)
        return
    
    # Box Managing
    def release(self):
        self.tap('A')
        sleep(0.2)
        self.tap_up()
        sleep(0.05)
        self.tap_up()
        self.tap('A')
        sleep(0.9)
        self.tap_up()
        self.tap('A')
        sleep(1.4)
        self.tap('A')
        return

    def release_row(self, move_right=True, last=False):
        for c in range(6):
            self.release()
            sleep(0.2)
            if c < 5:
                if move_right:
                    self.tap_right()
                else:
                    self.tap_left()
            else:
                if not last:
                    self.tap_down()
            sleep(0.2)
        return

    def release_box(self):
        with alive_bar(5) as bar:
            for r in range(5):
                self.release_row(r%2==0, r==4)
                bar()
        return

    # Hatching
    def reposition(self):
        # Resets location at bridge daycare
        self.tap('X')
        sleep(.5)
        self.tap('A')
        sleep(2.2)
        self.move(255, 0)
        sleep(0.035)
        self.reset()
        sleep(0.7)
        self.tap('A')
        sleep(0.7)
        self.tap('A')
        sleep(2.5)
        return

    def bike_circle(self, circles=20):
        with alive_bar(circles) as bar:
            for c in range(circles):
                for d in 'cxzaqwed':
                    self.move(self.controller.get_movement(d))
                    sleep(0.15)
                bar()
        self.reset()
        return

    def get_egg(self):
        """On Bike"""
        self.reposition()
        # Talk to lady
        self.move(0, 10)
        sleep(0.15)
        self.up(0.2)
        self.reset()
        sleep(0.2)
        # Get egg
        self.tap('A')
        sleep(0.9)
        self.tap('A')
        sleep(0.8)
        self.tap('A')
        sleep(3.5)
        self.tap('A')
        sleep(1.5)
        self.tap('A')
        sleep(0.5)
        self.tap('A')
        sleep(2)
        self.tap('A')
        sleep(1)
        self.tap('A')
        sleep(1)
        self.tap('A')
        sleep(1)
        self.tap('A')
        sleep(2)
        self.tap('A')
        sleep(1)
        self.tap('A')
        sleep(1)
        self.tap('A')
        sleep(1)
        self.tap('B')
        sleep(0.4)
        self.tap('B')
        sleep(0.4)
        self.tap('B')
        return

    def handle_hatching(self):
        self.tap('A')
        sleep(15)
        self.tap('A')
        sleep(4)
        return

    def hatch_egg(self):
        # Get
        sleep(0.3)
        print('> Getting Egg')
        self.get_egg()
        sleep(0.3)
        
        print('> Hatching')
        self.bike_circle(70)

        self.handle_hatching()

        # Saftey Circles to spawn eggs :(
        self.bike_circle(20)
        return

    def shiny_check_box(self):
        print('> Releasing box and shiny checking')
        sleep(0.6)
        shiny_pos = []
        with alive_bar(30) as bar:
            for r in range(5):
                for c in range(6):
                    shiny, present = shinyChecker.check_shiny()
                    if not shiny and present:
                        self.release()
                        sleep(0.2)
                    else:
                        if shiny:
                            shiny_pos.append([r, c if r%2==0 else 5-c])
                    if c == 5 and r < 4:
                        self.tap_down()
                    else:
                        if c != 5 or r < 4:
                            self.tap_right() if r%2==0 else self.tap_left()
                    bar()
        return shiny_pos

    def batch_eggs(self, num_eggs=30):
        for egg in range(num_eggs):
            print()
            print(f"({egg+1: >{len(str(num_eggs))}}/{num_eggs})")
            self.hatch_egg()

            # Go to box
            # shinies = self.shiny_check_box()
        return
    

if __name__ == "__main__":
    t = Trainer()

    # t.tap('H')
    # sleep(0.5)
    # t.tap('H')
    # sleep(0.5)
    # t.tap('H')
    # sleep(0.5)

    t.reload_game()

    t.tap('X')
    sleep(1)
    t.tap_up()
    sleep(1)
    t.tap('A')
    sleep(3)
    t.tap('R')
    sleep(2.5)
    print(t.shiny_check_box())

    # t.batch_eggs()


    t.reset()
    t.controller.close_ser()
