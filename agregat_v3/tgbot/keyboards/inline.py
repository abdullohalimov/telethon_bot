from aiogram.types import InlineKeyboardButton
from tgbot.keyboards.factory import CategoryData
from aiogram.utils.keyboard import InlineKeyboardBuilder


def categories_inl(categories):
    keyb = InlineKeyboardBuilder()
    for i in categories[0]:
        splitted = i.split('||')
        print(categories[0])
        # print(splitted)
        keyb.row(InlineKeyboardButton(text=f'{splitted[2]}: {splitted[3].replace("{", "").replace("}", "")} {splitted[4]}', callback_data=CategoryData(parent_id=splitted[0], child_id=splitted[1], parent_name=splitted[2], child_name=splitted[3], match_words=splitted[4]).pack()))
    keyb.row(InlineKeyboardButton(text="Категории", callback_data="categories"))
    keyb.add(InlineKeyboardButton(text="Удалить", callback_data="delete"))
    
    
    return keyb.as_markup()


# Функция возвращает Inline Keyboard с статическими кнопками
def langugage_keyboard():
    keyb = InlineKeyboardBuilder()
    keyb.add(InlineKeyboardButton(text="Русский", callback_data="rus"))
    keyb.add(InlineKeyboardButton(text="O'zbekcha", callback_data="uzb"))
    return keyb.as_markup()
