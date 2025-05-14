from .nlp import nlp

def extract_value(matches, doc):
    spans_usados = set()
    valor_total = 0.0

    for _, start, end in matches:
        if any(i in spans_usados for i in range(start, end)):
            continue

        span = doc[start:end]
        tokens = [t.text.lower() for t in span]

        try:
            if "reais" in tokens and "centavos" in tokens and "e" in tokens:
                reais = float(span[0].text.replace(",", "."))
                centavos = float(span[3].text.replace(",", ".")) / 100
                valor_total += reais + centavos

            elif len(tokens) == 2 and tokens[1] == "reais":
                valor_total += float(span[0].text.replace(",", "."))

            elif len(tokens) == 2 and tokens[1] == "centavos":
                valor_total += float(span[0].text.replace(",", ".")) / 100

            elif len(tokens) == 2 and "r$" in tokens[0]:
                valor_total += float(span[1].text.replace(",", "."))

            spans_usados.update(range(start, end))
        except:
            continue

    return round(valor_total, 2) if valor_total else None

def extract_product(matches, doc):
    products = []

    for match_id, start, end in matches:
        span = doc[start:end]
        products.append(span.text)

    return products[0] if products else None

def extract_operation(matches, doc):
    op_priority = {
        "OP_INFLOW": "inflow",
        "OP_OUTFLOW": "outflow",
        "OP_REPORT": "report",
        "OP_FORECAST": "forecast"
    }

    for match_id, _, _ in matches:
        op_type = nlp.vocab.strings[match_id]
        if op_type in op_priority:
            return op_priority[op_type]

    return None
