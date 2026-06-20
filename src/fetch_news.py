import urllib.parse
import feedparser

from config import SEARCH_QUERIES


def build_rss_url(term: str, hl: str, gl: str, ceid: str) -> str:
    query = urllib.parse.quote(term)
    return f"https://news.google.com/rss/search?q={query}&hl={hl}&gl={gl}&ceid={ceid}"


def fetch_all_items():
    items = []
    for query_set in SEARCH_QUERIES:
        for term in query_set["terms"]:
            url = build_rss_url(term, query_set["hl"], query_set["gl"], query_set["ceid"])
            feed = feedparser.parse(url)
            for entry in feed.entries:
                items.append(
                    {
                        "title": entry.get("title", "").strip(),
                        "link": entry.get("link", "").strip(),
                        "published": entry.get("published", ""),
                        "source": entry.get("source", {}).get("title", "") if hasattr(entry, "source") else "",
                        "summary_raw": entry.get("summary", ""),
                        "lang": query_set["label"],
                    }
                )
    return items
