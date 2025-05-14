from spacy.matcher import Matcher
import json
from spacy.matcher import Matcher
from pathlib import Path
from .nlp import nlp

def get_value_matcher():
    matcher = Matcher(nlp.vocab)

    pattern_reais_centavos = [
        {"LIKE_NUM": True}, {"LOWER": "reais"}, {"LOWER": "e"},
        {"LIKE_NUM": True}, {"LOWER": "centavos"}
    ]
    pattern_simbol = [{"TEXT": {"REGEX": r"(?i)^r\$"}}, {"LIKE_NUM": True}]
    pattern_reais = [{"LIKE_NUM": True}, {"LOWER": "reais"}]
    pattern_centavos = [{"LIKE_NUM": True}, {"LOWER": "centavos"}]

    matcher.add("VALOR", [pattern_reais_centavos, pattern_simbol, pattern_reais, pattern_centavos])
    return matcher

def get_product_matcher():
    matcher = Matcher(nlp.vocab)

    # path to the JSON file with products labels
    data_path = Path(__file__).resolve().parent.parent.parent / "data" / "classificationRules.json"
    with open(data_path, "r", encoding="utf-8") as f:
        produtos = json.load(f)

    for item in produtos:
        label = item["label"]
        # Pattern with one or more words 
        label_tokens = label.lower().split()
        pattern = [{"LOWER": token} for token in label_tokens]
        matcher.add("PRODUTO", [pattern])

    return matcher

def get_operation_matcher():    # inflow/outflow/chart/previews
    matcher = Matcher(nlp.voc)
    # todo...
    return matcher
