import easyocr
import os


def text_rec(file_path):
    try:
        reader = easyocr.Reader(['ru', 'en', 'uk'])
        co = reader.readtext(file_path, detail=0, paragraph=True)
        result = ''
        for i in co:
            result += f'\n{i}'
        os.remove(file_path)
    except:
        result = "Не удалось распознать =("
    return result
