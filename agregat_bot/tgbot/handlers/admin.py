from datetime import datetime
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, ContentTypes
from tgbot.models.database import Person
from tgbot.keyboards.inline import categories_inl
import re

from tgbot.services.langugages import get_language
import requests

url = "https://aztester.uz/api-announcement/v1/category/tree"
response_uz = requests.get(url, headers={'language': "uz_latn"})
response_cyrl = requests.get(url, headers={'language': "uz_cyrl"})
response_ru = requests.get(url, headers={'language': "ru"})

# def get_or_add_to_base(got_data, categories):


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def caption_text(got_data, status, status2, categories = 'none', media_files = 'none', ):
    try:
        ex_db_record: Person = Person.get(
            Person.message_text == got_data['message_text'])
        ex_db_record.user_id = got_data['user_id']
        ex_db_record.user_name = got_data['user_name']
        ex_db_record.user_link = got_data['user_link']
        ex_db_record.group_id = got_data['group_id']
        ex_db_record.group_name = got_data['group_name']
        ex_db_record.group_link = got_data['group_link']
        ex_db_record.message_id = got_data['message_id']
        ex_db_record.message_text = got_data['message_text']
        ex_db_record.category = f"{categories[0]}"
        ex_db_record.media_files = media_files
        ex_db_record.datatime = datetime.now()
        ex_db_record.status = status2
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
            category=f"{categories[0]}",
            media_files=media_files,
            datatime=datetime.now(),
            status=status2,
        )

    txt = f'''
⚡️ Statusi:  #{status}
👤 User: <a href="https://t.me/{got_data['user_link']}">{got_data['user_name']}</a> 
🔹 Group: <a href="https://t.me/{got_data['group_link']}">{got_data['group_name']}</a> ID: <b>{got_data['group_id']}</b>
💬 Message: {remove_html_tags(got_data['message_text'])}
👉 <a href="https://t.me/{got_data['group_link']}/{got_data['message_id']}">Message_link</a> ID: <b>{got_data['message_id']}</b> ''' 
    return txt


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
        pass
    else:
        if message.photo:
            try:
                got_data = str_to_dict(message.caption)
            except:
                print(message)
            if len(got_data['message_text'].split()) > 3:
                categories = get_language(
                    got_data['message_text'], response_ru, response_cyrl, response_uz)
                if categories[0]:
                    txt = caption_text(got_data=got_data, status="joylandi ✅", status2='1',
                                       categories=categories, media_files=message.photo[0].file_id)
                    await message.bot.send_photo(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), photo=message.photo[0].file_id)
                else:
                    txt = caption_text(got_data=got_data, status="joylanmadi ❌", status2='0' ,media_files=message.photo[0].file_id)
                    await message.bot.send_photo(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), photo=message.photo[0].file_id)

        elif message.video:
            try:
                got_data = str_to_dict(message.caption)
            except:
                print(message)
            if len(got_data['message_text'].split()) > 3:
                categories = get_language(
                    got_data['message_text'], response_ru, response_cyrl, response_uz)
                if categories[0]:
                    txt = caption_text(got_data=got_data, status="joylandi ✅", status2='1',
                                       categories=categories, media_files=message.video.file_id)
                    await message.bot.send_video(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), video=message.video.file_id)
                else:
                    txt = caption_text(got_data=got_data, status="joylanmadi ❌", status2='0', media_files=message.video.file_id)
                    await message.bot.send_video(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), video=message.video.file_id)

        else:
            try:
                got_data = str_to_dict(message.text)
            except:
                print(message)
            if len(got_data['message_text'].split()) > 3:
                categories = get_language(
                    got_data['message_text'], response_ru, response_cyrl, response_uz)
                if categories[0]:
                    txt = caption_text(got_data=got_data, status="joylandi ✅", status2='1', categories=categories)
                    await message.bot.send_message(-1001527539668, txt, reply_markup=categories_inl(categories), disable_web_page_preview=True)
                else:
                    txt = caption_text(got_data=got_data, status="joylanmadi ❌", status2='0')
                    await message.bot.send_message(-1001527539668, txt, reply_markup=categories_inl(categories), disable_web_page_preview=True)


async def callback_handler(callback: CallbackQuery):
    print(callback.message.entities)
    print(callback.message.text[78:78+10])
    print('ok')



def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=[
                                "start"], state="*", is_admin=True)
    dp.register_message_handler(
        new_announcement, content_types=ContentTypes.ANY, state="*", is_admin=True)
    dp.register_callback_query_handler(callback_handler, state="*")
    
