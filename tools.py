import time
import pandas as pd
from customtkinter import StringVar, BooleanVar
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import constants as const


# SUPPORT FUNCTION.
def get_link(driver: WebDriver, link: str) -> bool:
    """Go to profile page."""
    try:
        driver.get(link)
        time.sleep(5)
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


def import_excel(data: list[dict], file_name=const.PATH_EXCEL_DATA) -> None:
    # GET DATA FROM EXCEL FILE.
    df = pd.read_excel(file_name, sheet_name="Sheet1")
    # FORMAT DATA TO PYTHON OBJECT.
    data.clear()
    for index in range(df.shape[0]):
        data.append({key: value[index] for key, value in df.to_dict().items()})


def export_excel(data: list[dict], file_name=const.PATH_EXCEL_DATA) -> None:
    with pd.ExcelWriter(file_name, engine="openpyxl", mode="w") as writer:
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name="Sheet1", index=False)


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


def login(
    driver: WebDriver,
    notification: StringVar,
    is_logged_in: BooleanVar,
    username: str,
    password: str,
) -> None:
    try:
        # GO TO LOGIN PAGE.
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        # ENTER USERNAME & PASSWORD.
        driver.find_element(By.XPATH, const.FIELD_USERNAME).send_keys(username)
        driver.find_element(By.XPATH, const.FIELD_PASSWORD).send_keys(password)
        time.sleep(2)
        # CLICK LOGIN BUTTON.
        driver.find_element(By.XPATH, const.BUTTON_SUBMIT_LOGIN).click()
        time.sleep(5)
        # CHECK LOGIN.
        try:
            driver.find_element(By.XPATH, const.AVATAR)
            notification.set("LOGIN SUCCESSFULLY")
            is_logged_in.set(True)
        except:
            # HANDLE ERROR.
            handle_verification_pin(driver, notification)
            time.sleep(2)
            handle_captcha(driver, notification)
            time.sleep(2)
            handle_verification_phone(driver, notification)
            time.sleep(2)
            notification.set("LOGIN SUCCESSFULLY")
            is_logged_in.set(True)
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
        send_message(driver, data, index)
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
            time.sleep(2)
            # CONFIRM ACTION.
            driver.find_element(By.XPATH, const.BUTTON_SUBMIT_CONNECT).click()
            time.sleep(2)
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


def send_message(driver: WebDriver, data: list[dict], index: int) -> None:
    # CHECK STATUS.
    if not check_status(data, index, const.CASE_MESSAGE):
        return
    # GET NAME & MESSAGE OF PROFILE.
    name, message = data[index]["NAME"], data[index]["MESSAGE"]
    message: str = message.replace("{{name}}", name)

    try:
        CONDITION = EC.presence_of_element_located((By.XPATH, const.BUTTON_MESSAGE))
        WebDriverWait(driver, 15).until(CONDITION)
        # CLICK BUTTON.
        driver.find_element(By.XPATH, const.BUTTON_MESSAGE).click()
        time.sleep(2)
        # TYPE MESSAGE.
        textbox = driver.find_element(By.XPATH, const.FIELD_MESSAGE)
        textbox.send_keys(Keys.CONTROL + "a")
        textbox.send_keys(Keys.DELETE)
        textbox.send_keys(message)
        # SEND MESSAGE.
        driver.find_element(By.XPATH, const.BUTTON_SUBMIT_MESSAGE).click()

        update_state(data, index, const.CASE_SUCCESS)
    except:
        pass
