from transformers import BertTokenizer, BertModel
import logging
import numpy as np

MODEL_NAME = "bert-base-uncased"


def site_to_matrix(text: str) -> list[list[int]]:
    """Uses BERT-Emo to generate a relative emotional makeup of website"""
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertModel.from_pretrained(MODEL_NAME)
    input = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    output = model(**input)
    return output.pooler_output.detach().numpy().tolist()


def find_site_similarity(site_1: list[list[str]], site_2: list[list[str]]) -> int:
    """Returns a score from 0 to 1 of how similar the site's matrices are"""
    first = np.array(site_1)
    second = np.array(site_2)
    difference = first - second
    diff = np.vectorize(lambda el: np.abs(el))(difference)
    dims = diff.shape[0]*diff.shape[1]
    return 1 - np.sum(diff)/dims
