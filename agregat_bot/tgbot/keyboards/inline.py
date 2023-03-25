from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.keyboards.factory import category_button


def categories_inl(categories):
    keyb = InlineKeyboardMarkup()
    for i in categories[0]:
        splitted = i.split('||')
        print(categories[0])
        # print(splitted)
        keyb.add(InlineKeyboardButton(f'{splitted[2]}: {splitted[3].replace("{", "").replace("}", "")} {splitted[4]}', callback_data=category_button.new(
            parent_id=splitted[0], child_id=splitted[1], parent_name=splitted[2], child_name=splitted[3], match_words=splitted[4])))
    keyb.add(InlineKeyboardButton("Категории", callback_data="categories"))
    keyb.add(InlineKeyboardButton("Удалить", callback_data="delete"))
    return keyb


# Функция возвращает Inline Keyboard с статическими кнопками
def langugage_keyboard():
    keyb = InlineKeyboardMarkup()
    keyb.add(InlineKeyboardButton("Русский", callback_data="rus"))
    keyb.add(InlineKeyboardButton("O'zbekcha", callback_data="uzb"))
    return keyb
