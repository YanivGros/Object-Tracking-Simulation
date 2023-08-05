from typing import Tuple


class OttBaseObject:
    position: Tuple[int, int]
    id = 0

    def __init__(self, position: (int, int), color: str = "white", steps_to_live=0, meaning=0, should_leave_trail=True):
        self.should_leave_trail = should_leave_trail
        self.object_id = OttBaseObject.id
        OttBaseObject.id += 1
        self.steps_to_live = steps_to_live
        self.position = position
        self.meaning = meaning
        self.color = color
        self.cur_step = 0

    def get_location(self):
        return self.position

    def get_color(self):
        return self.color

    def update_location(self):
        self.cur_step += 1

    def is_alive(self):
        return self.cur_step < self.steps_to_live or self.steps_to_live == 0

    def get_meaning(self):
        return self.meaning

    def __gt__(self, other):
        return self.meaning > other.meaning


