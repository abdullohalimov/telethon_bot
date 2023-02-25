from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

def categories_inl(categories):
    keyb = InlineKeyboardMarkup()
    for i in categories:
        keyb.add(InlineKeyboardButton(i, callback_data=i))
    keyb.add(InlineKeyboardButton("Все равно добавить", callback_data="add"))
    return keyb
    