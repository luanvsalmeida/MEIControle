def extrair_valor(matches, doc):
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
