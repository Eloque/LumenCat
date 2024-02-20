
import customtkinter
from customtkinter import CTkFrame

from CTkSpinbox import Spinbox
import tkinter as tk

from laserproject import LaserProject, LaserObject, LaserTextObject


class MaterialTest:
    def __init__(self, parent):
        self.root = customtkinter.CTkToplevel(parent)
        self.parent = parent
        root = self.root

        self.laser_project = None

        root.title("Material Test")

        frame = CTkFrame(root, width=960, height=640)
        frame.grid(row=0, column=0, padx=10, pady=10)

        self.canvas = customtkinter.CTkCanvas(frame, width=500, height=500)
        self.canvas.grid(row=0, column=0, padx=10, pady=10, rowspan=2)

        settings_frame = customtkinter.CTkFrame(frame, width=300)
        settings_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        button_ok = customtkinter.CTkButton(master=frame,
                                            command=self.update,
                                            text="Update",
                                            fg_color="transparent",
                                            border_width=2,
                                            text_color=("gray10", "#DCE4EE"))

        button_ok.grid(row=1, column=1, sticky="n")

        settings_label = customtkinter.CTkLabel(settings_frame, text="Settings", width=290)

        power_label = customtkinter.CTkLabel(settings_frame, text="Power")

        min_power_label = customtkinter.CTkLabel(settings_frame, text="Min")
        self.min_power_entry = Spinbox(settings_frame, width=130, step_size=5, callback=self.update)

        max_power_label = customtkinter.CTkLabel(settings_frame, text="Max")
        self.max_power_entry = Spinbox(settings_frame, width=130, step_size=5, callback=self.update)

        steps_power_label = customtkinter.CTkLabel(settings_frame, text="Steps")
        self.steps_power_entry = Spinbox(settings_frame, width=130, step_size=1, callback=self.update)

        speed_label = customtkinter.CTkLabel(settings_frame, text="Speed")

        min_speed_label = customtkinter.CTkLabel(settings_frame, text="Min")
        self.min_speed_entry = Spinbox(settings_frame, width=130, step_size=50, callback=self.update)

        max_speed_label = customtkinter.CTkLabel(settings_frame, text="Max")
        self.max_speed_entry = Spinbox(settings_frame, width=130, step_size=50, callback=self.update)

        steps_speed_label = customtkinter.CTkLabel(settings_frame, text="Steps")
        self.steps_speed_entry = Spinbox(settings_frame, width=130, step_size=1, callback=self.update)

        settings_label.grid(row=0, column=0, columnspan=5, padx=4, pady=2)

        power_label.grid(row=1, column=0, padx=4, pady=2)
        min_power_label.grid(row=1, column=1, padx=4, pady=2, sticky="e")
        self.min_power_entry.grid(row=1, column=2, padx=4, pady=2)
        max_power_label.grid(row=1, column=3, padx=4, pady=2, sticky="e")
        self.max_power_entry.grid(row=1, column=4, padx=4, pady=2)
        steps_power_label.grid(row=2, column=1, padx=4, pady=2, sticky="e")
        self.steps_power_entry.grid(row=2, column=2, padx=4, pady=2)

        speed_label.grid(row=3, column=0, padx=4, pady=2)
        min_speed_label.grid(row=3, column=1, padx=4, pady=2, sticky="e")
        self.min_speed_entry.grid(row=3, column=2, padx=4, pady=2)
        max_speed_label.grid(row=3, column=3, padx=4, pady=2, sticky="e")
        self.max_speed_entry.grid(row=3, column=4, padx=4, pady=2)
        steps_speed_label.grid(row=4, column=1, padx=4, pady=2, sticky="e")
        self.steps_speed_entry.grid(row=4, column=2, padx=4, pady=2)

        # Set all the values to reasonable defaults
        self.min_power_entry.set(40)
        self.max_power_entry.set(90)
        self.steps_power_entry.set(4)

        self.min_speed_entry.set(200)
        self.max_speed_entry.set(2000)
        self.steps_speed_entry.set(4)

        # Function to handle the closing of the toplevel
        def on_close():
            self.parent.laser_project = self.laser_project
            self.parent.draw_all_elements()
            self.root.destroy()

        # Set the close event handler
        self.root.protocol("WM_DELETE_WINDOW", on_close)

    def show(self):
        # Goram ugly hack to make the window appear on top
        self.root.after(100, self.root.lift)
        self.root.mainloop()

    def update(self):

        # Get the values from the settings
        min_power = int(self.min_power_entry.get())
        max_power = int(self.max_power_entry.get())
        power_steps = int(self.steps_power_entry.get())

        min_speed = int(self.min_speed_entry.get())
        max_speed = int(self.max_speed_entry.get())
        speed_steps = int(self.steps_speed_entry.get())

        # Create laser project
        self.laser_project = LaserProject()

        step_size = (max_speed - min_speed) / (speed_steps - 1) if speed_steps > 1 else 0
        speed_values = [min_speed + i * step_size for i in range(speed_steps)]
        # convert all speed values to integers
        speed_values = [int(speed) for speed in speed_values]

        step_size = (max_power - min_power) / (power_steps - 1) if power_steps > 1 else 0
        power_values = [min_power + i * step_size for i in range(power_steps)]
        # convert all power values to integers
        power_values = [int(power) for power in power_values]

        y = 6 + 2
        x = 0

        text_power = 20
        text_speed = 600

        for speed in speed_values:

            laser_object = LaserTextObject(speed, "../fonts/Ubuntu-R.ttf", 8, text_speed, text_power, 1)
            laser_object.location = (x, y)
            self.laser_project.laser_objects.append(laser_object)
            y += 12

        y = 0
        x = 12 - 1
        for power in power_values:
            laser_object = LaserTextObject(power, "../fonts/Ubuntu-R.ttf", 8, text_speed, text_power, 1)
            laser_object.location = (x, y)
            self.laser_project.laser_objects.append(laser_object)
            x += 12

        x = 8
        y = 4

        # Create laser objects
        for speed in speed_values:

            for power in power_values:
                laser_object = LaserObject(speed, power, 1)
                laser_object.add_rectangle(x, y, 10, 10)

                self.laser_project.laser_objects.append(laser_object)

                x += 12

            x = 8
            y += 12

        self.draw_all_elements()

    def draw_all_elements(self):

        min_y = 400
        max_x = 0

        # First, clear the canvas
        self.canvas.delete("all")

        # Get the min and max values for x and y
        for laser_object in self.laser_project.laser_objects:
            for shape in laser_object.get_process_points():
                for point in shape:
                    if point[0] > max_x:
                        max_x = point[0]

                    if point[1] < min_y:
                        min_y = point[1]

        max_y = 400
        min_x = 0

        # For Y we need a spread of max_y - min_y
        spread_y = max_y - min_y

        # For X we need a spared of max_x - min_x
        spread_x = max_x - min_x

        if spread_x > spread_y:
            scale_factor = 490 / spread_x
        else:
            scale_factor = 490 / spread_y

        for laser_object in self.laser_project.laser_objects:

            # Get the points for the object
            object_points = laser_object.get_process_points()

            # Rescale all the points from it 400x400 to 300x300
            for shape in object_points:
                for point in shape:
                    point[0] = point[0] * scale_factor
                    point[0] += 5

                    p = point[1]
                    p = (p - min_y) * scale_factor
                    p += 5

                    point[1] = p

            # All of these individual lists, contain individual shapes
            for shape in object_points:
                current_point = shape[0]

                for point in shape:
                    line = self.canvas.create_line(current_point[0], current_point[1],
                                                   point[0], point[1], fill="black", width=1)

                    # add a tag to the line
                    self.canvas.addtag_withtag("laser_object", line)
                    current_point = point


