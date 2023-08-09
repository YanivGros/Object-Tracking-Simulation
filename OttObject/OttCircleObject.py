# Create a specific implementation of TrackedObjectBase for a specific type of tracked object
import math

from OttObject.OttBaseObject import OttBaseObject


class OttCircleObject(OttBaseObject):
    def __init__(self, name, position, radius, color="red", steps_to_live=0, meaning=0):
        super().__init__(name, position, color, steps_to_live, meaning)
        self.radius = radius
        self.center = position[0] - radius, position[1]
        steps_for_full_circle = math.ceil(radius * math.pi * 2)
        self.step_size = 1 / steps_for_full_circle

    def update_location(self):
        super().update_location()
        next_x = self.center[0] + self.radius * math.cos(self.step_size * self.cur_step * 2 * math.pi)
        next_y = self.center[1] + self.radius * math.sin(self.step_size * self.cur_step * 2 * math.pi)
        self.position = (math.ceil(next_x), math.ceil(next_y))

    def is_alive(self):
        return self.cur_step < self.steps_to_live or self.steps_to_live == 0
