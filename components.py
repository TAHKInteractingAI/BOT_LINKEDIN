from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry, CTkFrame, CTkCheckBox
from constants import FONT_B, FONT_I


class CustomEntry(CTkEntry):
    def __init__(self, **configs):
        padx, pady = configs.pop("padx", 20), configs.pop("pady", 20)
        configs.update({"width": 280, "height": 45, "font": FONT_I})

        super().__init__(**configs)
        self.pack(padx=padx, pady=pady)


class UsedCookies(CTkCheckBox):
    def __init__(self, **configs):
        configs.update({"text": "Apply Cookies", "font": FONT_I})

        super().__init__(**configs)
        self.pack(anchor="w", padx=20, pady=20)


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
        used_cookies = configs.pop("used_cookies", None)

        CustomEntry(master=self, textvariable=username)
        CustomEntry(master=self, textvariable=password, show=" ", pady=0)
        UsedCookies(master=self, variable=used_cookies)


class FeatureFrame(CTkFrame):
    def __init__(self, master: CTk, **configs):
        super().__init__(master, fg_color="transparent")
        self.pack()
        # FEATURES.
        login, run_task = configs.pop("login", None), configs.pop("run_task", None)
        CustomButton(master=self, text="LOGIN", command=login, pady=20)
        CustomButton(master=self, text="RUN TASK", command=run_task)
