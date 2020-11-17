# -*- coding: utf-8 -*-

class Car:
    def __init__(self, x, y, velocity, turn_rate, angle):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.velocity = velocity
        self.turn_rate = turn_rate
        self.angle = angle

    def go_forward(self):
        self.old_x = self.x
        self.x += self.velocity

    def turn_right(self):
        pass

    def turn_left(self):
        pass
