import datetime
import json

import gspread
from dateutil import parser as date_parser
from google.oauth2.service_account import Credentials

from config import (
    CLASSIFY_SYSTEM_PROMPT,
    CONFIG_TAB_NAME,
    DEFAULT_COUNTRY,
    DEFAULT_DAYS_BACK,
    GOOGLE_SERVICE_ACCOUNT_JSON,
    GOOGLE_SHEET_ID,
)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

CAMPO_PAIS = "País (gl)"
CAMPO_DATA_INICIAL = "Data de busca inicial (opcional, formato DD/MM/AAAA)"
CAMPO_PALAVRAS_CHAVE = "Palavras-chave de busca (opcional)"
CAMPO_PROMPT_CLASSIFICACAO = "Critério de relevância para a IA (opcional)"

DEFAULT_ROWS = [
    ["Campo", "Valor", "Observação"],
    [CAMPO_PAIS, DEFAULT_COUNTRY, "Sigla do país. Para mais de um, separe por vírgula. Ex: BR,US"],
    [
        CAMPO_DATA_INICIAL,
        "",
        "Deixe vazio para buscar sempre os últimos 7 dias. Preencha só para uma carga inicial maior; depois limpe este campo.",
    ],
    [
        CAMPO_PALAVRAS_CHAVE,
        "",
        'Deixe vazio para usar os termos padrão do sistema. Se preencher, use a sintaxe do Google Notícias, ex: ("CMO" OR "Diretor de Marketing") (nomeado OR contratado). Substitui os termos padrão para todos os países selecionados.',
    ],
    [
        CAMPO_PROMPT_CLASSIFICACAO,
        "",
        "Deixe vazio para usar o critério padrão do sistema. Se preencher, escreva em texto livre o critério que a IA deve usar para aceitar ou rejeitar uma notícia.",
    ],
]


def _get_client():
    info = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return gspread.authorize(creds)


def _get_or_create_worksheet():
    client = _get_client()
    sheet = client.open_by_key(GOOGLE_SHEET_ID)
    try:
        worksheet = sheet.worksheet(CONFIG_TAB_NAME)
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=CONFIG_TAB_NAME, rows=10, cols=3)
        worksheet.update("A1", DEFAULT_ROWS)
    return worksheet


def _read_field(worksheet, campo: str) -> str:
    values = worksheet.get_all_values()
    for row in values[1:]:
        if len(row) >= 2 and row[0].strip() == campo:
            return row[1].strip()
    return ""


def get_settings() -> dict:
    worksheet = _get_or_create_worksheet()

    paises_raw = _read_field(worksheet, CAMPO_PAIS) or DEFAULT_COUNTRY
    paises = [p.strip().upper() for p in paises_raw.split(",") if p.strip()]

    data_inicial_raw = _read_field(worksheet, CAMPO_DATA_INICIAL)
    dias_busca = DEFAULT_DAYS_BACK
    if data_inicial_raw:
        try:
            data_inicial = date_parser.parse(data_inicial_raw, dayfirst=True).date()
            hoje = datetime.date.today()
            dias_busca = max((hoje - data_inicial).days, 1)
        except (ValueError, OverflowError):
            dias_busca = DEFAULT_DAYS_BACK

    palavras_chave = _read_field(worksheet, CAMPO_PALAVRAS_CHAVE) or None

    prompt_classificacao = _read_field(worksheet, CAMPO_PROMPT_CLASSIFICACAO) or CLASSIFY_SYSTEM_PROMPT

    return {
        "paises": paises,
        "dias_busca": dias_busca,
        "palavras_chave": palavras_chave,
        "prompt_classificacao": prompt_classificacao,
    }
