import tools
import threading
import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class CustomButton(ctk.CTkButton):
    def __init__(self, master, text, command, padx=0, pady=0, **configs):
        super().__init__(master, height=40, text=text, command=command, **configs)
        self.pack(padx=padx, pady=pady)


class LabelResult(ctk.CTkLabel):
    def __init__(self, master, textvariable):
        super().__init__(
            master,
            width=300,
            height=50,
            corner_radius=5,
            fg_color="white",
            text_color="black",
            font=("monospace", 14, "bold"),
            textvariable=textvariable,
        )
        self.pack(padx=20, pady=20)


class CustomEntry(ctk.CTkEntry):
    def __init__(self, padx=20, pady=20, width=280, height=45, **configs):
        super().__init__(width=width, height=height, **configs)
        self.pack(padx=padx, pady=pady)


class AccountFrame(ctk.CTkFrame):
    def __init__(self, master, username: ctk.StringVar, password: ctk.StringVar):
        super().__init__(master, 300, 200)
        self.pack(pady=20)
        # USERNAME & PASSWORD FIELD.
        FONT = ("monospace", 14, "italic")
        CustomEntry(
            master=self,
            placeholder_text="Enter your username",
            font=FONT,
            textvariable=username,
        )
        CustomEntry(
            master=self,
            placeholder_text="Enter your password",
            font=FONT,
            textvariable=password,
            show=" ",
        )


class App(ctk.CTk):
    DRIVER, DATA = None, []

    @classmethod
    def load_driver(cls, executable_path="chromedriver.exe") -> None:
        """Load Chrome Driver."""
        if cls.DRIVER != None:
            cls.DRIVER.quit()
        try:
            service = Service(executable_path=executable_path)
            cls.DRIVER = webdriver.Chrome(service=service)
            cls.DRIVER.implicitly_wait(10)
        except:
            cls.DRIVER = None

    def __init__(self):
        super().__init__(fg_color="black")
        self.title("")
        self.set_location()
        self.resizable(False, False)
        self.wm_attributes("-topmost", 1)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # CONTROL VARIABLE.
        self.notification = ctk.StringVar(value="")
        self.is_logged_in = ctk.BooleanVar(value=False)
        self.username = ctk.StringVar(value="partner.info@ah-globalgroup.com")
        self.password = ctk.StringVar(value="Nhan123@")
        # LAYOUT.
        AccountFrame(self, self.username, self.password)
        LabelResult(self, self.notification)
        CustomButton(self, "LOGIN", self.login, 0, 20)
        CustomButton(self, "CONNECT", self.connect)

    def set_location(self):
        # SET WINDOW SIZE.
        WINDOW_WIDTH, WINDOW_HEIGHT = 400, 450
        # GET SCREEN SIZE.
        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()
        # CALCULATE POSITION.
        X_POSITION = SCREEN_WIDTH - WINDOW_WIDTH
        Y_POSITION = (SCREEN_HEIGHT // 2) - (WINDOW_HEIGHT // 2)
        # SET LOCATION.
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{X_POSITION}+{Y_POSITION}")

    def on_closing(self):
        if App.DRIVER != None:
            App.DRIVER.quit()
        self.destroy()

    def login(self) -> None:
        # CHECK DATA STATE.
        tools.import_excel(App.DATA)
        if not App.DATA:
            self.notification.set("DATA IS EMPTY!")
            return
        # CHECK DRIVER STATE.
        App.load_driver()
        if not App.DRIVER:
            self.notification.set("CAN'T LOAD DRIVER!")
            return
        # EXECUTE MISSION.
        threading.Thread(
            target=lambda: tools.login(
                App.DRIVER,
                self.notification,
                self.is_logged_in,
                self.username.get(),
                self.password.get(),
            )
        ).start()

    def connect(self) -> None:
        # CHECK LOGIN STATE.
        if not self.is_logged_in.get():
            self.notification.set("PLEASE LOGIN FIRST!")
            return
        # EXECUTE MISSION.
        threading.Thread(
            target=lambda: tools.connect(App.DRIVER, App.DATA, self.notification)
        ).start()


if __name__ == "__main__":
    App().mainloop()
