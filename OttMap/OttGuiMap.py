import threading
import time
import tkinter as tk
import random
from typing import Callable, Tuple

from OttMap.OttBaseMap import OttBaseMap
from OttObject import OttBaseObject

WIDTH = 1
OUT_LINE_COLOR = "black"


class OttGuiMap(tk.Tk, OttBaseMap):
    def __init__(self, length, width, object_time_appearance_list: dict[OttBaseObject, int] = None,
                 task_length=100,
                 agent_callback: Callable[[list[OttBaseObject]], Tuple[int, int]] = None,
                 padding=10):

        tk.Tk.__init__(self)
        OttBaseMap.__init__(self, length, width, task_length, object_time_appearance_list, agent_callback)
        self.agent_callback = agent_callback

        self.padding = padding
        self.title("Object Tracking Task App")
        self.attributes("-fullscreen", True)  # Make the window fullscreen

        # Calculate canvas size based on the screen dimensions and the size of the matrix
        screen_width = self.winfo_screenwidth() - 2 * padding
        screen_height = self.winfo_screenheight() - 2 * padding - 100

        canvas_edge_length = min(screen_width, screen_height)
        self.square_size = min((canvas_edge_length - 2 * padding) // width,
                               (canvas_edge_length - 2 * padding) // length)

        self.geometry(f"{canvas_edge_length}x{canvas_edge_length}")

        # Create a canvas to draw the squares
        self.canvas = tk.Canvas(self, width=canvas_edge_length, height=canvas_edge_length, bg="white")
        self.canvas.pack(pady=10)

        # Create GUI elements
        self.start_button = tk.Button(self, text="Start Tracking", command=self._start_tracking)
        self.start_button.pack(pady=10)
        self.tracked_objects: list[OttBaseObject] = []

        self.draw_map()

    def draw_map(self):
        # Clear the canvas
        self.canvas.delete("all")
        # Draw the squares based on the matrix
        for i in range(self.width):
            for j in range(self.length):
                x1, y1 = i * self.square_size, j * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                self.canvas.create_rectangle(x1 + self.padding, y1 + self.padding, x2 + self.padding, y2 + self.padding,
                                             fill="white",
                                             outline=OUT_LINE_COLOR,
                                             width=WIDTH)

        for obj in self.ott_objects:
            x1, y1 = obj.position[0] * self.square_size, obj.position[1] * self.square_size
            x2, y2 = x1 + self.square_size, y1 + self.square_size
            self.canvas.create_rectangle(x1 + self.padding, y1 + self.padding, x2 + self.padding, y2 + self.padding,
                                         fill=obj.get_color(),
                                         outline=OUT_LINE_COLOR,
                                         width=WIDTH)

    def _start_tracking(self):
        for i in range(self.task_length):
            self.update()
            self.draw_map()
            if self.agent_callback is not None:
                position = self.agent_callback(self.ott_objects)
                x1, y1 = position[0] * self.square_size, position[1] * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                self.canvas.create_rectangle(x1 + self.padding, y1 + self.padding, x2 + self.padding, y2 + self.padding,
                                             outline="purple",
                                             width=WIDTH * 4)
            self.update_idletasks()
            self.update_map()
            if self.object_time_appearance_list is not None:
                for obj, time_appearance in self.object_time_appearance_list.items():
                    if i == time_appearance:
                        self.add_object(obj)

