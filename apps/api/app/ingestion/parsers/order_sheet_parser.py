def parse_order_sheet(text: str) -> dict:
    return {"title": "Unknown Order Sheet", "text": text, "metadata": {"parser": "order_sheet_parser_v1"}}
