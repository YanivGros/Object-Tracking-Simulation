from abc import ABC
from typing import Callable, Tuple

from OttObject import OttBaseObject


class OttBaseMap(ABC):
    """Base class for all map classes."""

    def __init__(self, length, width, task_length=100,
                 object_time_appearance_list: dict[OttBaseObject, int] = None,
                 agent_callback: Callable[[list[OttBaseObject]], Tuple[int, int]] = None):
        self.length = length
        self.width = width
        self.task_length = task_length
        self.agent_callback = agent_callback
        self.object_time_appearance_list = object_time_appearance_list
        self.ott_objects = []

    def add_object(self, obj: OttBaseObject):
        """Add an object to the map."""
        self.ott_objects.append(obj)

    def remove_object(self, obj: OttBaseObject):
        """Remove an object from the map."""
        self.ott_objects.remove(obj)

    def get_objects(self):
        return self.ott_objects

    def update_map(self):
        """Update the map."""
        object_to_delete = []
        trail_objects = []
        for obj in self.ott_objects:
            if obj.should_leave_trail:
                trail_objects.append(
                    OttBaseObject(obj.position, color="gray", steps_to_live=5, should_leave_trail=False, meaning=0))

                obj.update_location()
                if obj.position == trail_objects[-1].position:
                    trail_objects.pop()
            else:
                obj.update_location()

            if not obj.is_alive():
                object_to_delete.append(obj)
            else:
                assert obj.position[0] < self.width and obj.position[1] < self.length
                assert obj.position[0] >= 0 and obj.position[1] >= 0

        for obj in trail_objects:
            self.add_object(obj)
        for obj in object_to_delete:
            self.remove_object(obj)
        return object_to_delete

    def print(self):
        """Print the map."""
        pass
