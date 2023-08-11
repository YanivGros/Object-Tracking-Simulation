import time
from abc import ABC, abstractmethod
from typing import Tuple

from OttObject import OttBaseObject


class OttBaseMap(ABC):
    """
    The base class for OttMap.
    """

    def __init__(self, length, width, task_length=100, delay=0,
                 object_time_appearance_list: dict[OttBaseObject, int] = ()):
        """
        Initialize the Map.
        @param length: The length of the map.
        @param width: The width of the map.
        @param task_length: The length of the task.
        @param delay: The delay between each step.
        @param object_time_appearance_list: Dictionary mapping OttBaseObjects to their appearance times at the map.
        """
        self.length = length
        self.width = width
        self.task_length = task_length
        self.delay = delay
        self.object_time_appearance_list = object_time_appearance_list
        self.agent_position = (0, 0)
        self.ott_objects = []
        self.cur_step = 0

    def add_object(self, obj: OttBaseObject):
        """
        Add an object to the map.
        @param obj: The object to add.
        @return: None
        """
        self.ott_objects.append(obj)

    def remove_object(self, obj: OttBaseObject):
        """
        Remove an object from the map.
        @param obj: The object to remove.
        @return: None
        """
        self.ott_objects.remove(obj)

    def get_objects(self):
        """
        Get the list of OttBaseObjects on the map.
        @return: The list of OttBaseObjects on the map.
        """
        return self.ott_objects

    def set_agent_position(self, position: Tuple[int, int]):
        """
        Set the agent's position.
        @param position: The agent's position.
        @return: None
        """
        self.agent_position = position

    def update_map(self):
        """
        Update the map.
        @return: None
        """
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

        for obj, time_appearance in self.object_time_appearance_list.items():
            if self.cur_step == time_appearance:
                self.add_object(obj)
        self.cur_step += 1
        if self.delay:
            time.sleep(self.delay)

    @abstractmethod
    def draw_map(self):
        """
        Draw the map.
        @return: None
        """
        pass
