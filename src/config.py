import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")
SHEET_TAB_NAME = os.environ.get("SHEET_TAB_NAME", "Movimentos")

DB_PATH = "data/seen.sqlite3"

# Cada item gera uma URL de RSS do Google News.
# when:7d limita ao período da última semana.
SEARCH_QUERIES = [
    {
        "label": "pt-BR",
        "hl": "pt-BR",
        "gl": "BR",
        "ceid": "BR:pt",
        "terms": [
            '("CMO" OR "Chief Marketing Officer" OR "diretor de marketing" OR "diretora de marketing" OR "VP de marketing") (nomeado OR nomeada OR assume OR contratado OR contratada OR substitui) when:7d',
        ],
    },
    {
        "label": "en-US",
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en",
        "terms": [
            '("CMO" OR "Chief Marketing Officer" OR "VP of Marketing" OR "Head of Marketing") (joins OR appointed OR named OR hires OR promoted) when:7d',
        ],
    },
]

CLASSIFY_SYSTEM_PROMPT = """Você é um classificador de notícias de negócios. Sua única tarefa é decidir se uma notícia trata de
MUDANÇA DE LIDERANÇA EM MARKETING (contratação, promoção, saída, nomeação) em uma empresa média ou grande.

Responda apenas "SIM" ou "NAO".

Responda SIM somente se a notícia for sobre uma PESSOA específica assumindo, deixando ou sendo promovida a um cargo de liderança
de marketing (CMO, Diretor de Marketing, VP de Marketing, Head of Marketing, etc.) em uma empresa de porte médio ou grande.

Responda NAO para:
- Notícias sobre campanhas publicitárias, lançamentos de produto, patrocínios
- Marketing genérico, tendências de mercado, conteúdo educacional sobre marketing
- Empresas claramente pequenas, startups muito iniciais, ou pessoas físicas sem vínculo corporativo claro
- Notícias que apenas citam o cargo de passagem, sem ser o tema central
"""

EXTRACT_SYSTEM_PROMPT = """Extraia as informações da notícia de mudança de liderança em marketing abaixo e retorne APENAS um JSON válido
com exatamente estas chaves: pessoa, empresa, cargo, pais, tipo_movimento, resumo, porte_empresa.

- tipo_movimento: um de "contratação", "promoção", "saída", "outro"
- porte_empresa: um de "médio", "grande", "indeterminado"
- resumo: no máximo 3 linhas, em português, resumindo o fato
- pais: país da empresa, se identificável, senão "indeterminado"

Não inclua texto fora do JSON.
"""
