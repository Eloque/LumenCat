import os

import customtkinter
from CTkXYFrame import *

from tkinter import filedialog
import tkinter as tk
from laserproject import LaserProject, LaserObject, LaserTextObject

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
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Triangle", command=self.create_triangle)
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
                                                        command = self.create_gcode,
                                                        text="Export GCode",
                                                        fg_color="transparent",
                                                        border_width=2,
                                                        text_color=("gray10", "#DCE4EE"))
        self.button_load_test.grid(row=3, column=0, padx=20, pady=10)

        self.button_resize_canvas = customtkinter.CTkButton(master=self.control_bar,
                                                        command = self.fit_canvas_to_frame,
                                                        text="Resize Canvas",
                                                        fg_color="transparent",
                                                        border_width=2,
                                                        text_color=("gray10", "#DCE4EE"))
        self.button_resize_canvas.grid(row=4, column=0, padx=20, pady=10)

        self.button_resize_canvas = customtkinter.CTkButton(master=self.control_bar,
                                                        command = self.move_canvas_to_origin,
                                                        text="Move Canvas",
                                                        fg_color="transparent",
                                                        border_width=2,
                                                        text_color=("gray10", "#DCE4EE"))
        self.button_resize_canvas.grid(row=5, column=0, padx=20, pady=10)

        self.button_resize_canvas = customtkinter.CTkButton(master=self.control_bar,
                                                        command = self.draw_all_elements,
                                                        text="Draw Control Elements",
                                                        fg_color="transparent",
                                                        border_width=2,
                                                        text_color=("gray10", "#DCE4EE"))
        self.button_resize_canvas.grid(row=6, column=0, padx=20, pady=10)



        # create main canvas frame
        self.main_frame = CTkXYFrame(self, width=600, height=600, corner_radius=0)
        self.main_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        self.appearance_mode_optionemenu.set("System")

        # Create a standard Tkinter canvas inside the CTkFrame
        # Make it scrollable, and bedsize + 2 x offset
        self.bed_size = 400
        self.offset = 10
        self.scale_factor = 8

        # self.canvas = tk.Canvas(self.main_frame, bg="white", width=self.bed_size + self.offset * 2, height=self.bed_size + self.offset * 2)
        self.canvas = tk.Canvas(self.main_frame,
                                bg="white",
                                width=( self.bed_size * self.scale_factor) + self.offset * 2,
                                height=( self.bed_size * self.scale_factor) + self.offset * 2
                                )
        self.canvas.pack()

        # Create a scrollbar for the canvas

        # Wait some time, so the window can be moved
        self.after(100, self.draw_all_elements)
        self.after(100, self.move_canvas_to_origin)


        # Move to the second screen for dev reasons
        # This is a dirty hack, to work around WSL2 tomfoolery
        self.geometry(f"+2900+100")

    def on_configure(self, event):
        pass

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

        # Should that really be here? The redraw function?
        # And draw it
        self.draw_all_elements()

        return

    def button_render_event(self):

        self.draw_all_elements()

    # Combined function to draw both control and LaserObject elements
    def draw_all_elements(self):

        # Clear the canvas
        self.canvas.delete("all")

        # Draw the control elements
        self.draw_control_elements()

        # Check if the laser project is loaded
        if self.laser_project is None:
            pass
        else:
            self.draw_laser_project()

        # take all the items of the canvas, and move them by offset
        self.canvas.move("all", self.offset, self.offset)

        # Apply the current scaling
        # self.canvas.scale("all", 0, 0, self.scale_factor, self.scale_factor)

    def draw_control_elements(self):

        # # Put a dot at every 25 mm
        spacing = 25
        radius = 0.1

        for x in range(0, self.bed_size + spacing, spacing):
            for y in range(0, self.bed_size + spacing, spacing):
                item = self.canvas.create_oval(x - radius,
                                        y - radius,
                                        x + radius,
                                        y + radius, outline="black", fill="black")

                # now scale the item created
                self.canvas.scale(item, 0, 0, self.scale_factor, self.scale_factor)

        main_dash = 3
        # draw a thin dotted line at every 25mm on the X and Y axis
        for y in range(0, self.bed_size + spacing, spacing):
            item = self.canvas.create_line(0, y, self.bed_size, y, dash=(main_dash, main_dash))

            # now scale the item created
            self.canvas.scale(item, 0, 0, self.scale_factor, self.scale_factor)

        for x in range(0, self.bed_size + spacing, spacing):
            item = self.canvas.create_line(x, 0, x, self.bed_size, dash=(main_dash, main_dash))

            # now scale the item created
            self.canvas.scale(item, 0, 0, self.scale_factor, self.scale_factor)

    def draw_laser_project(self):

        # We will iterate through all the shapes we have
        # Get all shapes as process points
        shapes = self.laser_project.get_all_shapes_as_process_points()

        # And then draw it
        # Go through all the points
        for shape in shapes:
            # And draw them on the canvas
            for point_list in shape:
                current_point = point_list[0]

                for point in point_list:

                    line = self.canvas.create_line(current_point[0]  , current_point[1] ,
                                                   point[0], point[1], fill="black", width=3)

                    self.canvas.scale(line, 0, 0, self.scale_factor, self.scale_factor)
                    current_point = point

        return

    def create_gcode(self):

        gcode = self.laser_project.get_gcode()

        # Open the gcode file
        with open("gcode.nc", "w") as f:
            for item in gcode:
                f.write(item + "\n")

    def fit_canvas_to_frame(self):

        raise NotImplemented

    def move_canvas_to_origin(self):

        # set the vsb in main_frame to max
        self.main_frame.xy_canvas.yview_moveto(1.0)
        self.main_frame.xy_canvas.xview_moveto(0.0)


    def create_triangle(self):

        # We are going to create a triangle with cartasion coordinates
        # from 25,25 to 25,50 to 50,25

        points = [[25, 25], [25, 50], [50, 25], [25, 25]]

        # Check if we have a LaserProject, create it if needed
        if self.laser_project is None:
            self.laser_project = LaserProject()

        lt = LaserTextObject("J", "../Ubuntu-R.ttf", 20, 600, 250)
        self.laser_project.laser_objects.append(lt)

        self.draw_all_elements()

        return

        # Create a LaserObject
        laser_object = LaserObject(600, 250)
        laser_object.location = (0,0)

        laser_object.add_polygon(points)

        # Add the LaserObject to the LaserProject
        self.laser_project.laser_objects.append(laser_object)

        # And draw all it
        self.draw_all_elements()




if __name__ == "__main__":
    app = App()
    app.mainloop()