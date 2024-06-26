from os import path
from time import sleep
from pickle import load, dump
from customtkinter import StringVar, BooleanVar
from pandas import DataFrame, ExcelWriter, read_excel

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import constants as const


# SUPPORT FUNCTION.
def load_driver(driver: WebDriver | None) -> WebDriver | None:
    if driver != None:
        driver.close()
    else:
        try:
            service = Service(executable_path=const.PATH_CHROME_DRIVER)
            driver = Chrome(service=service)
            driver.implicitly_wait(10)
        except:
            driver = None
    return driver


def import_excel() -> list[dict]:
    data = list()
    try:
        df = read_excel(const.PATH_EXCEL_DATA, sheet_name="Sheet1")
        df = df.astype("object")
        df.fillna(value="", inplace=True)
        for index in range(df.shape[0]):
            data.append({key: value[index] for key, value in df.to_dict().items()})
    except:
        pass
    return data


def export_excel(data: list[dict]) -> None:
    with ExcelWriter(const.PATH_EXCEL_DATA, engine="openpyxl", mode="w") as writer:
        DataFrame(data).to_excel(writer, sheet_name="Sheet1", index=False)


def get_link(driver: WebDriver, link: str) -> bool:
    try:
        driver.get(link)
        sleep(5)
        return True
    except:
        return False


def check_status(data: list[dict], index: int, states: list[str]) -> bool:
    status = data[index]["STATE_1"], data[index]["STATE_2"], data[index]["STATE_3"]
    if status == states:
        return True
    else:
        return False


def update_state(data: list[dict], index: int, states: list[str]) -> None:
    data[index]["STATE_1"] = states[0]
    data[index]["STATE_2"] = states[1]
    data[index]["STATE_3"] = states[2]


def import_cookies() -> list[dict] | None:
    try:
        with open("resources/cookies.pkl", "rb") as file:
            return load(file)
    except:
        return None


def export_cookies(driver: WebDriver) -> None:
    with open("resources/cookies.pkl", "wb") as file:
        dump(driver.get_cookies(), file)


# LOGIN TASK.
def handle_verification_pin(driver: WebDriver, notification: StringVar) -> None:
    FIELD = const.CLASS_PIN_VERIFICATION
    CONDITION = EC.presence_of_element_located((By.CLASS_NAME, FIELD))
    try:
        WebDriverWait(driver, 10).until(CONDITION)
        notification.set("PIN VERIFICATION DETECTED")
        WebDriverWait(driver, 120).until_not(CONDITION)
    except TimeoutException:
        notification.set("NO PIN VERIFICATION")


def handle_captcha(driver: WebDriver, notification: StringVar) -> None:
    FIELD = const.ID_CAPTCHA
    CONDITION = EC.presence_of_element_located((By.ID, FIELD))
    try:
        WebDriverWait(driver, 10).until(CONDITION)
        notification.set("CAPTCHA DETECTED")
        WebDriverWait(driver, 120).until_not(CONDITION)
    except TimeoutException:
        notification.set("NO CAPTCHA")


def handle_verification_phone(driver: WebDriver, notification: StringVar) -> None:
    FIELD = const.ID_PHONE_VERIFICATION
    CONDITION = EC.presence_of_element_located((By.ID, FIELD))
    try:
        WebDriverWait(driver, 10).until(CONDITION)
        notification.set("PHONE VERIFICATION DETECTED")
        WebDriverWait(driver, 120).until_not(CONDITION)
    except TimeoutException:
        notification.set("NO PHONE VERIFICATION")


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
    if get_link(driver, "https://www.linkedin.com/login"):
        notification.set("LOGIN SUCCESSFULLY")
        is_logged_in.set(True)
    else:
        notification.set("LOGIN FAILED")
        is_logged_in.set(False)


