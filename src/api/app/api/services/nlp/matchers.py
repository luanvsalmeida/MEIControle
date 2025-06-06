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

def get_operation_matcher():
    matcher = Matcher(nlp.vocab)

    inflow_terms = ["venda", "registrar venda", "registro de venda", "vendi", "recebi", "entrada"]
    outflow_terms = ["compra", "registrar compra", "registro de compra", "comprei", "gastei", "saída", "saida"]
    report_terms = ["relatório", "relatorio", "resumo", "extrato", "gráfico", "grafico"]
    forecast_terms = ["previsão", "previsao", "prever", "projeção", "projeçao", "projecao", "estimativa"]
    product_terms = [["registrar", "produto"], ["cadastrar", "produto"]]

    for term in inflow_terms:
        matcher.add("OP_INFLOW", [[{"LOWER": term}]])
    for term in outflow_terms:
        matcher.add("OP_OUTFLOW", [[{"LOWER": term}]])
    for term in report_terms:
        matcher.add("OP_REPORT", [[{"LOWER": term}]])
    for term in forecast_terms:
        matcher.add("OP_FORECAST", [[{"LOWER": term}]])
    for term_pair in product_terms:
        matcher.add("OP_SAVE_PRODUCT", [[
            {"LOWER": term_pair[0]}, {"LOWER": term_pair[1]}
        ]])

    return matcher

