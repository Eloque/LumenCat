import os

import customtkinter

from tkinter import filedialog
import tkinter as tk
from laserproject import LaserProject

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # For now, I am going to put the LaserProject here
        self.laser_project = None

        # configure window
        self.title("LumenCat")
        self.geometry(f"{1200}x{800}")

        # configure grid layout (3x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Tools", font=customtkinter.CTkFont(size=20, weight="bold"))

        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Tool 1", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)

        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")

        self.control_bar = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        label = customtkinter.CTkLabel(self.control_bar, text="Control", font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.control_bar.grid(row=0, column=3, rowspan=2, sticky="nsew")

        self.button_load_file = customtkinter.CTkButton(master=self.control_bar,
                                                        command = self.button_load_file_event,
                                                        text="Load File",
                                                        fg_color="transparent",
                                                        border_width=2,
                                                        text_color=("gray10", "#DCE4EE"))
        self.button_load_file.grid(row=1, column=0, padx=20, pady=10)

        self.button_load_test = customtkinter.CTkButton(master=self.control_bar,
                                                        command = self.button_load_test_object,
                                                        text="Load test object",
                                                        fg_color="transparent",
                                                        border_width=2,
                                                        text_color=("gray10", "#DCE4EE"))
        self.button_load_test.grid(row=2, column=0, padx=20, pady=10)

        self.button_load_test = customtkinter.CTkButton(master=self.control_bar,
                                                        command = self.button_render_event,
                                                        text="Render",
                                                        fg_color="transparent",
                                                        border_width=2,
                                                        text_color=("gray10", "#DCE4EE"))
        self.button_load_test.grid(row=3, column=0, padx=20, pady=10)


        # create main canvas frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.bind("<Configure>", self.on_configure)

        # Create a standard Tkinter canvas inside the CTkFrame
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.main_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew", rowspan=2)
        self.appearance_mode_optionemenu.set("System")

        # On the canvas draw a rectangle, from 0,0 to 500,500
        self.canvas.create_rectangle(0, 0, 400, 400)

        # Also, draw a dot every 10 pixels
        for i in range(0, 400, 10):
            self.canvas.create_line(i, 0, i, 400, fill="gray")
            self.canvas.create_line(0, i, 400, i, fill="gray")

        self.scale_factor = 1

        # Move to the second screen for dev reasons
        # This is a dirty hack, to work around WSL2 tomfoolery
        self.geometry(f"+2900+100")

    def on_configure(self, event):
        self.rescale()

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def button_load_file_event(self):

        # Get the current directory
        current_directory = os.getcwd()

        # Create filedialog
        filename = filedialog.askopenfilename(initialdir=current_directory, title="Select file",
                                                filetypes=(("svg files", "*.svg"), ("all files", "*.*")))

        # Create LaserProject
        self.laser_project = LaserProject()
        self.laser_project.load_from_svg_file(filename)


    def button_load_test_object(self):

        # Create LaserProject
        self.laser_project = LaserProject()
        self.laser_project.load_test_project()

    def button_render_event(self):

        self.canvas.scale("all", 0, 0, 1, 1)

        # Get all the points from the svg
        shapes = self.laser_project.get_all_shapes_as_points()

        # Go through all the points
        for shape in shapes:
            # And draw them on the canvas
            for point_list in shape["points"]:

                for sections in point_list:
                    current_point = sections[0]

                    for point in sections[1:]:

                        self.canvas.create_line(current_point[0], current_point[1], point[0], point[1], fill="black")
                        current_point = point

        self.canvas.create_line(0, 0, 400,400, fill="black")
        self.canvas.scale("all", 0, 0, self.scale_factor, self.scale_factor)

    def rescale(self):
        # Get the current width of the canvas parent frame
        width = self.main_frame.winfo_width()

        # Calculate the scale factor
        self.scale_factor = width / 400

        # And zoom in on the canvas, so the rectangle is the size of the canvas
        self.canvas.scale("all", 0, 0, self.scale_factor, self.scale_factor)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()