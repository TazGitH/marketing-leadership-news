import urllib.parse
import feedparser

from config import COUNTRY_PRESETS, DEFAULT_COUNTRY


def build_rss_url(term: str, hl: str, gl: str, ceid: str) -> str:
    query = urllib.parse.quote(term)
    return f"https://news.google.com/rss/search?q={query}&hl={hl}&gl={gl}&ceid={ceid}"


def fetch_all_items(paises: list[str], dias_busca: int):
    items = []
    for sigla in paises:
        preset = COUNTRY_PRESETS.get(sigla)
        if preset is None:
            print(f"Aviso: país '{sigla}' não tem preset configurado, ignorando (use {DEFAULT_COUNTRY} ou adicione em config.py).")
            continue
        for term in preset["terms"]:
            term_com_periodo = f"{term} when:{dias_busca}d"
            url = build_rss_url(term_com_periodo, preset["hl"], preset["gl"], preset["ceid"])
            feed = feedparser.parse(url)
            for entry in feed.entries:
                items.append(
                    {
                        "title": entry.get("title", "").strip(),
                        "link": entry.get("link", "").strip(),
                        "published": entry.get("published", ""),
                        "source": entry.get("source", {}).get("title", "") if hasattr(entry, "source") else "",
                        "summary_raw": entry.get("summary", ""),
                        "lang": sigla,
                    }
                )
    return items
