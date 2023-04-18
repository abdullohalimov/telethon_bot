from aiogram.types import InlineKeyboardButton
from tgbot.keyboards.factory import CategoryData, CategoryKeyboard, DeleteButtons
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.services.catgkeyboard import get_catalog_async
import logging

async def main_menu_keyboard(categories = None):
    keyb = InlineKeyboardBuilder()
    if categories:
        logging.warning(categories)
        if len(categories) >= 1:
            for i in categories:
                i = str(i)
                if 'none' in i:
                    continue
                try:
                    a = await get_catalog_async(c = i)
                    a = a.split(':>:')
                    # keyb.row(InlineKeyboardButton(text=f'❌ {a[2]} -> {a[0]}', callback_data=CategoryData(category=a[1]).pack()))
                    keyb.row(InlineKeyboardButton(text=f'❌ {a[0]}', callback_data=CategoryData(category=a[1]).pack()))
                except:
                    logging.critical(i)
                    logging.critical(type(i))
        else:
            a = await get_catalog_async(c = i)
            a = a.split(':>:')
            keyb.row(InlineKeyboardButton(text=f'❌ {a[2]} -> {a[0]}', callback_data=CategoryData(category=a[1]).pack()))
    keyb.row(InlineKeyboardButton(text="🗂 Категории", callback_data="categories"))
    keyb.add(InlineKeyboardButton(text="🗑 Удалить", callback_data=DeleteButtons(state='alarm').pack()))
    
    return keyb.as_markup()

def add_category_keyboard(categories: list):
    keyb = InlineKeyboardBuilder()
    for key, value in categories[0].items():
        keyb.add(InlineKeyboardButton(text=f'{value}', callback_data=CategoryKeyboard(category=key, parent=categories[1]).pack()))
    
    keyb.adjust(2)
    if categories[0] == []:
        return False
    else:
        return keyb.as_markup()

def deleting_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✅ Не удалить", callback_data=DeleteButtons(state='misclick').pack()))
    keyboard.row(InlineKeyboardButton(text="❌ УДАЛИТЬ ", callback_data=DeleteButtons(state='delete').pack()))
    
    return keyboard.as_markup()

# recover_inl = InlineKeyboardBuilder().row(InlineKeyboardButton(text="✅ Восстановить", callback_data="recover")).as_markup()


