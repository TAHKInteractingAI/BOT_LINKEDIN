from os import path
import gspread
from gspread.worksheet import Worksheet
from oauth2client.service_account import ServiceAccountCredentials

# CONSTANTS.
SHEET_NAME = "LINKEDIN_TOOL_BOT"
CREDENTAILS_PATH = path.join("resources", "privates", "credentials.json")
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


# FEATURES.
def get_worksheet() -> Worksheet:
    # GET CREDENTAILS DATA.
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTAILS_PATH, SCOPES
    )
    # CREATE ACCESS CLIENT.
    client = gspread.authorize(credentials)
    # GET DATA FROM SHEET.
    spreadsheet = client.open(SHEET_NAME)
    return spreadsheet.get_worksheet(0)


def import_gsheet() -> list[dict]:
    worksheet = get_worksheet()
    return worksheet.get_all_records()


def export_gsheet(data: list[dict]) -> None:
    worksheet = get_worksheet()
    for index, datum in enumerate(data, start=2):
        row = [list(datum.values())]
        worksheet.update(row, f"A{index}:G{index}")
