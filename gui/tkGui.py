import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

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
        self.main_button_1 = customtkinter.CTkButton(master=self.control_bar, text="Load File", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        #self.main_button_1.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_1.grid(row=1, column=0, padx=20, pady=10)

        # create main canvas frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew", rowspan=2)

        self.appearance_mode_optionemenu.set("System")

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()