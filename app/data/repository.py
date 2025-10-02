from pathlib import Path
import shutil
from fastapi import UploadFile
import pandas as pd

XLSX_FILE_PATH = Path("app_data") / "table.xlsx"
XLSX_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

def save_xlsx_file(file: UploadFile):
    with open(XLSX_FILE_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

def read_xlsx_file():
    if not XLSX_FILE_PATH.exists():
        return None
    return pd.read_excel(XLSX_FILE_PATH)