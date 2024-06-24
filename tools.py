import time
import pandas as pd
from customtkinter import StringVar, BooleanVar
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# SUPPORT FUNCTION.
def get_link(driver: WebDriver, link: str) -> bool:
    """Go to profile page."""
    try:
        driver.get(link)
        time.sleep(5)
        return True
    except:
        return False


def update_state(data: list[dict], index: int, state: list[str]) -> None:
    """Update state after go to profile page."""
    data[index]["STATE_1"] = state[0]
    data[index]["STATE_2"] = state[1]
    data[index]["STATE_3"] = state[2]


def import_excel(data: list[dict], file_name="LINKEDIN_DATA.xlsx") -> None:
    """Import data from an excel file."""
    # GET DATA FROM EXCEL FILE.
    df = pd.read_excel(file_name, sheet_name="Sheet1")
    # FORMAT DATA TO PYTHON OBJECT.
    data.clear()
    for index in range(df.shape[0]):
        data.append({key: value[index] for key, value in df.to_dict().items()})


def export_excel(data: list[dict], file_name="LINKEDIN_DATA.xlsx") -> None:
    """Export data to an excel file."""
    with pd.ExcelWriter(file_name, engine="openpyxl", mode="w") as writer:
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name="Sheet1", index=False)


# MAIN FUNCTION.
def handle_verification_pin(driver: WebDriver, notification: StringVar) -> None:
    """Find PIN verfication & take 2 minutes to solve it."""
    FIELD = "input_verification_pin"
    CONDITION = EC.presence_of_element_located((By.CLASS_NAME, FIELD))
    try:
        WebDriverWait(driver, 10).until(CONDITION)
        notification.set("VERIFICATION PIN DETECTED!")
        WebDriverWait(driver, 120).until_not(CONDITION)
    except TimeoutException:
        notification.set("NO VERIFICATION PIN DETECTED!")


def handle_captcha(driver: WebDriver, notification: StringVar) -> None:
    """Find captcha verfication & take 2 minutes to solve it."""
    FIELD = "captcha-internal"
    CONDITION = EC.presence_of_element_located((By.ID, FIELD))
    try:
        WebDriverWait(driver, 10).until(CONDITION)
        notification.set("CAPTCHA DETECTED!")
        WebDriverWait(driver, 120).until_not(CONDITION)
    except TimeoutException:
        notification.set("NO CAPTCHA DETECTED!")


def handle_verification_phone(driver: WebDriver, notification: StringVar) -> None:
    """Find phone number verfication & take 2 minutes to solve it."""
    FIELD = "register-verification-phone-number"
    CONDITION = EC.presence_of_element_located((By.ID, FIELD))
    try:
        WebDriverWait(driver, 10).until(CONDITION)
        notification.set("PHONE VERIFICATION DETECTED!")
        WebDriverWait(driver, 120).until_not(CONDITION)
    except TimeoutException:
        notification.set("NO PHONE VERIFICATION DETECTED!")


def login(
    driver: WebDriver,
    notification: StringVar,
    is_logged_in: BooleanVar,
    username: str,
    password: str,
) -> None:
    """Login to LinkedIn."""
    USERNAME_FIELD = "/html/body/div[1]/main/div[2]/div[1]/form/div[1]/input"
    PASSWORD_FIELD = "/html/body/div[1]/main/div[2]/div[1]/form/div[2]/input"
    SUBMIT_BUTTON = "/html/body/div/main/div[2]/div[1]/form/div[3]/button"
    try:
        # GO TO LOGIN PAGE.
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        # ENTER USERNAME & PASSWORD.
        driver.find_element(By.XPATH, USERNAME_FIELD).send_keys(username)
        driver.find_element(By.XPATH, PASSWORD_FIELD).send_keys(password)
        time.sleep(2)
        # CLICK LOGIN BUTTON.
        driver.find_element(By.XPATH, SUBMIT_BUTTON).click()
        time.sleep(2)
        # HANDLE ERROR.
        handle_verification_pin(driver, notification)
        time.sleep(2)
        handle_captcha(driver, notification)
        time.sleep(2)
        handle_verification_phone(driver, notification)
        time.sleep(2)
        notification.set("LOGIN SUCCESSFULLY!")
        is_logged_in.set(True)
    except:
        notification.set("LOGIN FAILED!")
        is_logged_in.set(False)


def connect(driver: WebDriver, data: list[dict], notification: StringVar) -> None:
    """Connect to LinkedIn profiles."""
    SUCC_CASE = ["Pending", "Invite sent", "Message not sent"]
    FAIL_CASE = ["Not Connected", "Not Connected", "Message not sent"]
    BTN_CONNECT = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button"
    BTN_CONFIRM = "/html/body/div[3]/div/div/div[3]/button[2]"

    for index, datum in enumerate(data):
        # CONTINUE TO NEXT RECORD.
        if not get_link(driver, datum["LINKEDIN_LINK"]):
            continue
        # MAKE CONNECT.
        try:
            button = driver.find_element(By.XPATH, BTN_CONNECT)
            status = button.get_attribute("aria-label")
            # CHECK CASE.
            if "Invite" in status:
                try:
                    # SEND CONNECT.
                    button.click()
                    time.sleep(2)
                    # CONFIRM SEND CONNECT.
                    btn_confirm = driver.find_element(By.XPATH, BTN_CONFIRM)
                    btn_confirm.click()
                    time.sleep(2)
                    # STATUS CHANGED TO PENDING.
                    status = button.get_attribute("aria-label")
                    if "Pending" in status:
                        update_state(data, index, SUCC_CASE)
                except NoSuchElementException:
                    update_state(data, index, FAIL_CASE)
            elif "Pending" in status:
                update_state(data, index, SUCC_CASE)
            else:
                update_state(data, index, FAIL_CASE)
        except NoSuchElementException:
            update_state(data, index, FAIL_CASE)
    # EXPORT DATA.
    notification.set("CONNECT SUCCESSFULLY!")
    export_excel(data)
