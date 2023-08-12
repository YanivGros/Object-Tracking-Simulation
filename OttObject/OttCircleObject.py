# Create a specific implementation of TrackedObjectBase for a specific type of tracked object
import math
from functools import *

from OttObject.OttBaseObject import OttBaseObject


class OttCircleObject(OttBaseObject):
    """
    A class that represents a circle object.
    """

    def __init__(self, radius, **kwargs):
        """
        Initialize the OttCircleObject.
        The circle will be centered at (position[0], position[1] - radius). The circle will be drawn clockwise.
        @param radius: Radius of the circle.
        @keyword name: Name of the object.
        @keyword position: Position of the object.
        @keyword color: Color of the object.
        @keyword steps_to_live: Number of steps the object will live for.
        @keyword meaning: Meaning of the object.
        """
        super().__init__(**kwargs)
        self.radius = radius
        self.center = self.position[0], self.position[1] - radius
        steps_for_full_circle = math.ceil(radius * math.pi * 2)
        self.step_size = 1 / steps_for_full_circle

    @wraps(OttBaseObject.update_location)
    def update_location(self):
        super().update_location()
        next_x = self.center[0] + self.radius * math.cos(self.step_size * self.cur_step * 2 * math.pi)
        next_y = self.center[1] - self.radius * math.sin(self.step_size * self.cur_step * 2 * math.pi)
        self.position = (math.ceil(next_y), math.ceil(next_x))

    @wraps(OttBaseObject.is_alive)
    def is_alive(self):
        return self.cur_step < self.steps_to_live or self.steps_to_live == 0
