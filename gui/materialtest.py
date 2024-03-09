import customtkinter
from customtkinter import CTkFrame

import laserproject
from CTkSpinbox import Spinbox

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

        y = 3 + 2
        x = 0

        text_power = 150
        text_speed = 1500

        # Rectangle size
        rectangle_size = 5

        for speed in speed_values:

            laser_object = LaserTextObject(speed, "../fonts/Ubuntu-R.ttf", 8, text_speed, text_power, 1)
            laser_object.location = (x, y)
            self.laser_project.laser_objects.append(laser_object)
            y += ( rectangle_size + 2 )

        y = 0
        x = 9 - 1

        for power in power_values:
            laser_object = LaserTextObject(power, "../fonts/Ubuntu-R.ttf", 8, text_speed, text_power, 1)
            laser_object.location = (x, y)
            self.laser_project.laser_objects.append(laser_object)
            x += (rectangle_size + 2)

        x = 8
        y = 4

        # Create laser objects
        for speed in speed_values:

            for power in power_values:
                laser_object = LaserObject(speed, power*10, 1)
                laser_object.add_rectangle(x, y, rectangle_size, rectangle_size)
                laser_object.fill()

                self.laser_project.laser_objects.append(laser_object)

                x += (rectangle_size + 2)

            x = 8
            y += (rectangle_size + 2)

        self.draw_all_elements()

        return

    def draw_all_elements(self):

        # Initialize to extreme values to ensure they are updated
        max_x = -float('inf')
        min_y = float('inf')

        # Iterate through points to find min and max values
        for laser_object in self.laser_project.laser_objects:
            for shape in laser_object.get_process_points():
                for point in shape["points"]:
                    max_x = max(max_x, point[0])
                    min_y = min(min_y, point[1])

        # Assume max_y and min_x are constants
        max_y = 400
        min_x = 0

        # Calculate spreads
        spread_x = max_x - min_x
        spread_y = max_y - min_y

        # Determine the scale factor based on the larger spread
        scale_factor = 490 / max(spread_x, spread_y)

        # Clear the canvas
        self.canvas.delete("all")

        # Draw it to canvas
#        self.laser_project.draw_laser_objects(self.canvas, scale_factor)

        for laser_object in self.laser_project.laser_objects:

            object_points = laser_object.get_process_points()

            # Sort the object_points, so that objects that have fill "true" are drawn first
            object_points = sorted(object_points, key=lambda x: x["fill"], reverse=True)

            # Rescale all the points from it 400x400 to 300x300
            for shape in object_points:
                current_point = shape["points"][0]

                for i, point in enumerate(shape["points"]):
                    # Rescale points directly
                    point[0] = (point[0] * scale_factor) + 5
                    point[1] = ((point[1] - min_y) * scale_factor) + 5

                    if shape["fill"]:
                        color = laserproject.get_color_by_power(laser_object.power)
                    else:
                        color = "black"

                    # Draw lines from the current point to the next, starting from the second iteration
                    if i > 0:
                        self.canvas.create_line(current_point[0], current_point[1],
                                                point[0], point[1], fill=color, width=1)

                    current_point = point


