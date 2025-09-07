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
    
    # Movement
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

    def reset(self):
        self.controller.reset()
        return

    # Actions
    def release(self):
        self.controller.tap(buttons='A')
        sleep(0.2)
        self.tap_up()
        sleep(0.05)
        self.tap_up()
        self.controller.tap(buttons='A')
        sleep(0.9)
        self.tap_up()
        self.controller.tap(buttons='A')
        sleep(1.4)
        self.controller.tap(buttons='A')
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

if __name__ == "__main__":
    t = Trainer()
    
    # for i in range(5):
    #     t.tap_up()
    #     sleep(0.1)
    # for i in range(5):
    #     t.tap_left()
    #     sleep(0.1)
    # t.controller.tap(buttons='R')

    t.release_box()
    # t.tap_left()
    # t.tap_right()

    sleep(2)
    t.reset()
    t.controller.close_ser()