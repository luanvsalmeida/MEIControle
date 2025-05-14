from .nlp import nlp
from .matchers import get_valor_matcher
from .exctrators import extrair_valor

def interpretar_mensagem(texto: str) -> dict:
    doc = nlp(texto)

    matcher_valor = get_valor_matcher()
    matches_valor = matcher_valor(doc)

    valor = extrair_valor(matches_valor, doc)

    return {
        "valor": valor,
        # "tipo_operacao": ...,  # ex: venda ou compra
        # "produto": ...
    }
