from functools import wraps

from OttObject.OttBaseObject import OttBaseObject


class OttDiagonalLineObject(OttBaseObject):
    """
    A class that represents a diagonal line object.
    """
    def __init__(self, end, **kwargs):
        """
        Initialize the OttDiagonalLineObject.
        @param end: The end point of the line.
        @keyword name: Name of the object.
        @keyword position: Position of the object.
        @keyword color: Color of the object.
        @keyword steps_to_live: Number of steps the object will live for.
        @keyword meaning: Meaning of the object.
        """
        super().__init__(**kwargs)
        assert abs(self.position[0] - end[0]) == abs(self.position[1] - end[1]), "The line must be diagonal"
        self.cur_step = 0
        self.end = end
        self.x_step = 1 if end[0] > self.position[0] else -1
        self.y_step = 1 if end[1] > self.position[1] else -1

    @wraps(OttBaseObject.update_location)
    def update_location(self):
        super().update_location()
        if self.position != self.end:
            self.position = (self.position[0] + self.x_step, self.position[1] + self.y_step)

    @wraps(OttBaseObject.is_alive)
    def is_alive(self):
        return (self.cur_step < self.steps_to_live or self.steps_to_live == 0) and self.position != self.end
