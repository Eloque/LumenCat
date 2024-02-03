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

        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Circle", command=self.create_circle)
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)

        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Crochet", command=self.create_crochet)
        self.sidebar_button_1.grid(row=3, column=0, padx=20, pady=10)

        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Minecraft", command=self.create_sword)
        self.sidebar_button_1.grid(row=4, column=0, padx=20, pady=10)

        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Terrain", command=self.create_terrain_base)
        self.sidebar_button_1.grid(row=5, column=0, padx=20, pady=10)

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
        # self.main_frame = CTkXYFrame(self, width=600, height=600, corner_radius=0)
        self.main_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        self.appearance_mode_optionemenu.set("System")

        # Create a standard Tkinter canvas inside the CTkFrame
        # Make it scrollable, and bedsize + 2 x offset
        self.bed_size = 400
        self.offset = 10
        self.scale_factor = 4
        self.bar_size = 50

        # self.canvas = tk.Canvas(self.main_frame, bg="white", width=self.bed_size + self.offset * 2, height=self.bed_size + self.offset * 2)
        self.canvas = tk.Canvas(self.main_frame,
                                bg="white",
                                width=( self.bed_size * self.scale_factor) + self.offset * 2 + self.bar_size,
                                height=( self.bed_size * self.scale_factor) + self.offset * 2 + self.bar_size
                                )
        self.canvas.pack()

        # Create a button bar beneath the canvas
        self.canvas_control_bar = customtkinter.CTkFrame(self, height=30, corner_radius=0)
        self.canvas_control_bar.grid(row=1, column=1, padx=20, pady=2, sticky="nsew")

        # add plus and minus buttons
        self.plus_button = customtkinter.CTkButton(self.canvas_control_bar, text="+", command=self.zoom_in)
        self.plus_button.grid(row=0, column=0, padx=20, pady=2)
        self.minus_button = customtkinter.CTkButton(self.canvas_control_bar, text="-", command=self.zoom_out)
        self.minus_button.grid(row=0, column=1, padx=20, pady=2)

        # Wait some time, so the window can be moved
        self.after(100, self.draw_all_elements)
        self.after(100, self.move_canvas_to_origin)


        # Move to the second screen for dev reasons
        # This is a dirty hack, to work around WSL2 tomfoolery
        self.geometry(f"+2700+100")

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

        # Also move them by the bar size, but we probably need to do that somewhere else
        self.canvas.move("all", self.bar_size, 0)

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

        # put down coordinates at the side and bottom
        for x in range(0, self.bed_size + spacing, spacing):
            item = self.canvas.create_text(x, self.bed_size + 2, text=str(x))

            # now scale the item created
            self.canvas.scale(item, 0, 0, self.scale_factor, self.scale_factor)

        for y in range(self.bed_size + spacing, -1, -spacing):
            item = self.canvas.create_text(-2, y, text=str(self.bed_size-y))

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

        # Check if we have a LaserProject, create it if needed
        if self.laser_project is None:
            self.laser_project = LaserProject()

        # Create a LaserObject
        laser_object = LaserObject(600, 250, 1)
        laser_object.location = (0,0)

        laser_object.add_polygon(points)

        # Add the LaserObject to the LaserProject
        self.laser_project.laser_objects.append(laser_object)

        # And draw all it
        self.draw_all_elements()

    def create_circle(self):

        # Check if we have a LaserProject, create it if needed
        if self.laser_project is None:
            self.laser_project = LaserProject()

        # Heavy cut mdf?
        speed = 200
        power = 800
        passes = 4

        # Trial 2
        speed = 400
        power = 700
        passes = 10

        l = 7

        # Create a LaserObject
        laser_object = LaserObject(speed, power, passes)
        laser_object.location = (l,l)
        laser_object.add_circle(5,5, 5)

        # Add the LaserObject to the LaserProject
        self.laser_project.laser_objects.append(laser_object)

        laser_object = LaserObject(speed, power, passes)
        laser_object.location = (l,l)
        laser_object.add_circle(5,5, 9)

        # Add the LaserObject to the LaserProject
        self.laser_project.laser_objects.append(laser_object)

        laser_object = LaserObject(speed, power, passes)
        laser_object.location = (l,l)
        laser_object.add_circle(5,5, 12)

        # Add the LaserObject to the LaserProject
        self.laser_project.laser_objects.append(laser_object)

        # And draw all it
        self.draw_all_elements()

    def create_crochet(self):

        self.laser_project = LaserProject()
        speed = 600
        power = 700
        passes = 20

        # Add 6cm x 6cm square
        laser_object = LaserObject(speed, power, passes)
        laser_object.location = (0,0)

        laser_object.add_rounded_rectangle(30,30,60,60,5)

        # Add four circles, each 2mm in diameter, at the corners
        laser_object.add_circle(5, 5, 1.5)
        laser_object.add_circle(55, 55, 1.5)
        laser_object.add_circle(5, 55, 1.5)
        laser_object.add_circle(55, 5, 1.5)

        self.laser_project.laser_objects.append(laser_object)

        laser_object = LaserTextObject("5cm x 5cm\nBoven", "../Ubuntu-R.ttf", 20, 600, 250, 1)
        laser_object.location = (5,15)

        self.laser_project.laser_objects.append(laser_object)

        self.draw_all_elements()

    def zoom_in(self):

        self.scale_factor += 1

        # Set canvas width and height
        self.canvas.config(width=( self.bed_size * self.scale_factor) + self.offset * 2 + self.bar_size,
                           height=( self.bed_size * self.scale_factor) + self.offset * 2 + self.bar_size)

        #
        # self.canvas = tk.Canvas(self.main_frame,
        #                         bg="white",
        #                         width=( self.bed_size * self.scale_factor) + self.offset * 2 + self.bar_size,
        #                         height=( self.bed_size * self.scale_factor) + self.offset * 2 + self.bar_size
        #                         )


        self.draw_all_elements()

    def zoom_out(self):

        self.scale_factor -= 1

        # Set canvas width and height
        self.canvas.config(width=( self.bed_size * self.scale_factor) + self.offset * 2 + self.bar_size,
                           height=( self.bed_size * self.scale_factor) + self.offset * 2 + self.bar_size)

        self.draw_all_elements()

    def create_sword(self):

        self.laser_project = LaserProject()
        # laser_object = LaserObject(400, 700, 10)  partial succes
        # laser_object = LaserObject(180, 850, 4)   failed

        # laser_object = LaserObject(600, 700, 15) partial fail
        # laser_object = LaserObject(300, 700, 12) fail
        # laser_object = LaserObject(400, 1000, 10) failed, barely

        laser_object = LaserObject(190, 900, 1 )

        laser_object.location = (0,0)

        pommel = [
                (0,0),
                (0,3),
                (2,3)
            ]

        #laser_object.add_polygon(pommel)

        x = 2
        y = 3

        hilt1 = [
                (x,y),
                (x,y+1),
                (x+1,y+1)
            ]

        #laser_object.add_polygon(hilt)

        x+=1
        y+=1

        hilt2 = [
                (x,y+1),
                (x+1,y+1),
                (x+1,y+2)
            ]

        #laser_object.add_polygon(hilt)

        guard = [
                (x,y+2),
                (x,y+4),
                (x-1,y+4),
                (x-1,y+6),
                (x+1,y+6),
                (x+1,y+5),
                (x+2,y+5),
                (x+2,y+4)
        ]

        #laser_object.add_polygon(guard)

        x+=3
        y+=4

        blade = [(x,y)]

        for i in range(0, 7):

            y += 1
            blade.append((x,y))

            x += 1
            blade.append((x,y))

        # tip
        y += 1
        blade.append((x, y))
        x += 3
        blade.append((x,y))
        y -= 3
        blade.append((x, y))
        x -= 1
        blade.append((x, y))

        for i in range(0, 7):

            y -= 1
            blade.append((x,y))

            x -= 1
            blade.append((x,y))

        y -= 1
        blade.append((x, y))
        x+=1
        blade.append((x, y))
        y -= 1
        blade.append((x, y))
        x+=1
        blade.append((x, y))
        y -= 2
        blade.append((x, y))
        x -= 2
        blade.append((x, y))
        y += 1
        blade.append((x, y))
        x -= 2
        blade.append((x, y))
        y += 1
        blade.append((x, y))
        x -= 1
        blade.append((x, y))
        y -= 1
        blade.append((x, y))
        x -= 1
        blade.append((x, y))
        y -= 1
        blade.append((x, y))
        x -= 1
        blade.append((x, y))
        y -= 2
        blade.append((x, y))
        x -= 3
        blade.append((x, y))

        sword = pommel + hilt1 + hilt2 + guard + blade

        # make the sword 3 times as big
        sword = [(x * 3, y * 3) for x, y in sword]

        #laser_object.add_polygon(sword)
        #laser_object.add_circle(4.5, 4.5, 1)

        # # Copy sword
        # sword2 = sword.copy()
        #
        # # rotate the sword 180 degrees
        # sword2 = [(-x, -y) for x, y in sword2]
        #
        # # and move the sword2 up by 50
        # sword2 = [(x+78, y + 48 + 10) for x, y in sword2]
        #
        # laser_object.add_polygon(sword2)
        # laser_object.add_circle(78-4.5, 10+48-4.5, 1)
        #
        # laser_object.add_polygon(sword2)

        # create a copy of sword, move it to the right by 50
        for i in range(0, 1):
            sword2 = sword.copy()
            sword2 = [(x+35*i, y+0) for x, y in sword2]

            laser_object.add_circle(35*i + 4.5, 4.5, 1)
            laser_object.add_polygon(sword2)

        # sword3 = sword.copy()
        # sword3 = [(x+35, y) for x, y in sword3]
        # laser_object.add_polygon(sword3)

        self.laser_project.laser_objects.append(laser_object)
        self.draw_all_elements()

    def create_terrain_base(self):

        self.laser_project = LaserProject()
        speed = 1600
        power = 500
        passes = 3

        # Add 6cm x 6cm square
        laser_object = LaserObject(speed, power, passes)
        laser_object.location = (0, 0)

        laser_object.add_rounded_rectangle(30, 15+2.5, 50, 25, 5)
        laser_object.add_rounded_rectangle(30 + 5 + 50, 15+2.5, 50, 25, 5)
        laser_object.add_rounded_rectangle(30 + 10 + 100, 15+2.5, 50, 25, 5)

        laser_object.add_rounded_rectangle(30, 15+25+5+5, 50, 25, 5)
        laser_object.add_rounded_rectangle(30 + 5 + 50, 15+25+5+5, 50, 25, 5)
        laser_object.add_rounded_rectangle(30 + 10 + 100, 15+25+5+5, 50, 25, 5)

        laser_object.add_rectangle(0,0, 170, 70)

        self.laser_project.laser_objects.append(laser_object)



        self.laser_project.laser_objects.append(laser_object)

        self.draw_all_elements()

if __name__ == "__main__":
    app = App()
    app.mainloop()