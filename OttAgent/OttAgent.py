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

    def __init__(self, ott_map: OttBaseMap, g, alpha, starting_position, min_a=0.01, T1=1):
        """
        Initialize the agent.
        @param ott_map: The map the agent is in.
        @param g: The g parameter.
        @param alpha: The alpha parameter.
        @param starting_position: The starting position of the agent.
        @param min_a: The minimum value of a.
        @param T1: The T1 parameter.
        """
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

    def step(self, cur_objects_list: List[OttBaseObject]):
        """
        @param cur_objects_list: The list of objects in the agent's view.
        @return: The agent's next position based on the CFG.
        """
        if not cur_objects_list:
            direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            return self.position[0] + direction[0], self.position[1] + direction[1]

            # current_m = self.s.get_meaning()
        for obj in cur_objects_list:
            if obj not in self._object_list:
                self._object_list.append(obj)
                self.a_list[obj] = self.rng.uniform(self.min_a)  # self.rng.uniform(self.min_a)
                self.b_list[obj] = 0.1
        for obj in self._object_list:
            if obj not in cur_objects_list:
                self._object_list.remove(obj)
                del self.a_list[obj]
                del self.b_list[obj]
        current_m = np.zeros(len(self._object_list))
        current_a = np.zeros(len(self._object_list))
        current_b = np.zeros(len(self._object_list))
        current_s = np.zeros(len(self._object_list))
        for i, obj in enumerate(self._object_list):
            if obj == self.s:
                current_m[i] = self.s.get_meaning()
            else:
                current_m[i] = obj.get_meaning()
            current_a[i] = self.a_list[obj]
            current_b[i] = self.b_list[obj]
            current_s[i] = obj.get_meaning()

        updated_a = current_a + self.g * ((current_m / current_b) * (current_a / np.sum(current_a)) - current_a)
        updated_a = np.maximum(updated_a, self.min_a)
        updated_b = current_b + (updated_a > self.alpha * self.T1) * updated_a * current_m
        # updated_b = current_b + (updated_a > self.alpha * self.T1) * (updated_a - self.alpha) * current_m
        print(f"updated_a: {updated_a}")
        print(f"updated_b: {updated_b}")
        # print(print(f"updated_a: {updated_a}"))
        # print(print(f"updated_alpha: {self.alpha * self.T1}"))
        # print(print(f"updated_b: {updated_b}"))

        # updated_b = current_b
        self.a_list = {obj: updated_a[i] for i, obj in enumerate(self._object_list)}
        self.b_list = {obj: updated_b[i] for i, obj in enumerate(self._object_list)}
        scores = current_s * updated_a
        print(f"scores: {scores} len: {len(scores)}")

        if self.s != self._object_list[np.argmax(scores)]:
            if self.s in cur_objects_list:
                self.b_list[self.s] = 0.1
            self.s = self._object_list[np.argmax(scores)]
        print(f"self.s: {self.s.color}")
        return self.s.position

    def _sim(self):
        """
        Runs the sim. Fails if already ran.
        :return: None
        """
        max_step = 100
        for t in range(max_step):
            self.ott_map.update_map()
            next_agent_position = self.step(self.ott_map.ott_objects)
            self.ott_map.set_agent_position(next_agent_position)
            self.agent_position = next_agent_position
            self.ott_map.draw_map()
