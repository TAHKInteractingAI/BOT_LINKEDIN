from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry, CTkFrame, CTkCheckBox

# CONSTANTS.
FONT_B = ("monospace", 14, "bold")
FONT_I = ("monospace", 14, "italic")


class CustomEntry(CTkEntry):
    def __init__(self, **configs):
        padx, pady = configs.pop("padx", 20), configs.pop("pady", 20)
        configs.update({"width": 280, "height": 45, "font": FONT_I})

        super().__init__(**configs)
        self.pack(padx=padx, pady=pady)


class CustomCkBox(CTkCheckBox):
    def __init__(self, **configs):
        side = configs.pop("side", "left")
        configs.update({"font": FONT_I})

        super().__init__(**configs)
        self.pack(side=side, padx=20, pady=20)


class CustomButton(CTkButton):
    def __init__(self, **configs):
        padx, pady = configs.pop("padx", 0), configs.pop("pady", 0)
        configs.update({"width": 150, "height": 40})

        super().__init__(**configs)
        self.pack(padx=padx, pady=pady)


class Notification(CTkLabel):
    def __init__(self, master: CTk, **configs):
        configs.update(
            {
                "width": 300,
                "height": 50,
                "corner_radius": 5,
                "font": FONT_B,
                "fg_color": "white",
                "text_color": "black",
            }
        )

        super().__init__(master, **configs)
        self.pack(padx=20, pady=20)


class AccountFrame(CTkFrame):
    def __init__(self, master: CTk, **configs):
        super().__init__(master)
        self.pack(padx=20, pady=20)
        # CONTROL VARIABLES.
        username, password = configs.pop("username", ""), configs.pop("password", "")
        use_cookies = configs.pop("used_cookies", None)
        use_ghseets = configs.pop("used_gsheets", None)

        CustomEntry(master=self, textvariable=username)
        CustomEntry(master=self, textvariable=password, show=" ", pady=0)
        CustomCkBox(master=self, text="Use Cookies", variable=use_cookies, side="left")
        CustomCkBox(master=self, text="Use GSheets", variable=use_ghseets, side="right")


class FeatureFrame(CTkFrame):
    def __init__(self, master: CTk, **configs):
        super().__init__(master, fg_color="transparent")
        self.pack()
        # FEATURES.
        login, run_task = configs.pop("login", None), configs.pop("run_task", None)
        CustomButton(master=self, text="LOGIN", command=login, pady=20)
        CustomButton(master=self, text="RUN TASK", command=run_task)
