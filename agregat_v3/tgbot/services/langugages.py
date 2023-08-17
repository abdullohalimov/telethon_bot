import difflib
import re
from lingua import Language, LanguageDetectorBuilder
from tgbot.services.categories import get_categories
from tgbot.models.database import Keywords

def detect_cyrillic_language(text):
    # languages = [Language.TURKISH, Language.ENGLISH]
    detector = LanguageDetectorBuilder.from_all_languages_with_cyrillic_script().build()
    return detector.detect_language_of(text)


def get_language(message2, response_ru, response_cyrl, response_uz):
    # languages = [Language.TURKISH, Language.ENGLISH]
    detector = LanguageDetectorBuilder.from_all_languages().build()
    if detector.detect_language_of(message2) == Language.RUSSIAN:
        print("RUSSIAN LANGUAGEE")
        ctgrs = get_categories(response_ru, message2, 0.9)
        if ctgrs == " ":
            ctgrs = get_categories(response_ru, message2, 0.8)

    else:
        if detect_cyrillic_language(message2):
            print("CYRL LANGUAGEE")

            ctgrs = get_categories(response_cyrl, message2, 0.9)
            if ctgrs == " ":
                ctgrs = get_categories(response_cyrl, message2, 0.8)

        else:
            print("LATIN LANGUAGEE")

            ctgrs = get_categories(response_uz, message2, 0.9)
            if ctgrs == " ":
                ctgrs = get_categories(response_uz, message2, 0.8)

    return ctgrs
    
def get_categoriesv2(text: str):
    kwds = Keywords.select()
    categories = set()
    for quer in kwds:
        quer: Keywords

        # if  f"{str(quer.keyword).lower()}" in a.lower():
        #     print(quer.category)
        #     print(quer.keyword)
        # else:
        #     continue

        if re.match(f'.?{str(quer.keyword).lower()}', text.lower(), re.DOTALL):
            
            categories.add(quer.category)

    # return get_language(text, response_ru, response_cyrl, response_uz)
    for quer in kwds:
        str1 = text.lower().split()
        str2 = str(quer.keyword).lower()
        a = difflib.get_close_matches(str2, str1, 3, 0.85) 
        for i in a:
            # categories2.add(f"{key}||{list(j.keys())[0]}||{parents[key]}||{str2}||{set(a)}")  
            categories.add(f'{quer.category}')

    return categories
