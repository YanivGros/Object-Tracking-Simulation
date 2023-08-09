import time
from typing import Callable, Tuple

from OttMap.OttBaseMap import OttBaseMap
from OttObject import OttBaseObject

PROMPT = "-" * 50


class OttCmdMap(OttBaseMap):
    """ Display the map to the command line"""

    def __init__(self, length, width, task_length=100,
                 object_time_appearance_list: dict[OttBaseObject, int] = None,
                 agent_callback: Callable[[list[OttBaseObject]], Tuple[int, int]] = None):
        super().__init__(length, width, task_length, object_time_appearance_list, agent_callback)
        self.cur_step = 0
        self.mainloop()

    def draw_map(self):
        """Draw the map to the command line"""
        #     print object location
        print(PROMPT)
        print("Map at time step: ", self.cur_step)
        for obj in self.ott_objects:
            print(obj)
        print("Agent looking at: ", self.agent_position)
        # print(PROMPT)

    def mainloop(self):
        """Run the map"""
        for i in range(self.task_length):
            self.cur_step = i
            self.update_map()
            self.draw_map()
            for obj, time_appearance in self.object_time_appearance_list.items():
                if i == time_appearance:
                    self.add_object(obj)
            time.sleep(0.5)
            # input("Press Enter to continue...")
