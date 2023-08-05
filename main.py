import math
import time
import tkinter as tk
import random

from OttAgent.OttAgent import OttAgent
from OttMap.OttGuiMap import OttGuiMap
from OttObject import OttCircleObject, OttBaseObject, OttDiagonalLineObject


def sample_agent(object_list: list[OttBaseObject]):
    if object_list:
        return max(object_list).position
    else:
        return 0, 0


# Run the application
if __name__ == "__main__":
    object_time_appearance_list = {OttCircleObject((20, 20), 10, "red", meaning=4): 0,
                                   OttDiagonalLineObject((0, 0), (60, 60), "green", meaning=2): 50,
                                   }
    agent = OttAgent(g=10 ** -0.5, alpha=1.4, starting_position=(30, 30))
    app = OttGuiMap(length=60, width=60, object_time_appearance_list=object_time_appearance_list, task_length=300,
                    agent_callback=agent.step)

    app.mainloop()
    # app.add_object(OttCircleObject((20, 20), 10, "red"))
    # app.update_map()
    # time.sleep(0.1)
    # app.update_map()
    # time.sleep(0.1)
    # app.update_map()
    # time.sleep(0.1)
    # app.update_map()
    # app.update_map()
    # app.update_map()
    # app.update_map()
    #
    # # for i in range(100):
    # #     app.update_map()
    # #     time.sleep(0.1)
    # app.mainloop()
