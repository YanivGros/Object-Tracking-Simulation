from functools import wraps

from OttMap.OttBaseMap import OttBaseMap

PROMPT = "-" * 50


class OttCmdMap(OttBaseMap):
    """
    Display the map and its updates in the command line interface.
    """

    @wraps(OttBaseMap.__init__)
    def __init__(self, should_print=False, **kwargs):
        super().__init__(**kwargs)
        self.should_print = should_print

    @wraps(OttBaseMap.add_object)
    def draw_map(self):
        if self.should_print:
            print(PROMPT)
            print("Map at time step: ", self.cur_step)
            for obj in self.ott_objects:
                print(obj)
            print("Agent looking at: ", self.agent_position)
