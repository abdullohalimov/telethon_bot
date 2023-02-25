from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

def categories_inl(categories):
    keyb = InlineKeyboardMarkup()
    for i in categories:
        keyb.add(InlineKeyboardButton(i, callback_data=i))
    keyb.add(InlineKeyboardButton("Категории", callback_data="add"))
    keyb.add(InlineKeyboardButton("Удалить", callback_data="add"))
    return keyb
    

# Функция возвращает Inline Keyboard с статическими кнопками 
def langugage_keyboard():
    keyb = InlineKeyboardMarkup()
    keyb.add(InlineKeyboardButton("Русский", callback_data="rus"))
    keyb.add(InlineKeyboardButton("O'zbekcha", callback_data="uzb"))
    return keyb