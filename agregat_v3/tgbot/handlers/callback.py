from traceback import print_exc
from aiogram.types import CallbackQuery
from tgbot.keyboards.factory import CategoryData, CategoryKeyboard, DeleteButtons
from aiogram import Router, Bot
from tgbot.models.database import Product
from tgbot.keyboards.inline import main_menu_keyboard, add_category_keyboard, deleting_keyboard
from tgbot.handlers.admin import remove_markdown
from tgbot.services.catgkeyboard import get_catalog
from tgbot.services.api import delete_product

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
        group_id = callback.message.entities[3].extract_from(callback.message.text)
        message_id = callback.message.entities[5].extract_from(callback.message.text)    
    else:
        msgtype = 'caption'
        entities = callback.message.caption_entities
        group_id = callback.message.caption_entities[3].extract_from(callback.message.caption)
        message_id = callback.message.caption_entities[5].extract_from(callback.message.caption)
    # print(msgtype, entities, group_id, message_id)
    return [msgtype, entities, group_id, message_id]


@custom_router.callback_query(CategoryData.filter())
async def category_data(callback: CallbackQuery, callback_data: CategoryData):
    """E'longa o'rnatilgan kategoriyalarni o'chiruvchi handler. Biron kategoriya o'chirish uchun bosilganda uni shu e'londan o'chirib yuboradi

    Args:
        callback (CallbackQuery): Kiruvchi Callback
        callback_data (CategoryData): Callbackning qo'shimcha ma'lumotlari
    """
    # kelgan callback orqali unga tegishli xabardagi ma'lumotlarni olish
    msgtype, entities, group_id, message_id = id_list(callback)
    
    # message_id va group_id orqali bazadan shu e'lon ma'lumotlarini topish
    record: Product = Product.get(Product.message_id==message_id, Product.group_id==group_id)
    
    a = callback_data.category  
    newcategory = record.category.split(',')
    newcategory.remove(a)
    newcategory2 = ','.join(newcategory) if newcategory != [] else 'none'
    if msgtype == 'caption':
        await callback.message.edit_caption(caption=callback.message.caption.replace(f'📝 Category: {record.category}', f'📝 Category: {newcategory2}'), caption_entities=entities, reply_markup=main_menu_keyboard(newcategory), disable_web_page_preview=True)
    else:
        await callback.message.edit_text(text=callback.message.text.replace(f'📝 Category: {record.category}', f'📝 Category: {newcategory2}'), entities=entities, reply_markup=main_menu_keyboard(newcategory), disable_web_page_preview=True)
    record.category = newcategory2
    record.save()
    await callback.answer()


@custom_router.callback_query(CategoryKeyboard.filter())
async def category_keyboard(callback: CallbackQuery, callback_data: CategoryKeyboard):
    print('router3')
    msgtype, entities, group_id, message_id = id_list(callback)
    record: Product = Product.get(Product.message_id==message_id, Product.group_id==group_id)
    print(callback_data)
    catlg = get_catalog(callback_data.category)
    newcategory = f"{record.category},{callback_data.category}".replace('none,', '')
    if catlg != {}:
        await callback.message.edit_reply_markup(reply_markup=add_category_keyboard(catlg))
    else:
        textt = f'📝 Category: {record.category},{callback_data.category}'.replace('none,', '')
        if msgtype == "caption":
            await callback.message.edit_caption(caption=callback.message.caption.replace(f'📝 Category: {record.category}', textt), caption_entities=entities, reply_markup=main_menu_keyboard(newcategory.split(',')), disable_web_page_preview=True)
        else:
            await callback.message.edit_text(text=callback.message.text.replace(f'📝 Category: {record.category}', textt), entities=entities, reply_markup=main_menu_keyboard(newcategory.split(',')), disable_web_page_preview=True)
        record.category = f"{record.category},{callback_data.category}".replace('none,', '')
        record.save()
        # await callback.message.edit_reply_markup(reply_markup=categories_inl())
    await callback.answer()
    

@custom_router.callback_query(DeleteButtons.filter())
async def delete_buttons(callback: CallbackQuery, callback_data: DeleteButtons):
    msgtype, entities, group_id, message_id = id_list(callback)
    
    entities = entities[0], entities[1], entities[2], entities[3], entities[4], entities[5]
    
    if callback_data.state == "alarm":
        await callback.message.edit_reply_markup(reply_markup=deleting_keyboard())
            
    elif callback_data.state == "misclick":
        text = callback.message.caption if msgtype == 'caption' else callback.message.text
        categories = text[text.find('📝 Category:'):].replace('📝 Category:', '').split(',')
        await callback.message.edit_reply_markup(reply_markup=main_menu_keyboard(categories))
        
    elif callback_data.state == "delete":
        record: Product = Product.get(Product.message_id==message_id, Product.group_id==group_id)
        await delete_product(message_id=message_id, group_id=group_id)
        record.delete()
        record.save()
        await callback.message.delete()
    
    await callback.answer()


@custom_router2.callback_query()
async def callback_handler(callback: CallbackQuery):
    # msgtype, entities, group_id, message_id = id_list(callback)
    
    # entities = entities[0], entities[1], entities[2], entities[3], entities[4], entities[5]

    if callback.data == 'categories':
        await callback.message.edit_reply_markup(reply_markup=add_category_keyboard(get_catalog(0)))
    await callback.answer()





# if callback.data == "delete":
#     try:
#         record: Person = Person.get(Person.message_id==message_id, Person.group_id==group_id)
#         record.status = '-1'
#         if msgtype == 'caption':
#             await callback.message.edit_caption(caption=callback.message.caption.replace(f'📝 Category: {record.category}', f'📝 Category: none') + "\n\n❌УДАЛЕН❌", reply_markup=recover_inl, caption_entities=entities, disable_web_page_preview=True)
#         else:
#             await callback.message.edit_text(text=callback.message.text.replace(f'📝 Category: {record.category}', f'📝 Category: none') + "\n\n❌УДАЛЕН❌", reply_markup=recover_inl, entities=entities, disable_web_page_preview=True)
#         record.category = 'none'
#         record.save()
#     except:
#         print(print_exc())
#         for i in entities:
#             print(i)

# if callback.data == 'recover':
#     record: Person = Person.get(Person.message_id==message_id, Person.group_id==group_id)
#     record.status = '0'
#     record.save()
#     if msgtype == 'caption':
#         await callback.message.edit_caption(caption=callback.message.caption.replace("\n\n❌УДАЛЕН❌", ""), reply_markup=main_menu_keyboard(), caption_entities=entities, disable_web_page_preview=True)
#     else:
#         await callback.message.edit_text(text=callback.message.text.replace("\n\n❌УДАЛЕН❌", ""), reply_markup=main_menu_keyboard(), entities=entities, disable_web_page_preview=True)

    
