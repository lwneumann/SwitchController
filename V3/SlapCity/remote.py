class Remote:
    def __init__(self):
        return
    
    def convert_inputs(self, inputs):
        movements = [x for x in inputs if x in {'w', 'a', 's', 'd'}]
        buttons = [x for x in inputs if x not in {'w', 'a', 's', 'd'}]
        return movements, buttons

    def get_movement(self, movements):
        x_move = {'a': 0, 'd': 255}
        y_move = {'w': 0, 's': 255}

        x = 128
        y = 128

        for m in movements:
            if m in x_move:
                x = x_move[m] if x == 128 else 128
            if m in y_move:
                y = y_move[m] if y == 128 else 128
        
        return "<", x, y

    def press(self, inputs):
        movements, buttons = self.convert_inputs(inputs)
        movements = self.get_movement(movements)

        print(movements)
        print(buttons)
        print()
        return
    
    def release(self, inputs):
        return
