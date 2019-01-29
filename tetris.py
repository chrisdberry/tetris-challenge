#!/usr/bin/env python

from random import randint
import sys
from copy import deepcopy

class Tetris(object):
    _shapes = [
        [[1,1,1,1],],
        [[1,0], [1,0], [1, 1]],
        [[0,1], [0,1], [1, 1]],
        [[0,1], [1,1], [1, 0]],
        [[1,1], [1,1]],
    ]

    def __init__(self):
        self.height = 8
        self.width = 20
        self.init_board()
        self.add_shape()

    def init_board(self):
        #board is a list of ints which are binary mask for
        #empty/ non empy cells
        self.board = []
        for i in range(self.height):
            self.board.append(0)

    def play(self):
        while True:
            self.render_board()
            while True:
                if not self.valid_move_possible():
                    self.fix_shape()
                    self.add_shape()
                    break
                move = input(
                    "Make your move [w (counter), a (left), "
                    "s (clockwise), d (right), q (quit)]:")
                if move == "f":
                    print("Fix")
                    self.fix_shape()
                    self.add_shape()
                    break
                if move == "q":
                    sys.exit("Bye!")
                if move == "s":
                    result = self.rotate_shape(1)
                    if not result:
                        print("Invalid rotate! Try again")
                        continue
                    break
                if move == "w":
                    result = self.rotate_shape(-1)
                    if not result:
                        print("Invalid rotate! Try again")
                        continue
                    break
                if move == "a":
                    result = self.move_shape(-1)
                    if not result:
                        print("Invalid move! Try again")
                        continue
                    break
                if move == "d":
                    result = self.move_shape(1)
                    if not result:
                        print("Invalid move! Try again")
                        continue
                    break

    def row_cells(self, row):
        return ("{0:0" + str(self.width) + "b}").format(row)[::-1]

    def get_x_offset(self, cell_x):
        return self.row_cells(cell_x).index("1")

    def render_board(self):
        self.fix_shape() #add shape to board to render it
        #render board
        for row in reversed(self.board):
                print(("*" + self.row_cells(row
                        ).replace("0", " ").replace("1", "*") +
                    "*"))
        print("*" + "*" * self.width + "*")
        self.unfix_shape() #remove shape from board

    def collision(self, shape):
        #within border
        if ((shape["height"] - len(shape["body"]) + 1) < 0
            or min(shape["body"]) <= 1
            or max(shape["body"]) > (1 << self.width)):
            return True
        #board contents collision
        for i, cell_x in enumerate(shape["body"]):
            if (self.board[shape["height"] - i] & cell_x):
                return True
        return False

    def valid_move_possible(self):
        return any([self.rotate_shape(1,0), self.rotate_shape(-1,0),
                self.move_shape(-1,0), self.move_shape(1,0)])

    def add_shape(self):
        self.shape = {"height": self.height-1,
            "matrix": self._shapes[randint(0,4)],}
        x_offset = randint(1,self.width-4)
        self.shape["body"] = self.get_body_shape(
            self.shape["matrix"], x_offset)
        if not self.valid_move_possible() or self.collision(self.shape):
            sys.exit("Gameover!")

    def get_body_shape(self, shape_matrix, x_offset):
        shape_body = []
        for shape_row in shape_matrix:
            cell_x = 0
            for j, cell in enumerate(shape_row):
                cell_x += cell << (x_offset+j)
            shape_body.append(cell_x)
        return shape_body

    def fix_shape(self):
        for i, cell_x in enumerate(self.shape["body"]):
            self.board[self.shape["height"] - i] += cell_x

    def unfix_shape(self):
        for i, cell_x in enumerate(self.shape["body"]):
            self.board[self.shape["height"] - i] -= cell_x

    def rotate_shape(self, direction=1, commit=1):
        _shape = deepcopy(self.shape)
        _shape["height"] -= 1
        if direction > 0: #clockwise
            _shape["matrix"] = list(zip(*_shape["matrix"][::-1]))
        else: #anticlockwise
            _shape["matrix"] = list(zip(*_shape["matrix"]))[::-1]
        x_offset = self.get_x_offset(min(_shape["body"]))
        _shape["body"] = self.get_body_shape(
            _shape["matrix"], x_offset)
        if not self.collision(_shape):
            if commit:
              self.shape = _shape
            return True
        else:
            return False

    def move_shape(self, direction=1, commit=1):
        _shape = deepcopy(self.shape)
        _shape["height"] -= 1
        if direction > 0:
            _shape["body"] = [_ << 1 for _ in _shape["body"]]
        else:
            _shape["body"] = [_ >> 1 for _ in _shape["body"]]
        if not self.collision(_shape):
            if commit:
              self.shape = _shape
            return True
        else:
            return False


if __name__ == "__main__":
    tetris = Tetris()
    tetris.play()
