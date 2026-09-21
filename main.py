from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from compiler import recomplieQuran
from translations.encryptionLogic import compress_files, decompressfile
from functools import lru_cache
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_compiled_quran():
    return recomplieQuran()

def format_response(data):
    return JSONResponse(
        content=data,
        media_type="application/json",
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Quran Parser API"}

@app.get("/quran")
def get_quran():
    with open('compiledQuran.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
@app.get("/quran/translations")
def ls_translations():
    directory = 'translations/data/Compressed/'
    translations = []
    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            parts = filename[:-4].split('.')
            if len(parts) == 2:
                language, author = parts
                translations.append({
                    "language": language,
                    "author": author
                })
    return format_response(translations)

@app.get("/quran/translations/{language}/{author}")
def get_translation(language: str, author: str):
    file = f'{language}.{author}'
    try:
        decompressfile(f'translations/data/Compressed/{file}.zip')
        compiled_quran = load_compiled_quran()
        data = []
        for surah_id, surah in compiled_quran["data"].items():
            verses = []
            for verse in surah["verses"].values():
                for t in verse["Translations"]:
                    if t["language"] == language and t["author"] == author:
                        verses.append({
                            "number": verse["number"],
                            "data": {
                                "language": t["language"],
                                "author": t["author"],
                                "translation": t["translation"],
                                "base": False
                            }
                        })

                        break 
            data.append({
                surah_id: {
                    "name": surah["name"],
                    "nameAr": surah["nameAr"],
                    "nameEng": surah["nameEng"],
                    "verses": verses
                }
            })
        compress_files(f'translations/data/{file}')
        return format_response(data)
    
    except FileNotFoundError:
        return JSONResponse(
            content={"error": "Translation not found"},
            status_code=404
        ) 

@app.get("/quran/{surah}")
def get_surah(surah: int):
    compiled_quran = load_compiled_quran()
    try:
        surah_data = compiled_quran["data"][surah]
        return format_response(surah_data)
    
    except KeyError:
        return JSONResponse(
            content={"error": "Surah not found"},
            status_code=404
        )

@app.get("/quran/{surah}/{ayah}")
def get_verse(surah: int, ayah: int):
    compiled_quran = load_compiled_quran()
    try:
        verse_data = compiled_quran["data"][surah]["verses"][ayah]
        return format_response(verse_data)
    
    except KeyError:
        return JSONResponse(
            content={"error": "Verse not found"},
            status_code=404
        )

@app.get("/quran/surahs/names/{start}/{end}")
def get_surah_names(start: int, end: int):
    compiled_quran = load_compiled_quran()
    data = {}
    for surah_id in range(start, end + 1):
        try:
            surah_name = compiled_quran["data"][surah_id]
            data[surah_id] = {
                "name:": surah_name["name"],
                "nameAr": surah_name["nameAr"],
                "nameEng": surah_name["nameEng"],
                "numberOfVerses": surah_name["numberOfVerses"],
                "Origin": surah_name["Origin"],
                "juz": surah_name["juz"],
                "size": len(surah_name["verses"])
            }
        except KeyError:
            continue  
    return format_response(data)