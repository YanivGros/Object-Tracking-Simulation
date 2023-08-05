from OttObject.OttBaseObject import OttBaseObject


class OttDiagonalLineObject(OttBaseObject):
    def __init__(self, position, end, color="green", steps_to_live=100, meaning=0):
        super().__init__(position, color, steps_to_live, meaning)
        assert abs(position[0] - end[0]) == abs(position[1] - end[1]), "The line must be diagonal"
        self.cur_step = 0
        self.end = end
        self.x_step = 1 if end[0] > position[0] else -1
        self.y_step = 1 if end[1] > position[1] else -1

    def update_location(self):
        super().update_location()
        if self.position != self.end:
            self.position = (self.position[0] + self.x_step, self.position[1] + self.y_step)

    def is_alive(self):
        return (self.cur_step < self.steps_to_live or self.steps_to_live == 0) and self.position != self.end
