import tkinter as tk

class DrawingBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Board")

        # Canvas setup
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Track mouse movement
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset_position)

        # Initialize variables
        self.last_x, self.last_y = None, None
        self.pen_color = "black"
        self.pen_size = 2

        # Create control buttons
        self.controls_frame = tk.Frame(root, padx=5, pady=5)
        self.controls_frame.pack()

        self.color_button = tk.Button(self.controls_frame, text="Choose Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.controls_frame, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.size_label = tk.Label(self.controls_frame, text="Brush Size:")
        self.size_label.pack(side=tk.LEFT, padx=5)

        self.size_slider = tk.Scale(self.controls_frame, from_=1, to=20, orient=tk.HORIZONTAL)
        self.size_slider.set(self.pen_size)
        self.size_slider.pack(side=tk.LEFT, padx=5)

    def paint(self, event):
        if self.last_x and self.last_y:
            self.pen_size = self.size_slider.get()
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                     width=self.pen_size, fill=self.pen_color, capstyle=tk.ROUND)
        self.last_x, self.last_y = event.x, event.y

    def reset_position(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")

    def choose_color(self):
        from tkinter.colorchooser import askcolor
        color_code = askcolor(title="Choose Pen Color")[1]
        if color_code:
            self.pen_color = color_code

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingBoard(root)
    root.mainloop()
