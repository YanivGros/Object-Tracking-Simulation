import tkinter as tk
from functools import wraps

from OttMap.OttBaseMap import OttBaseMap
from OttObject import OttBaseObject

WIDTH = 1
OUT_LINE_COLOR = "black"


class OttGuiMap(tk.Tk, OttBaseMap):
    """
    Display the map and its updates in a GUI.
    """

    @wraps(OttBaseMap.__init__)
    def __init__(self, padding=10, color="white", **kwargs):
        tk.Tk.__init__(self)
        OttBaseMap.__init__(self, **kwargs)

        self.color = color
        self.padding = padding
        self.title("Object Tracking Task App")
        self.attributes("-fullscreen", True)

        screen_width = self.winfo_screenwidth() - 2 * padding
        screen_height = self.winfo_screenheight() - 2 * padding

        canvas_edge_length = min(screen_width, screen_height)
        self.square_size = min(
            (canvas_edge_length - 2 * padding) // self.width, (canvas_edge_length - 2 * padding) // self.length
        )

        self.geometry(f"{canvas_edge_length}x{canvas_edge_length}")

        self.canvas = tk.Canvas(
            self,
            width=self.square_size * self.width + padding * 2,
            height=self.square_size * self.length + padding * 2,
            bg="white",
        )
        self.canvas.pack(pady=10)

        self.tracked_objects: list[OttBaseObject] = []

    def get_color(self):
        return self.color

    @wraps(OttBaseMap.add_object)
    def draw_map(self):
        self.canvas.delete("all")
        for i in range(self.width):
            for j in range(self.length):
                x1, y1 = i * self.square_size, j * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                self.canvas.create_rectangle(
                    x1 + self.padding,
                    y1 + self.padding,
                    x2 + self.padding,
                    y2 + self.padding,
                    fill="white",
                    outline=OUT_LINE_COLOR,
                    width=WIDTH,
                )

        for obj in self.ott_objects:
            x1, y1 = obj.position[0] * self.square_size, obj.position[1] * self.square_size
            x2, y2 = x1 + self.square_size, y1 + self.square_size
            self.canvas.create_rectangle(
                x1 + self.padding,
                y1 + self.padding,
                x2 + self.padding,
                y2 + self.padding,
                fill=obj.get_color(),
                outline=OUT_LINE_COLOR,
                width=WIDTH,
            )

        x1, y1 = self.agent_position[0] * self.square_size, self.agent_position[1] * self.square_size
        x2, y2 = x1 + self.square_size, y1 + self.square_size
        self.canvas.create_rectangle(
            x1 + self.padding,
            y1 + self.padding,
            x2 + self.padding,
            y2 + self.padding,
            outline=OUT_LINE_COLOR,
            width=WIDTH * 4,
        )

    @wraps(OttBaseMap.add_object)
    def update_map(self, **kwargs):
        super().update_map()
        self.update()
        self.update_idletasks()
