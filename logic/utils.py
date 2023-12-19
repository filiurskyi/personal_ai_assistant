import re
from PIL import Image
import pytesseract


def filter_text(text):
    filtered_text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    filtered_text = re.sub(r"\s+", " ", filtered_text)
    return filtered_text


def ocr_image(image: Image):
    custom_config = r'-l eng --psm 3'
    text = pytesseract.image_to_string(image, config=custom_config)
    return filter_text(text)
