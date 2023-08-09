from abc import ABC
from typing import Callable, Tuple

from OttObject import OttBaseObject


class OttBaseMap(ABC):
    """Base class for all map classes."""

    def __init__(self, length, width, task_length=100,
                 object_time_appearance_list: dict[OttBaseObject, int] = (),
                 agent_callback: Callable[[list[OttBaseObject]], Tuple[int, int]] = lambda x: (0, 0)):

        self.length = length
        self.width = width
        self.task_length = task_length
        self.agent_callback = agent_callback
        self.object_time_appearance_list = object_time_appearance_list
        self.agent_position = agent_callback([])
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
        for obj in self.ott_objects:
            obj.update_location()
            if not obj.is_alive():
                object_to_delete.append(obj)
            else:
                assert obj.position[0] < self.width and obj.position[1] < self.length
                assert obj.position[0] >= 0 and obj.position[1] >= 0
        for obj in object_to_delete:
            self.remove_object(obj)
        self.agent_position = self.agent_callback(self.ott_objects)