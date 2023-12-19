import re
from PIL import Image
import pytesseract

LANGS = ["rus", "ukr", "eng"]


def filter_text(text):
    filtered_text = re.sub(r"[^a-zA-Z0-9а-яА-Я.,:;()!?*+=\-\s]", "", text)
    filtered_text = re.sub(r"\s+", " ", filtered_text)
    return filtered_text


def ocr_image(image: Image):
    text = pytesseract.image_to_string(image, lang="rus+eng+ukr")
    print(text)
    filtered_text = filter_text(text)
    return filtered_text
