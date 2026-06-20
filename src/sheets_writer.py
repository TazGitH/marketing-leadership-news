import datetime
import json

import gspread
from google.oauth2.service_account import Credentials

from config import GOOGLE_SERVICE_ACCOUNT_JSON, GOOGLE_SHEET_ID, SHEET_TAB_NAME

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

HEADER = [
    "Data",
    "Empresa",
    "Pessoa",
    "Cargo",
    "Tipo de movimento",
    "Pais",
    "Fonte",
    "Link",
    "Resumo",
    "Porte da empresa",
    "Status",
]


def _get_worksheet():
    info = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(GOOGLE_SHEET_ID)
    try:
        worksheet = sheet.worksheet(SHEET_TAB_NAME)
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=SHEET_TAB_NAME, rows=1000, cols=len(HEADER))
        worksheet.append_row(HEADER)
    if worksheet.row_values(1) != HEADER:
        worksheet.update("A1", [HEADER])
    return worksheet


def append_rows(rows: list[dict]):
    if not rows:
        return
    worksheet = _get_worksheet()
    today = datetime.date.today().isoformat()
    values = []
    for row in rows:
        values.append(
            [
                today,
                row.get("empresa", ""),
                row.get("pessoa", ""),
                row.get("cargo", ""),
                row.get("tipo_movimento", ""),
                row.get("pais", ""),
                row.get("source", ""),
                row.get("link", ""),
                row.get("resumo", ""),
                row.get("porte_empresa", ""),
                "novo",
            ]
        )
    worksheet.append_rows(values, value_input_option="USER_ENTERED")
