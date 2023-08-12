class OttBaseObject:
    id = 0
    """
    Base class for all trackable objects.
    """

    def __init__(self, name, position: (int, int), color: str = "white", steps_to_live=0, meaning=0, is_target=False):
        """
        Initialize the OttBaseObject.
        @param name: Name of the object.
        @param position: Position of the object.
        @param color: Color of the object.
        @param steps_to_live: Number of steps the object will live for.
        @param meaning: Meaning of the object.
        """
        self.name = name
        self.object_id = OttBaseObject.id
        self.is_target = is_target
        self.steps_to_live = steps_to_live
        self.position = position
        self._init_position = position
        self.meaning = meaning
        self.color = color
        self.cur_step = 0
        OttBaseObject.id += 1

    def get_location(self):
        return self.position

    def get_color(self):
        return self.color

    def update_location(self):
        """
        Update the location of the object.
        @return: None
        """
        self.cur_step += 1

    def is_alive(self):
        """
        Check if the object is still alive.
        @return: True if the object is still alive, False otherwise.
        """
        return self.cur_step < self.steps_to_live or self.steps_to_live == 0

    def get_meaning(self):
        return self.meaning

    def __str__(self):
        return f"Object {self.name} at {self.position}"

    def __eq__(self, other):
        if not isinstance(other, OttBaseObject):
            return False
        return self.object_id == other.object_id

    def __hash__(self):
        return hash(self.object_id)

    def reset(self):
        self.cur_step = 0
        self.position = self._init_position
