from os import path
from pandas import DataFrame, ExcelWriter, read_excel

# CONSTANTS.
CREDENTAILS_PATH = path.join("resources", "privates", "data.xlsx")


def import_excel() -> list[dict]:
    data = list()
    try:
        df = read_excel(CREDENTAILS_PATH, sheet_name="Sheet1")
        df = df.astype("object")
        df.fillna(value="", inplace=True)
        for index in range(df.shape[0]):
            data.append({key: value[index] for key, value in df.to_dict().items()})
    except:
        pass
    return data


def export_excel(data: list[dict]) -> None:
    with ExcelWriter(CREDENTAILS_PATH, engine="openpyxl", mode="w") as writer:
        DataFrame(data).to_excel(writer, sheet_name="Sheet1", index=False)
