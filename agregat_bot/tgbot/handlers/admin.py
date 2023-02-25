from datetime import datetime
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, ContentTypes
from tgbot.models.database import Person
from tgbot.keyboards.inline import categories_inl

from tgbot.services.langugages import get_language
import requests

url = "https://aztester.uz/api-announcement/v1/category/tree"
response_uz = requests.get(url, headers={'language': "uz_latn"})
response_cyrl = requests.get(url, headers={'language': "uz_cyrl"})
response_ru = requests.get(url, headers={'language': "ru"})


def str_to_dict(string):
    dictionary = {}
    data = string.split('(delimeter)')
    dictionary['user_id'] = data[0]
    dictionary['user_name'] = data[1]
    dictionary['user_link'] = data[2]
    dictionary['group_id'] = data[3]
    dictionary['group_name'] = data[4]
    dictionary['group_link'] = data[5]
    dictionary['message_id'] = data[6]
    dictionary['message_text'] = data[7]
    return dictionary



async def admin_start(message: Message):
    await message.reply("Hello, admin!")


async def new_announcement(message: Message):
    # функция должна принятое сообщение переслать в другую группу и добавить к нему две инлайн кнопки
    # print(message)
    if message.media_group_id != None:
        #album
        # print("Album")
        pass
    else:
        # print(message.caption)
        # exit(0)
        # got_data = str_to_dict(message.text)
        # if got_data[''] and len(event.message.text.split()) > 3:
        # print(got_data)
        # print(message.photo)
        if message.photo:
            try:
                got_data = str_to_dict(message.caption)
            except:
                print(message)
            if len(got_data['message_text'].split()) > 3:
                categories = get_language(got_data['message_text'], response_ru, response_cyrl, response_uz)
                if categories:
                    txt = f'''
⚡️ Statusi:  #joylandi ✅
👤 User: {got_data['user_name']} (https://t.me/{got_data['user_link']})])
🔹 Group {got_data['group_name']} (https://t.me/{got_data['group_link']})])
💬 Message: {got_data['message_text']}
👉 message_link: https://t.me/{got_data['group_link']}/{got_data['message_id']}'''
                    try:
                        ex_db_record: Person = Person.get(Person.message_text == got_data['message_text'])       
                        ex_db_record.datatime = datetime.now()
                        ex_db_record.save()
                    except:
                    
                        Person.create(
                        user_id=got_data['user_id'], 
                        user_name=got_data['user_name'], 
                        user_link=got_data['user_link'], 
                        group_id=got_data['group_id'], 
                        group_name=got_data['group_name'], 
                        group_link=got_data['group_link'], 
                        message_id=got_data['message_id'], 
                        message_text=got_data['message_text'], 
                        category=f"{categories}", 
                        media_files='none',
                        datatime=datetime.now()
                        )
                    await message.bot.send_message(-1001527539668, txt, reply_markup=categories_inl(categories))
                else:
                    txt = f'''
⚡️ Statusi:  #joylanmadi ❌
👤 User: {got_data['user_name']} (https://t.me/{got_data['user_link']})])
🔹 Group {got_data['group_name']} (https://t.me/{got_data['group_link']})])
💬 Message: {got_data['message_text']}
👉 message_link: https://t.me/{got_data['group_link']}/{got_data['message_id']}'''
                    await message.bot.send_message(-1001527539668, txt, reply_markup=categories_inl(categories))

                    
        else:
            try:
                got_data = str_to_dict(message.text)
            except:
                print(message)
            if len(got_data['message_text'].split()) > 3:
                categories = get_language(got_data['message_text'], response_ru, response_cyrl, response_uz)
                if categories:
                    txt = f'''
⚡️ Statusi:  #joylandi ✅
👤 User: {got_data['user_name']} (https://t.me/{got_data['user_link']})])
🔹 Group {got_data['group_name']} (https://t.me/{got_data['group_link']})])
💬 Message: {got_data['message_text']}
👉 message_link: https://t.me/{got_data['group_link']}/{got_data['message_id']}'''
                    try:
                        ex_db_record: Person = Person.get(Person.message_text == got_data['message_text'])     
                        ex_db_record.datatime = datetime.now()
                        ex_db_record.save()
                    except Exception:
                        Person.get_or_create(
                        user_id=got_data['user_id'], 
                        user_name=got_data['user_name'], 
                        user_link=got_data['user_link'], 
                        group_id=got_data['group_id'], 
                        group_name=got_data['group_name'], 
                        group_link=got_data['group_link'], 
                        message_id=got_data['message_id'], 
                        message_text=got_data['message_text'], 
                        category=f"{categories} ", 
                        media_files='none',
                        datatime=datetime.now()
                        )
                    await message.bot.send_message(-1001527539668, txt, reply_markup=categories_inl(categories))
                else:
                    txt = f'''
    ⚡️ Statusi:  #joylanmadi ❌
    👤 User: {got_data['user_name']} (https://t.me/{got_data['user_link']})])
    🔹 Group {got_data['group_name']} (https://t.me/{got_data['group_link']})])
    💬 Message: {got_data['message_text']}
    👉 message_link: https://t.me/{got_data['group_link']}/{got_data['message_id']}'''
                    await message.bot.send_message(-1001527539668, txt, reply_markup=categories_inl(categories))
                print(categories)
            

async def callback_handler(callback: CallbackQuery):
    if callback.data == "add":
        await callback.answer(cache_time=60)
    else:
        pass
        
    await callback.answer(cache_time=60)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=[
                                "start"], state="*", is_admin=True)
    dp.register_message_handler(new_announcement, content_types=ContentTypes.ANY, state="*", is_admin=True)
