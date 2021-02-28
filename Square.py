class Square:

    def __init__(self, x, y, number, modify):
        self.pos_x = x
        self.pos_y = y
        self.value = number
        self.is_modifiable = modify

    # updates value of square
    def update_number(self, number):
        if self.is_modifiable:
            self.value = number

    # verify if square is empty
    def is_empty(self):
        if self.value == 0:
            return True
        else:
            return False

    def update_modifiable(self, option):
        if option is True:
            self.is_modifiable = True
        else:
            self.is_modifiable = False
