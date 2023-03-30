from traceback import print_exc
from aiogram.types import CallbackQuery
from tgbot.keyboards.factory import CategoryData, CategoryKeyboard
from aiogram import Router, Bot
from tgbot.models.database import Person
from tgbot.keyboards.inline import recover_inl, categories_inl, categories_keyb_inl
from tgbot.handlers.admin import remove_markdown
from tgbot.services.catgkeyboard import get_catalog

custom_router = Router()
custom_router2 = Router()

def id_list(callback: CallbackQuery):
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
    print('router2')
    msgtype, entities, group_id, message_id = id_list(callback)
    record: Person = Person.get(Person.message_id==message_id, Person.group_id==group_id)
    a = callback_data.category  
    newcategory = record.category.split(',')
    newcategory.remove(a)
    newcategory2 = ','.join(newcategory) if newcategory != [] else 'none'
    if msgtype == 'caption':
        await callback.message.edit_caption(caption=callback.message.caption.replace(f'📝 Category: {record.category}', f'📝 Category: {newcategory2}'), caption_entities=entities, reply_markup=categories_inl(newcategory), disable_web_page_preview=True)
    else:
        await callback.message.edit_text(text=callback.message.text.replace(f'📝 Category: {record.category}', f'📝 Category: {newcategory2}'), entities=entities, reply_markup=categories_inl(newcategory), disable_web_page_preview=True)
    record.category = newcategory2
    record.save()
    await callback.answer()

@custom_router.callback_query(CategoryKeyboard.filter())
async def category_keyboard(callback: CallbackQuery, callback_data: CategoryKeyboard):
    print('router3')
    msgtype, entities, group_id, message_id = id_list(callback)
    record: Person = Person.get(Person.message_id==message_id, Person.group_id==group_id)
    print(callback_data)
    catlg = get_catalog(callback_data.cat)
    newcategory = f"{record.category},{callback_data.cat}".replace('none,', '')
    if catlg != {}:
        await callback.message.edit_reply_markup(reply_markup=categories_keyb_inl(catlg))
    else:
        textt = f'📝 Category: {record.category},{callback_data.cat}'.replace('none,', '')
        if msgtype == "caption":
            await callback.message.edit_caption(caption=callback.message.caption.replace(f'📝 Category: {record.category}', textt), caption_entities=entities, reply_markup=categories_inl(newcategory.split(',')), disable_web_page_preview=True)
        else:
            await callback.message.edit_text(text=callback.message.text.replace(f'📝 Category: {record.category}', textt), entities=entities, reply_markup=categories_inl(newcategory.split(',')), disable_web_page_preview=True)
        record.category = f"{record.category},{callback_data.cat}".replace('none,', '')
        record.save()
        # await callback.message.edit_reply_markup(reply_markup=categories_inl())
    await callback.answer()
    

@custom_router2.callback_query()
async def callback_handler(callback: CallbackQuery):
    print('router1')
    msgtype, entities, group_id, message_id = id_list(callback)
    
    entities = entities[0], entities[1], entities[2], entities[3], entities[4], entities[5]
    if callback.data == "delete":
        try:
            record: Person = Person.get(Person.message_id==message_id, Person.group_id==group_id)
            record.status = '-1'
            if msgtype == 'caption':
                await callback.message.edit_caption(caption=callback.message.caption.replace(f'📝 Category: {record.category}', f'📝 Category: none') + "\n\n❌УДАЛЕН❌", reply_markup=recover_inl, caption_entities=entities, disable_web_page_preview=True)
            else:
                await callback.message.edit_text(text=callback.message.text.replace(f'📝 Category: {record.category}', f'📝 Category: none') + "\n\n❌УДАЛЕН❌", reply_markup=recover_inl, entities=entities, disable_web_page_preview=True)
            record.category = 'none'
            record.save()
        except:
            print(print_exc())
            for i in entities:
                print(i)

    if callback.data == 'recover':
        record: Person = Person.get(Person.message_id==message_id, Person.group_id==group_id)
        record.status = '0'
        record.save()
        if msgtype == 'caption':
            await callback.message.edit_caption(caption=callback.message.caption.replace("\n\n❌УДАЛЕН❌", ""), reply_markup=categories_inl(), caption_entities=entities, disable_web_page_preview=True)
        else:
            await callback.message.edit_text(text=callback.message.text.replace("\n\n❌УДАЛЕН❌", ""), reply_markup=categories_inl(), entities=entities, disable_web_page_preview=True)

    if callback.data == 'categories':
        await callback.message.edit_reply_markup(reply_markup=categories_keyb_inl(get_catalog(0)))
    await callback.answer()
