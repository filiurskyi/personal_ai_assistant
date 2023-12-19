import re


def filter_text(text):
    filtered_text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    filtered_text = re.sub(r"\s+", " ", filtered_text)
    return filtered_text
