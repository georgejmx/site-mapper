from transformers import BertTokenizer, BertModel
import logging

MODEL_NAME = "bert-base-uncased"


def site_to_matrix(text: str) -> list[list[int]]:
    """Uses BERT-Emo to generate a relative emotional makeup of website"""
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertModel.from_pretrained(MODEL_NAME)
    input = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    output = model(**input)
    return output.pooler_output.detach().numpy().tolist()
