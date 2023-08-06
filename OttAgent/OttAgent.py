from typing import Dict, Any, List

import numpy as np

from OttMap import OttBaseMap
from OttObject import OttBaseObject
from ComDePy.numerical import Agent


class OttAgent(Agent):
    objects_representation: dict[OttBaseObject, Any]

    def __init__(self, g, alpha, starting_position, min_a=0.01, T1=1):

        self.g = g
        self.alpha = alpha
        self.min_a = min_a
        self.T1 = T1
        self.position: (int, int) = starting_position
        # self.cur_object: OttBaseObject = OttBaseObject(starting_position)
        self.rng = np.random.default_rng()
        self.a_list = {}
        self.b_list = {}
        self.s = OttBaseObject(starting_position, meaning=0.1)

        self._object_list: List[OttBaseObject] = []

    def step(self, cur_objects_list: List[OttBaseObject]):

        if not cur_objects_list:
            return 0, 0
        current_m = self.s.get_meaning()
        for obj in cur_objects_list:
            if obj not in self._object_list:
                self._object_list.append(obj)
                self.a_list[obj] = self.min_a  # self.rng.uniform(self.min_a)
                self.b_list[obj] = 1
        for obj in self._object_list:
            if obj not in cur_objects_list:
                self._object_list.remove(obj)
                del self.a_list[obj]
                del self.b_list[obj]
        current_a = np.array([self.a_list[obj] for obj in self._object_list])
        current_b = np.array([self.b_list[obj] for obj in self._object_list])
        current_s = np.array([obj.get_meaning() for obj in self._object_list])

        updated_a = current_a + self.g * ((current_m / current_b) * (current_a / np.sum(current_a)) - current_a)
        updated_a = np.maximum(updated_a, self.min_a)
        updated_b = current_b + (updated_a > self.alpha * self.T1) * updated_a * current_m
        # print(print(f"updated_a: {updated_a}"))
        # print(print(f"updated_alpha: {self.alpha * self.T1}"))
        # print(print(f"updated_b: {updated_b}"))

        # updated_b = current_b
        self.a_list = {obj: updated_a[i] for i, obj in enumerate(self._object_list)}
        self.b_list = {obj: updated_b[i] for i, obj in enumerate(self._object_list)}
        scores = current_s * updated_a
        if self.s != cur_objects_list[np.argmax(scores)]:
            if self.s in cur_objects_list:
                self.b_list[self.s] = 1
            self.s = cur_objects_list[np.argmax(scores)]
        return self.s.position

    def _sim(self):
        """
        Runs the sim. Fails if already ran.
        :return: self
        """

        for t in range(1, self.max_steps):
            self.a[t], self.b[t], self.s[t] = self._step(self.a[t - 1], self.b[t - 1], self.s[:t])

        self._segment_explore_exploit()

        return self
