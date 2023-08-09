import math
import time
import tkinter as tk
import random

from OttAgent.OttAgent import OttAgent
from OttMap.OttCmdMap import OttCmdMap
from OttMap.OttGuiMap import OttGuiMap
from OttObject import OttCircleObject, OttBaseObject, OttDiagonalLineObject


def sample_agent(object_list: list[OttBaseObject]):
    if object_list:
        return max(object_list).position
    else:
        return 0, 0


# Run the application
if __name__ == "__main__":
    object_time_appearance_list = {OttCircleObject("Main-object", (20, 20), 10, "red", meaning=1): 0,
                                   OttDiagonalLineObject("Distracting-object", (0, 0), (60, 60), "green", meaning = 0.5): 5,
    }
    agent = OttAgent(g=0.01, alpha=1.4, starting_position=(30, 30))
    app = OttCmdMap(length=60, width=60, object_time_appearance_list=object_time_appearance_list, task_length=300,
                    agent_callback=agent.step)

    app.mainloop()
