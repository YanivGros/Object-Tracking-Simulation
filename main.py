from OttAgent import *
from OttMap import *
from OttObject import *

LENGTH = 60
WIDTH = 60
TASK_LENGTH = 300

if __name__ == "__main__":
    object_time_appearance_list = {
        OttCircleObject(
            name="Main-object",
            position=(LENGTH / 2 + 10, WIDTH / 2),
            radius=10,
            color="red",
            meaning=1,
        ): 0,
        OttDiagonalLineObject(
            name="Distracting-object",
            position=(0, 0),
            end=(LENGTH, WIDTH),
            color="green",
            meaning=0.5,
        ): 50,
    }

    ott_map = OttGuiMap(
        length=60,
        width=60,
        object_time_appearance_list=object_time_appearance_list,
        task_length=300,
    )
    agent = OttAgent(ott_map=ott_map, g=0.5, alpha=1.4, starting_position=(30, 30))

    agent.sim()
    print("Done!")
