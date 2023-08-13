import random
from typing import List

import numpy as np
from ComDePy.numerical import Agent

from OttMap.OttBaseMap import OttBaseMap
from OttObject import OttBaseObject


class OttAgent(Agent):
    """
    An agent that used CFG to track objects in the map.
    """

    def __init__(self, ott_map: OttBaseMap, g, alpha, starting_position, max_steps=100, min_a=0.01, T1=1):
        """
        Initialize the agent.
        @param ott_map: The map the agent is in.
        @param g: The g parameter.
        @param alpha: The alpha parameter.
        @param starting_position: The starting position of the agent.
        @param min_a: The minimum value of a.
        @param T1: The T1 parameter.
        """
        self.max_steps = max_steps
        self.ott_map = ott_map
        self.g = g
        self.alpha = alpha
        self.min_a = min_a
        self.T1 = T1
        self.position: (int, int) = starting_position

        self.rng = np.random.default_rng()
        self.a_list = {}
        self.b_list = {}
        self.s = None
        self._object_list: List[OttBaseObject] = []
        self.number_of_alternations = 0
        self.total_step_spent_on_target = 0

    def step(self, cur_objects_list: List[OttBaseObject]):
        """
        @param cur_objects_list: The list of objects in the agent's view.
        @return: The agent's next position based on the CFG.
        """
        if not cur_objects_list:
            direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            return self.position[0] + direction[0], self.position[1] + direction[1]

        for obj in cur_objects_list:
            if obj not in self._object_list:
                self._object_list.append(obj)
                self.a_list[obj] = self.rng.uniform(self.min_a)
                self.b_list[obj] = 0.1

        for obj in self._object_list:
            if obj not in cur_objects_list:
                self._object_list.remove(obj)
                del self.a_list[obj]
                del self.b_list[obj]

        current_m = np.array([self.s.get_meaning() if obj == self.s else obj.get_meaning() for obj in self._object_list])
        current_a = np.array([self.a_list[obj] for obj in self._object_list])
        current_b = np.array([self.b_list[obj] for obj in self._object_list])
        current_s = np.array([obj.get_meaning() for obj in self._object_list])
        print(f"Current m: {current_m}")
        print(f"Current a: {current_a}")
        print(f"Current b: {current_b}")
        print(f"Current s: {current_s}")
        print(f"Current s: {self.s}")
        print("-"*50)

        updated_a = current_a + self.g * ((current_m / current_b) * (current_a / np.sum(current_a)) - current_a)
        updated_a = np.maximum(updated_a, self.min_a)

        updated_b = current_b + (updated_a > self.alpha * self.T1) * updated_a * current_m

        self.a_list = {obj: updated_a[i] for i, obj in enumerate(self._object_list)}
        self.b_list = {obj: updated_b[i] for i, obj in enumerate(self._object_list)}
        scores = current_s * updated_a

        if self.s is None:
            self.s: OttBaseObject = self._object_list[np.argmax(scores)]

        elif self.s != self._object_list[np.argmax(scores)]:
            self.b_list[self.s] = 0.1
            self.number_of_alternations += 1
            self.s = self._object_list[np.argmax(scores)]
        if self.s.is_target:
            self.total_step_spent_on_target += 1
        return self.s.position

    def _sim(self):
        """
        Runs the sim. Fails if already ran.
        :return: None
        """
        for t in range(self.max_steps):
            self.ott_map.update_map()
            next_agent_position = self.step(self.ott_map.ott_objects)
            self.ott_map.set_agent_position(next_agent_position)
            self.agent_position = next_agent_position
            self.ott_map.draw_map()
            # input("Press Enter to continue...")
        self.ott_map.reset()


