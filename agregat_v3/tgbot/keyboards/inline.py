from aiogram.types import InlineKeyboardButton
from tgbot.keyboards.factory import CategoryData, CategoryKeyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.services.catgkeyboard import get_catalog


def categories_inl(categories = None):
    keyb = InlineKeyboardBuilder()
    if categories:
        if len(categories) >= 1:
            for i in categories:
                if i == 'none':
                    continue
                a = get_catalog(c = i)
                print(a)
                a = a.split(':>:')
                # print(splitted)
                keyb.row(InlineKeyboardButton(text=f'❌ {a[2]} -> {a[0]}', callback_data=CategoryData(category=a[1]).pack()))
        else:
            a = get_catalog(c = i)
            print(a)
            a = a.split(':>:')
            # print(splitted)
            keyb.row(InlineKeyboardButton(text=f'❌ {a[2]} -> {a[0]}', callback_data=CategoryData(category=a[1]).pack()))
    keyb.row(InlineKeyboardButton(text="🗂 Категории", callback_data="categories"))
    keyb.add(InlineKeyboardButton(text="🗑 Удалить", callback_data="delete"))
    
    return keyb.as_markup()

def categories_keyb_inl(categories: list):
    keyb = InlineKeyboardBuilder()
    for key, value in categories[0].items():
        keyb.add(InlineKeyboardButton(text=f'{value}', callback_data=CategoryKeyboard(category=key, parent=categories[1]).pack()))
    
    keyb.adjust(2)
    if categories[0] == []:
        return False
    else:
        return keyb.as_markup()


recover_inl = InlineKeyboardBuilder().row(InlineKeyboardButton(text="✅ Восстановить", callback_data="recover")).as_markup()


