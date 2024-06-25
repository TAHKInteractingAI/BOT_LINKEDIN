from threading import Thread
from customtkinter import CTk, StringVar, BooleanVar

import features
from components import Notification, AccountFrame, FeatureFrame


class App(CTk):
    DRIVER, DATA = None, []

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
        self.username = StringVar(value="partner.info@ah-globalgroup.com")
        self.password = StringVar(value="Nhan123@")
        # LAYOUT.
        AccountFrame(self, username=self.username, password=self.password)
        Notification(self, textvariable=self.notification)
        FeatureFrame(self, login=self.login, run_task=self.run_task)

    def set_location(self) -> None:
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

    def on_closing(self) -> None:
        if App.DRIVER != None:
            App.DRIVER.quit()
        self.destroy()

    def check_login(self) -> bool:
        # CLEAR NOTIFICATION.
        self.notification.set("")
        # LOAD DATA.
        App.DATA = features.import_excel()
        if not App.DATA:
            self.notification.set("CAN'T LOAD DATA")
            return False
        # LOAD DRIVER.
        App.DRIVER = features.load_driver(App.DRIVER)
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
                    self.username.get(),
                    self.password.get(),
                )
            ).start()

    def check_run_task(self) -> bool:
        # CLEAR NOTIFICATION.
        self.notification.set("")
        # CHECK LOGIN.
        if not self.is_logged_in.get():
            self.notification.set("CAN'T FIND ACCOUNT")
            return False
        return True

    def run_task(self) -> None:
        if self.check_run_task():
            Thread(
                target=lambda: features.run_task(
                    App.DRIVER, App.DATA, self.notification
                )
            ).start()


if __name__ == "__main__":
    App().mainloop()
