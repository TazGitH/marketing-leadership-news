from fetch_news import fetch_all_items
from dedupe import filter_unseen, mark_as_seen
from classify import is_relevant, extract_details
from sheets_writer import append_rows


def main():
    print("Buscando notícias...")
    items = fetch_all_items()
    print(f"{len(items)} itens encontrados nas buscas.")

    unseen = filter_unseen(items)
    print(f"{len(unseen)} itens novos após deduplicação.")

    relevant_rows = []
    for item in unseen:
        try:
            if is_relevant(item):
                details = extract_details(item)
                details["link"] = item["link"]
                details["source"] = item.get("source") or item["title"].split(" - ")[-1]
                relevant_rows.append(details)
                print(f"RELEVANTE: {item['title']}")
            else:
                print(f"descartado: {item['title']}")
        except Exception as exc:
            print(f"erro ao processar '{item['title']}': {exc}")

    append_rows(relevant_rows)
    print(f"{len(relevant_rows)} linhas gravadas no Google Sheets.")

    mark_as_seen(unseen)
    print("Banco de dedup atualizado.")


if __name__ == "__main__":
    main()
