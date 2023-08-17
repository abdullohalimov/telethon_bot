import logging
from pprint import pprint
from aiogram.types import CallbackQuery, MessageEntity
from tgbot.keyboards.factory import CategoryData, CategoryKeyboard, DeleteButtons
from aiogram import Router, Bot
# from tgbot.models.database import Product
from tgbot.keyboards.inline import main_menu_keyboard, add_category_keyboard, deleting_keyboard
from tgbot.handlers.admin import remove_markdown_and_links
from tgbot.services.catgkeyboard import get_catalog_async
from tgbot.services.api import delete_product, get_product, update_product

custom_router = Router()
custom_router2 = Router()


def id_list(callback: CallbackQuery):
    """Berilgan Callbackdage message turini (text yoki photo, video) aniqlash, undagi entitiylarni olish va shu entitylardan group_id va message_id ni chiqarib barcha malumotlarni bir list da qaytaradigan funksiya

    Args:
        callback (CallbackQuery): kiruvchi Callback

    Returns:
        list: [xabar turi, entitylar, gruppa_id, va message_id] list korinishida
    """
    if callback.message.entities != None:
        msgtype = 'text'
        entities = callback.message.entities
        bolds = [entity.extract_from(callback.message.text) for entity in callback.message.entities if entity.type == 'bold']
        group_id = bolds[0]
        message_id = bolds[1]
    else:
        msgtype = 'caption'
        entities = callback.message.caption_entities
        bolds = [entity.extract_from(callback.message.caption) for entity in callback.message.caption_entities if entity.type == 'bold']
        group_id = bolds[0]
        message_id = bolds[1]
    return [msgtype, entities, group_id, message_id]


@custom_router.callback_query(CategoryData.filter())
async def category_data(callback: CallbackQuery, callback_data: CategoryData):
    # kelgan callback orqali unga tegishli xabardagi ma'lumotlarni olish
    msgtype, entities, group_id, message_id = id_list(callback)

    # message_id va group_id orqali bazadan shu e'lon ma'lumotlarini topish
    record: dict = await get_product(group_id=group_id, message_id=message_id)
    pprint(record)
    if record.get('detail') == 'Not found.':
        await callback.message.edit_text(text='Такого товара не существует') if callback.message.text else await callback.message.edit_caption(caption='Такого товара не существует')
    else:
        logging.error(record)
        newcategory = list(record['categories'])
        logging.warning(newcategory)
        a = callback_data.category
        logging.warning(a)
        newcategory.remove(int(a))
        newcategory2 = ','.join(str(x) for x in newcategory) if newcategory != [] else 'none'
        text = callback.message.caption if msgtype == 'caption' else callback.message.text

        if msgtype == 'caption':
            await callback.message.edit_caption(caption=callback.message.caption.replace(text[text.find('📝 Category:'):], f"📝 Category: {newcategory2 if newcategory2 != 'none' else 'none'}"), caption_entities=entities, reply_markup=await main_menu_keyboard(newcategory), disable_web_page_preview=True)
        else:
            await callback.message.edit_text(text=callback.message.text.replace(text[text.find('📝 Category:'):], f"📝 Category: {newcategory2 if newcategory2 != 'none' else 'none'}"), entities=entities, reply_markup=await main_menu_keyboard(newcategory), disable_web_page_preview=True)
        # record.category = newcategory2

        await update_product(group_id=group_id, message_id=message_id, categories=newcategory2.split(',') if newcategory2 != 'none' else [])
        logging.warning(record['id'])



    await callback.answer()


@custom_router.callback_query(CategoryKeyboard.filter())
async def category_keyboard(callback: CallbackQuery, callback_data: CategoryKeyboard):
    """
     Edits the category of a product based on the user's selection from a category keyboard.

     Args:
     - callback: Telegram callback query object.
     - callback_data: User's selected category from the category keyboard.

     Returns: None
     """
    msgtype, entities, group_id, message_id = id_list(callback)

    catlg = await get_catalog_async(callback_data.category)

    if catlg[0] != {}:
        await callback.message.edit_reply_markup(reply_markup=add_category_keyboard(catlg))
    else:
        # this is a product
        # record: dict = await get_product(group_id=group_id, message_id=message_id)        
        # if record['category'] == []:
        #     pass
        # else:
        #     pass
        
        text = callback.message.caption if msgtype == 'caption' else callback.message.text
        
        categories: list = text[text.find('📝 Category:'):].replace('📝 Category: ', '').split(',') if "none" not in text[text.find('📝 Category:'):] else []

        # logging.warning(text)
        categories.append(callback_data.category)
        logging.warning(callback_data.category)
        logging.warning(categories)
     
        # textt = f'📝 Category: {categories},{callback_data.category}'
        
        await update_product(group_id=group_id, message_id=message_id, categories=categories)

        if msgtype == "caption":
            await callback.message.edit_caption(caption=callback.message.caption.replace(text[text.find('📝 Category:'):], f"📝 Category: {','.join(str(i) for i in categories)}"), caption_entities=entities, reply_markup=await main_menu_keyboard(categories=categories), disable_web_page_preview=True)
        else:
            await callback.message.edit_text(text=callback.message.text.replace(text[text.find('📝 Category:'):], f"📝 Category: {','.join(str(i) for i in categories)}"), entities=entities, reply_markup=await main_menu_keyboard(categories=categories), disable_web_page_preview=True)

        # await callback.message.edit_reply_markup(reply_markup=categories_inl())
    await callback.answer()


@custom_router.callback_query(DeleteButtons.filter())
async def delete_buttons(callback: CallbackQuery, callback_data: DeleteButtons):
    """
    Callback function to handle the delete buttons.

    Args:
        callback (CallbackQuery): The callback query object.
        callback_data (DeleteButtons): The callback data object.

    Returns:
        None
    """
    
    msgtype, entities, group_id, message_id = id_list(callback)

    # entities = entities[0], entities[1], entities[2], entities[3], entities[4], entities[5]

    if callback_data.state == "alarm":
        await callback.message.edit_reply_markup(reply_markup=deleting_keyboard())

    elif callback_data.state == "misclick":
        text = callback.message.caption if msgtype == 'caption' else callback.message.text
        categories = text[text.find('📝 Category:'):].replace(
            '📝 Category:', '').split(',')
        await callback.message.edit_reply_markup(reply_markup=await main_menu_keyboard(categories))

    elif callback_data.state == "delete":
        await delete_product(message_id=message_id, group_id=group_id)
        await callback.message.delete()

    await callback.answer()


@custom_router2.callback_query()
async def callback_handler(callback: CallbackQuery):
    """
    Handles callback queries from inline keyboards.

    :param callback: A CallbackQuery object representing the callback.
    :return: None
    """


    # msgtype, entities, group_id, message_id = id_list(callback)

    # entities = entities[0], entities[1], entities[2], entities[3], entities[4], entities[5]

    if callback.data == 'categories':
        await callback.message.edit_reply_markup(reply_markup=add_category_keyboard(await get_catalog_async(0)))
    await callback.answer()

