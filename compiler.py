from quranParser import compileQuran
from translations.translationFormatting import load_translations
import json

def recomplieQuran(isJson=True):
    translations_data = load_translations()
    compiledquran = compileQuran(translations_data)
    if isJson:
        with open('compiledQuran.json', 'w', encoding='utf-8') as f:
            json.dump(compiledquran, f, ensure_ascii=False, indent=4)
    return compiledquran
    