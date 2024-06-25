import threading
import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import tools
import components
import constants as const


class App(ctk.CTk):
    DRIVER, DATA = None, []

    @classmethod
    def load_driver(cls, executable_path=const.PATH_CHROME_DRIVER) -> None:
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
        components.AccountFrame(self, self.username, self.password)
        components.LabelResult(self, self.notification)
        components.CustomButton(self, "LOGIN", self.login, 0, 20)
        components.CustomButton(self, "RUN TASK", self.run_task)

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
        # CLEAR NOTIFICATION.
        self.notification.set("")
        # CHECK DATA STATE.
        tools.import_excel(App.DATA)
        if not App.DATA:
            self.notification.set("DATA IS EMPTY")
            return
        # CHECK DRIVER STATE.
        App.load_driver()
        if not App.DRIVER:
            self.notification.set("CAN'T LOAD DRIVER")
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

    def run_task(self) -> None:
        # CLEAR NOTIFICATION.
        self.notification.set("")
        # CHECK LOGIN STATE.
        if not self.is_logged_in.get():
            self.notification.set("PLEASE LOGIN FIRST")
            return
        # EXECUTE MISSION.
        threading.Thread(
            target=lambda: tools.run_task(App.DRIVER, App.DATA, self.notification)
        ).start()


if __name__ == "__main__":
    App().mainloop()
