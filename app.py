from os import path
from threading import Thread
from typing import Callable, Any
from customtkinter import CTk, StringVar, BooleanVar
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service

import features
from esheets import import_excel
from gsheets import import_gsheet
from components import Notification, AccountFrame, FeatureFrame

# CREDENTAILS PATH.
CREDENTAILS_PATH = path.join("resources", "chromedriver.exe")


class App(CTk):
    DRIVER, DATA = None, []
    OPTIONS = ["LOGIN", "SEND CONNECT", "SEND MESSAGE"]

    @classmethod
    def load_driver(cls) -> None:
        if cls.DRIVER != None:
            cls.DRIVER.quit()
            cls.DRIVER = None

        try:
            service = Service(executable_path=CREDENTAILS_PATH)
            cls.DRIVER = Chrome(service=service)
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
        self.notification = StringVar(value="")
        self.is_logged_in = BooleanVar(value=False)
        self.used_cookies = BooleanVar(value=False)
        self.used_gsheets = BooleanVar(value=True)
        self.username = StringVar(value="partner.info@ah-globalgroup.com")
        self.password = StringVar(value="Nhan123@")
        self.control = StringVar(value=App.OPTIONS[0])
        # LAYOUT.
        AccountFrame(
            self,
            username=self.username,
            password=self.password,
            used_cookies=self.used_cookies,
            used_gsheets=self.used_gsheets,
        )
        Notification(self, textvariable=self.notification)
        FeatureFrame(
            self, control=self.control, options=App.OPTIONS, command=self.run_task
        )

    def set_location(self) -> None:
        # SET WINDOW SIZE.
        WINDOW_WIDTH, WINDOW_HEIGHT = 400, 475
        # GET SCREEN SIZE.
        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()
        # CALCULATE POSITION.
        X_POSITION = SCREEN_WIDTH - WINDOW_WIDTH
        Y_POSITION = (SCREEN_HEIGHT // 2) - (WINDOW_HEIGHT // 2)
        # SET LOCATION.
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{X_POSITION}+{Y_POSITION}")

    def on_closing(self) -> None:
        if App.DRIVER != None:
            App.DRIVER.quit()
        self.destroy()

    def check_login(self) -> bool:
        # CLEAR NOTIFICATION.
        self.notification.set("")
        # LOAD DATA.
        App.DATA = import_gsheet() if self.used_gsheets.get() else import_excel()
        if not App.DATA:
            self.notification.set("CAN'T LOAD DATA")
            return False
        # LOAD DRIVER.
        App.load_driver()
        if not App.DRIVER:
            self.notification.set("CAN'T LOAD DRIVER")
            return False
        return True

    def login(self) -> None:
        if self.check_login():
            Thread(
                target=lambda: features.login(
                    App.DRIVER,
                    self.notification,
                    self.is_logged_in,
                    self.used_cookies,
                    self.username.get(),
                    self.password.get(),
                )
            ).start()

    def check_run_feature(self) -> bool:
        # CLEAR NOTIFICATION.
        self.notification.set("")
        # CHECK LOGIN.
        if not self.is_logged_in.get():
            self.notification.set("CAN'T FIND ACCOUNT")
            return False
        return True

    def run_feature(self, feature: Callable[..., Any]) -> None:
        if self.check_run_feature():
            Thread(
                target=lambda: feature(
                    App.DRIVER, App.DATA, self.notification, self.used_gsheets
                )
            ).start()

    def run_task(self) -> None:
        match self.control.get():
            case "LOGIN":
                self.login()
            case "SEND CONNECT":
                self.run_feature(features.run_send_connect)
            case "SEND MESSAGE":
                self.run_feature(features.run_send_message)


if __name__ == "__main__":
    App().mainloop()
