from spacy.matcher import Matcher
from .nlp import nlp

def get_valor_matcher():
    matcher = Matcher(nlp.vocab)

    padrao_reais_centavos = [
        {"LIKE_NUM": True}, {"LOWER": "reais"}, {"LOWER": "e"},
        {"LIKE_NUM": True}, {"LOWER": "centavos"}
    ]
    padrao_com_simbolo = [{"TEXT": {"REGEX": r"(?i)^r\$"}}, {"LIKE_NUM": True}]
    padrao_reais = [{"LIKE_NUM": True}, {"LOWER": "reais"}]
    padrao_centavos = [{"LIKE_NUM": True}, {"LOWER": "centavos"}]

    matcher.add("VALOR", [padrao_reais_centavos, padrao_com_simbolo, padrao_reais, padrao_centavos])
    return matcher
