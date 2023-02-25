from datetime import datetime
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, ContentTypes
from tgbot.models.database import Person
from tgbot.keyboards.inline import categories_inl
from tgbot.services.categories import get_categories
from tgbot.services.langugages import detect_cyrillic_language, get_language
import requests

url = "https://aztester.uz/api-announcement/v1/category/tree"
response_uz = requests.get(url, headers={'language': "uz_latn"})
response_cyrl = requests.get(url, headers={'language': "uz_cyrl"})
response_ru = requests.get(url, headers={'language': "ru"})


def str_to_dict(string):
    # remove the curly braces from the string
    # string = string.strip('{}')
 
    # split the string into key-value pairs
    pairs = string.split(', \n')
    # return string.split('(delimeter)')
 
    # use a dictionary comprehension to create the dictionary, converting the values to integers and removing the quotes from the keys
    return {key[1:-2]: value for key, value in (pair.split(':^ ') for pair in pairs)}


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
        print(message.photo)
        if message.photo:
            pass
            # print(message.photo)
        else:
            try:
                got_data = str_to_dict(message.text)
            except:
                print(message)
            if len(got_data['message_text'].split()) > 3:
                categories = get_language(got_data['message_text'], response_ru, response_cyrl, response_uz)
                try:
                    ex_db_record: Person = Person.get(Person.message_text == message.text)       
                    ex_db_record.datatime = datetime.now()
                    ex_db_record.save()
                except:
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
