from .nlp import nlp
from .matchers import get_value_matcher, get_product_matcher, get_operation_matcher
from .extractors import extract_value, extract_product, extract_operation

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

    # Operation
    matcher_op = get_operation_matcher()
    matches_op = matcher_op(doc)
    operation = extract_operation(matches_op, doc)

    if isinstance(operation, dict) and operation.get("type") == "save":
        return {
            "operation": "save",
            "label": operation.get("label")
        }

    return {
        "value": value,
        "product": product,
        "operation": operation
    }

