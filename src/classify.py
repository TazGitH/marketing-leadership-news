import json
import anthropic

from config import ANTHROPIC_API_KEY, CLASSIFY_SYSTEM_PROMPT, EXTRACT_SYSTEM_PROMPT

MODEL = "claude-haiku-4-5-20251001"

_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def is_relevant(item: dict) -> bool:
    text = f"Título: {item['title']}\nResumo da fonte: {item.get('summary_raw', '')}"
    response = _client.messages.create(
        model=MODEL,
        max_tokens=10,
        system=CLASSIFY_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text}],
    )
    answer = response.content[0].text.strip().upper()
    return answer.startswith("SIM")


def extract_details(item: dict) -> dict:
    text = f"Título: {item['title']}\nResumo da fonte: {item.get('summary_raw', '')}\nLink: {item['link']}"
    response = _client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=EXTRACT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text}],
    )
    raw = response.content[0].text.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        return json.loads(raw[start : end + 1])
