from time import sleep
import remote


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
    def up(self):
        self.controller.move(UP)
        return
    
    def left(self):
        self.controller.move(LEFT)
        return

    def right(self):
        self.controller.move(RIGHT)
        return

    def down(self):
        self.controller.move(DOWN)
        return

    def stop(self):
        self.controller.move(NEUTRAL)
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
        for r in range(5):
            self.release_row(r%2==0, r==4)
        return

    # Hatching
    def reposition(self):
        # Resets location at bridge daycare
        self.tap('X')
        sleep(.5)
        self.tap('A')
        sleep(2.2)
        self.up()
        sleep(0.065)
        self.reset()
        sleep(0.5)
        self.tap('A')
        sleep(0.6)
        self.tap('A')
        sleep(4)
        return

    def bike_circle(self, circles=20):
        for c in range(circles):
            for d in 'qwedcxza':
                self.move(self.controller.get_movement(d))
                sleep(0.1)
        self.reset()
        return

if __name__ == "__main__":
    t = Trainer()

    # t.tap('B')
    # sleep(1)
    # t.tap('B')
    # sleep(1)
    # t.tap('B')
    # sleep(1)
    t.reposition()
    t.reposition()
    t.reposition()
    # t.bike_circle(circles=20)

    sleep(2)
    t.reset()
    t.controller.close_ser()