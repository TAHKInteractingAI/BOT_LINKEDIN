from os import path
from pickle import load, dump
from customtkinter import StringVar, BooleanVar
from selenium.webdriver.chrome.webdriver import WebDriver


# CONSTANTS.
CREDENTAILS_PATH = path.join("resources", "privates", "cookies.pkl")


def import_cookies() -> list[dict] | None:
    try:
        with open(CREDENTAILS_PATH, "rb") as file:
            return load(file)
    except:
        return None


def export_cookies(driver: WebDriver) -> None:
    with open(CREDENTAILS_PATH, "wb") as file:
        dump(driver.get_cookies(), file)


def login_with_cookies(
    driver: WebDriver, notification: StringVar, is_logged_in: BooleanVar
) -> None:
    cookies = import_cookies()
    # CHECK COOKIES.
    if not cookies:
        notification.set("CAN'T FIND COOKIES")
        is_logged_in.set(False)
        return
    # ADD COOKIES.
    for cookie in cookies:
        driver.add_cookie(cookie)
    # CHECK LOGIN.
    if driver.get(driver, "https://www.linkedin.com/login"):
        notification.set("LOGIN SUCCESSFULLY")
        is_logged_in.set(True)
    else:
        notification.set("LOGIN FAILED")
        is_logged_in.set(False)
