# PATH.
PATH_CHROME_DRIVER = "resources/chromedriver.exe"
PATH_EXCEL_DATA = "resources/data.xlsx"

# UI CONSTANTS.
FONT_B = ("monospace", 14, "bold")
FONT_I = ("monospace", 14, "italic")

# LOGIN.
FIELD_USERNAME = "/html/body/div[1]/main/div[2]/div[1]/form/div[1]/input"
FIELD_PASSWORD = "/html/body/div[1]/main/div[2]/div[1]/form/div[2]/input"
BUTTON_SUBMIT_LOGIN = "/html/body/div/main/div[2]/div[1]/form/div[3]/button"
AVATAR = "/html/body/div[5]/header/div/nav/ul/li[6]/div/button"
CLASS_PIN_VERIFICATION = "input_verification_pin"
ID_CAPTCHA = "captcha-internal"
ID_PHONE_VERIFICATION = "register-verification-phone-number"

# STATES: CONNECT -> PENDING -> MESSAGE -> SUCCESS.
CASE_CONNECT = ("Not Connected", "Not Connected", "Message not sent")
CASE_PENDING = ("Pending", "Invite sent", "Message not sent")
CASE_MESSAGE = ("Connected", "Connected", "Message not sent")
CASE_SUCCESS = ("Connected", "Connected", "Message sent")

# SEND CONNECT.
BUTTON_CONNECT = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button"
BUTTON_SUBMIT_CONNECT = "/html/body/div[3]/div/div/div[3]/button[2]"

# SEND MESSAGE.
BUTTON_MESSAGE = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[1]/button"
BUTTON_SUBMIT_MESSAGE = "/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/form/footer/div[2]/div[1]/button"
FIELD_MESSAGE = "/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/form/div[2]/div[1]/div/div[1]"
FIELD_ATTACHMENT = "/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/form/footer/div[1]/div[2]/input[3]"
