from .nlp import nlp
from .matchers import get_value_matcher, get_product_matcher
from .extractors import extract_value, extract_product


def interpretar_mensagem(text: str) -> dict:
    doc = nlp(text)
    # Value
    matcher_value = get_value_matcher()
    matches_value = matcher_value(doc)
    value = extract_value(matches_value, doc)

    # Product
    matcher_product = get_product_matcher()
    matches_product = matcher_product(doc)
    product = extract_product(matches_product, doc)

    return {
        "value": value,
        "product": product
        # "tipo_operacao": ...,  # ex: venda ou compra
        # "product": ...
    }