def login(
    driver: WebDriver,
    notification: StringVar,
    is_logged_in: BooleanVar,
    used_cookies: BooleanVar,
    username: str,
    password: str,
) -> None:
    try:
        # GO TO LOGIN PAGE.
        get_link(driver, "https://www.linkedin.com/login")
        if used_cookies.get():
            login_with_cookies(driver, notification, is_logged_in)
            sleep(3)
        # CHECK LOGIN.
        if is_logged_in.get():
            return
        else:
            notification.set("CONTINUE WITH CREDENTAILS")
            sleep(3)
        # TYPE USERNAME & PASSWORD.
        driver.find_element(By.XPATH, const.FIELD_USERNAME).send_keys(username)
        driver.find_element(By.XPATH, const.FIELD_PASSWORD).send_keys(password)
        sleep(2)
        # CLICK LOGIN BUTTON.
        driver.find_element(By.XPATH, const.BUTTON_SUBMIT_LOGIN).click()
        sleep(5)
        # CHECK LOGIN.
        try:
            driver.find_element(By.XPATH, const.AVATAR)
            notification.set("LOGIN SUCCESSFULLY")
            is_logged_in.set(True)
            if used_cookies.get():
                export_cookies(driver)
        except:
            handle_verification_pin(driver, notification)
            sleep(2)
            handle_captcha(driver, notification)
            sleep(2)
            handle_verification_phone(driver, notification)
            sleep(2)
            notification.set("LOGIN SUCCESSFULLY")
            is_logged_in.set(True)
            if used_cookies.get():
                export_cookies(driver)
    except:
        notification.set("LOGIN FAILED")
        is_logged_in.set(False)


# MAIN TASKS.
def run_task(driver: WebDriver, data: list[dict], notification: StringVar) -> None:
    for index, datum in enumerate(data):
        # CONTINUE TO NEXT RECORD.
        if not get_link(driver, datum["LINKEDIN_LINK"]):
            continue
        # RUN TASK.
        send_connect(driver, data, index)
        send_message(driver, data, index, datum)
    # EXPORT DATA.
    notification.set("TASK COMPLETED")
    export_excel(data)


def send_connect(driver: WebDriver, data: list[dict], index: int) -> None:
    # CHECK STATUS.
    if check_status(data, index, const.CASE_SUCCESS):
        return

    try:
        CONDITION = EC.presence_of_element_located((By.XPATH, const.BUTTON_CONNECT))
        WebDriverWait(driver, 15).until(CONDITION)

        button = driver.find_element(By.XPATH, const.BUTTON_CONNECT)
        status = button.get_attribute("aria-label")
        if "Invite" in status:
            # CLICK BUTTON.
            button.click()
            sleep(2)
            # CONFIRM ACTION.
            driver.find_element(By.XPATH, const.BUTTON_SUBMIT_CONNECT).click()
            sleep(2)
            # CHECK STATUS.
            status = button.get_attribute("aria-label")
            states = const.CASE_PENDING if "Pending" in status else const.CASE_CONNECT
            update_state(data, index, states)
        elif "Pending" in status:
            update_state(data, index, const.CASE_PENDING)
    except:
        try:
            CONDITION = EC.presence_of_element_located((By.XPATH, const.BUTTON_MESSAGE))
            WebDriverWait(driver, 15).until(CONDITION)

            button = driver.find_element(By.XPATH, const.BUTTON_MESSAGE)
            status = button.get_attribute("aria-label")
            if "Message" in status:
                update_state(data, index, const.CASE_MESSAGE)
        except:
            update_state(data, index, const.CASE_CONNECT)


def send_message(driver: WebDriver, data: list[dict], index: int, datum: dict) -> None:
    # CHECK STATUS.
    if not check_status(data, index, const.CASE_MESSAGE):
        return

    try:
        # GET DATA OF PROFILE.
        name, message = datum["NAME"], datum["MESSAGE"]
        message = message.replace("{{name}}", name)
        attachment = datum["ATTACHMENT"]

        CONDITION = EC.presence_of_element_located((By.XPATH, const.BUTTON_MESSAGE))
        WebDriverWait(driver, 15).until(CONDITION)
        # CLICK BUTTON.
        driver.find_element(By.XPATH, const.BUTTON_MESSAGE).click()
        sleep(2)
        # TYPE MESSAGE.
        textbox = driver.find_element(By.XPATH, const.FIELD_MESSAGE)
        textbox.send_keys(Keys.CONTROL + "a")
        textbox.send_keys(Keys.DELETE)
        sleep(2)
        textbox.send_keys(message)
        sleep(2)
        # ATTACH DATA.
        if attachment:
            rel_path = path.join("resources", "attachments", attachment)
            abs_path = path.abspath(rel_path)
            attachbox = driver.find_element(By.XPATH, const.FIELD_ATTACHMENT)
            attachbox.send_keys(abs_path)
            sleep(2)
        # SEND MESSAGE.
        driver.find_element(By.XPATH, const.BUTTON_SUBMIT_MESSAGE).click()

        update_state(data, index, const.CASE_SUCCESS)
    except:
        pass
