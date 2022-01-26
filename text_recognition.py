import easyocr
import os


def text_rec(file_path):
    reader = easyocr.Reader(['ru', 'en', 'uk'])
    result = reader.readtext(file_path, detail=0, paragraph=True)
    os.remove(file_path)
    return result
