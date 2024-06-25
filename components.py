from customtkinter import CTkButton, CTkLabel, CTkEntry, CTkFrame, StringVar
from constants import FONT_B, FONT_I


class CustomButton(CTkButton):
    def __init__(self, master, text, command, padx=0, pady=0, **configs):
        super().__init__(master, height=40, text=text, command=command, **configs)
        self.pack(padx=padx, pady=pady)


class LabelResult(CTkLabel):
    def __init__(self, master, textvariable):
        super().__init__(
            master,
            width=300,
            height=50,
            corner_radius=5,
            font=FONT_B,
            fg_color="white",
            text_color="black",
            textvariable=textvariable,
        )
        self.pack(padx=20, pady=20)


class CustomEntry(CTkEntry):
    def __init__(self, padx=20, pady=20, **configs):
        super().__init__(width=280, height=45, font=FONT_I, **configs)
        self.pack(padx=padx, pady=pady)


class AccountFrame(CTkFrame):
    def __init__(self, master, username: StringVar, password: StringVar):
        super().__init__(master, 300, 200)
        self.pack(pady=20)
        # USERNAME & PASSWORD FIELD.
        CustomEntry(master=self, textvariable=username)
        CustomEntry(master=self, textvariable=password, show=" ")
