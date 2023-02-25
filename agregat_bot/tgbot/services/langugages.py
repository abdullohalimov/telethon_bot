from lingua import Language, LanguageDetectorBuilder
from tgbot.services.categories import get_categories

def detect_cyrillic_language(text):
    # languages = [Language.TURKISH, Language.ENGLISH]
    detector = LanguageDetectorBuilder.from_all_languages_with_cyrillic_script().build()
    return detector.detect_language_of(text)


def get_language(message2, response_ru, response_cyrl, response_uz):
    # languages = [Language.TURKISH, Language.ENGLISH]
    detector = LanguageDetectorBuilder.from_all_languages().build()
    if detector.detect_language_of(message2) == Language.RUSSIAN:
        print("RUSSIAN LANGUAGEE")
        ctgrs = get_categories(response_ru, message2, 0.7)
        if ctgrs == " ":
            ctgrs = get_categories(response_ru, message2, 0.5)

        print(ctgrs)
    else:
        if detect_cyrillic_language(message2):
            print("CYRL LANGUAGEE")

            ctgrs = get_categories(response_cyrl, message2, 0.7)
            if ctgrs == " ":
                ctgrs = get_categories(response_cyrl, message2, 0.5)
            print(ctgrs)

        else:
            print("LATIN LANGUAGEE")

            ctgrs = get_categories(response_uz, message2, 0.7)
            if ctgrs == " ":
                ctgrs = get_categories(response_uz, message2, 0.5)
            print(ctgrs)

    return ctgrs
    
