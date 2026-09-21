import json

#---- Load necessary files

with open('translations/data/output.json', 'r', encoding='utf-8') as f:
    translations_data = json.load(f)

print("Files loaded successfully.")

#---- Processing and compiling Quran data

compiledquran = {}
bismillah = "بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ"
translationDict = {}

#---- Process translations
def processTranslations(content):
    translations = {}
    for t in content:
        lang = t["language"]
        author = t["author"]
        verse_list = t["verses"]
        for v in verse_list:
            if len(v) < 3 or not v[0].strip() or not v[1].strip():
                print("Bad verse data:", v)
                continue
            key = f"{v[0]}:{v[1]}"
            if key not in translations:
                translations[key] = []
            translations[key].append({
                "language": lang,
                "author": author,
                "translation": v[2].strip(),
                "base": True
            })
    return translations

#---- Process plain verses
def processplainVerses(content):
    count = 0
    verses = content.split('\n')
    processed_verses = []
    for verse in verses:
        verse = verse.strip()
        if verse and not verse.startswith(bismillah):
            processed_verses.append(verse)
        elif verse.startswith(bismillah):
            if count == 0:
                processed_verses.append(verse)
                count += 1
                continue
            extraprocess = verse.split(bismillah)
            for i in extraprocess:
                i = i.strip()
                if i:
                    processed_verses.append(i)
        count += 1
    return processed_verses

#---- Add End Points for Surahs   
def addEndPoint(content, data):
    secondLayerProcessing = []
    content_index = 0 

    for d in data:
        if d == '':
            continue
        limit = data[str(d)]["verses"] 

        secondLayerProcessing.append(bismillah)

        for i in range(limit):
            if content_index < len(content):
                secondLayerProcessing.append(content[content_index])
                content_index += 1
            else:
                break  

        secondLayerProcessing.append("End")

    return secondLayerProcessing

#---- Parse Quran into structured format

def parseQuran(content, data, origin, sajada_data, translationDict):

    # Compile Surah Details
    def compileSurah(data, verses, index):

        isBismillah = index != 9

        surahDetails = {
            "name": data[str(index)]["name"],
            "nameAr": data[str(index)]["arabic"],
            "nameEng": data[str(index)]["english"],
            "numberOfVerses": data[str(index)]["verses"],
            "isBismillah": isBismillah,
            "Origin": "Makki" if origin[str(index)] == "1" else "Madani",
            "juz": data[str(index)]["Juz"],
            "verses": compileVerses(verses[1:], index),
        }
        return surahDetails
    
    # Translation Lookup
    def translationLookup(verseNo, surahNo):
        key = f"{surahNo}:{verseNo}"
        return translationDict.get(key, [])

    # Compile Verses
    def compileVerses(verses, index):
        newVerses = {}
        vNo = 1  # Start numbering at 1
        for v in verses:
            if v == "End":
                break
            deets = {
                "verse": v,
                "number": vNo,
                "isSajda": str(index) in sajada_data and vNo == sajada_data[str(index)]["verse"],
                "Translations": translationLookup(vNo, index),
            }
            newVerses[vNo] = deets
            vNo += 1
        return newVerses
    
    # Main Parsing Logic
    index = 1
    tempVerse = []
    res = {}
    for line in content:
        if line == "End":
            res[index] = compileSurah(data, tempVerse, index)
            index += 1
            tempVerse = []
        else:
            tempVerse.append(line)
    return {"data":res}

def compileQuran(translation_data):
    with open('quran-simple.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    with open('data/sajada-data.json', 'r', encoding='utf-8') as f:
        sajada_data = json.load(f)

    with open('data/originkey.json', 'r', encoding='utf-8') as f:
        origin = json.load(f)

    with open('data/quran-Meta.json', 'r', encoding='utf-8') as f:
        quran_data = json.load(f)
    
    translationDict = processTranslations(translation_data)
    processed_verses = processplainVerses(content)
    extra_processing = addEndPoint(processed_verses, quran_data)

    compiledquran = parseQuran(extra_processing, quran_data, origin, sajada_data, translationDict)
    return compiledquran

#---- Save compiled Quran data to JSON file

compiledquran = compileQuran(translations_data)

with open('compiledQuran.json', 'w', encoding='utf-8') as f:
    json.dump(compiledquran, f, ensure_ascii=False, indent=4)

