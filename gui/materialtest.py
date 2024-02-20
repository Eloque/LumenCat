
import customtkinter
from CTkXYFrame import *
import tkinter as tk

from laserproject import LaserProject, LaserObject, LaserTextObject


class MaterialTest:
    def __init__(self, parent):
        self.root = customtkinter.CTkToplevel(parent)
        self.parent = parent
        root = self.root

        self.laser_project = None

        root.title("Material Test")

        frame = CTkXYFrame(root, width=660, height=330)
        frame.grid(row=0, column=0, padx=10, pady=10)

        self.canvas = customtkinter.CTkCanvas(frame, width=300, height=300)
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

        self.min_power = tk.StringVar()
        min_power_label = customtkinter.CTkLabel(settings_frame, text="Min")
        min_power_entry = customtkinter.CTkEntry(settings_frame, width=60, textvariable=self.min_power)

        self.max_power = tk.StringVar()
        max_power_label = customtkinter.CTkLabel(settings_frame, text="Max")
        max_power_entry = customtkinter.CTkEntry(settings_frame, width=60, textvariable=self.max_power)

        self.power_steps = tk.StringVar()
        steps_power_label = customtkinter.CTkLabel(settings_frame, text="Steps")
        steps_power_entry = customtkinter.CTkEntry(settings_frame, width=60, textvariable=self.power_steps)

        speed_label = customtkinter.CTkLabel(settings_frame, text="Speed")

        self.min_speed = tk.StringVar()
        min_speed_label = customtkinter.CTkLabel(settings_frame, text="Min")
        min_speed_entry = customtkinter.CTkEntry(settings_frame, width=60, textvariable=self.min_speed)

        self.max_speed = tk.StringVar()
        max_speed_label = customtkinter.CTkLabel(settings_frame, text="Max")
        max_speed_entry = customtkinter.CTkEntry(settings_frame, width=60, textvariable=self.max_speed)

        self.speed_steps = tk.StringVar()
        steps_speed_label = customtkinter.CTkLabel(settings_frame, text="Steps")
        steps_speed_entry = customtkinter.CTkEntry(settings_frame, width=60, textvariable=self.speed_steps)

        settings_label.grid(row=0, column=0, columnspan=5, padx=4, pady=2)

        power_label.grid(row=1, column=0, padx=4, pady=2)
        min_power_label.grid(row=1, column=1, padx=4, pady=2, sticky="e")
        min_power_entry.grid(row=1, column=2, padx=4, pady=2)
        max_power_label.grid(row=1, column=3, padx=4, pady=2, sticky="e")
        max_power_entry.grid(row=1, column=4, padx=4, pady=2)
        steps_power_label.grid(row=2, column=1, padx=4, pady=2, sticky="e")
        steps_power_entry.grid(row=2, column=2, padx=4, pady=2)

        speed_label.grid(row=3, column=0, padx=4, pady=2)
        min_speed_label.grid(row=3, column=1, padx=4, pady=2, sticky="e")
        min_speed_entry.grid(row=3, column=2, padx=4, pady=2)
        max_speed_label.grid(row=3, column=3, padx=4, pady=2, sticky="e")
        max_speed_entry.grid(row=3, column=4, padx=4, pady=2)
        steps_speed_label.grid(row=4, column=1, padx=4, pady=2, sticky="e")
        steps_speed_entry.grid(row=4, column=2, padx=4, pady=2)

        # Set all the values to reasonable defaults
        self.min_power.set(40)
        self.max_power.set(90)
        self.power_steps.set(4)

        self.min_speed.set(200)
        self.max_speed.set(2000)
        self.speed_steps.set(4)

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
        min_power = int(self.min_power.get())
        max_power = int(self.max_power.get())
        power_steps = int(self.power_steps.get())

        min_speed = int(self.min_speed.get())
        max_speed = int(self.max_speed.get())
        speed_steps = int(self.speed_steps.get())

        # Okay, we are going to do the speed vertical
        # and the power horizontal

        # First, clear the canvas
        self.canvas.delete("all")

        # For each speed step, write the speed on canvas
        y = 280
        for speed in range(min_speed, max_speed, (max_speed - min_speed) // speed_steps):
            y -= 25
            self.canvas.create_text(20, y, text=str(speed))
            x = 25
            for power in range(min_power, max_power, (max_power - min_power) // power_steps):
                x += 25
                self.canvas.create_rectangle(x, y+10, x + 20, y - 10, fill="")

        x = 35
        for power in range(min_power, max_power, (max_power - min_power) // power_steps):
            x += 25
            self.canvas.create_text(x, 280, text=str(power))

        # And here the real update is, creating the laser project and laser objects
        # Create laser project
        self.laser_project = LaserProject()

        y = 6 + 2
        x = 0

        text_power = 20
        text_speed = 600
        for speed in range(min_speed, max_speed, (max_speed - min_speed) // speed_steps):

            laser_object = LaserTextObject(speed, "../fonts/Ubuntu-R.ttf", 8, text_speed, text_power, 1)
            laser_object.location = (x, y)
            self.laser_project.laser_objects.append(laser_object)
            y += 12

        y = 0
        x = 12 - 1
        for power in range(min_power, max_power, (max_power - min_power) // power_steps):
            laser_object = LaserTextObject(power, "../fonts/Ubuntu-R.ttf", 8, text_speed, text_power, 1)
            laser_object.location = (x, y)
            self.laser_project.laser_objects.append(laser_object)
            x += 12

        x = 8
        y = 4

        # Create laser objects
        for speed in range(min_speed, max_speed, (max_speed - min_speed) // speed_steps):

            for power in range(min_power, max_power, (max_power - min_power) // power_steps):
                laser_object = LaserObject(speed, power, 1)
                laser_object.add_rectangle(x, y, 10, 10)

                self.laser_project.laser_objects.append(laser_object)

                x += 12

            x = 8
            y += 12

        self.parent.laser_project = self.laser_project
        self.parent.draw_all_elements()

        pass

