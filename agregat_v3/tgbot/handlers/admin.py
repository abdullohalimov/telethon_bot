from typing import List
from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, InputMediaPhoto
import requests
import re
from tgbot.keyboards.inline import categories_inl
from tgbot.models.database import Person
from tgbot.filters.admin import AdminFilter
from tgbot.services.langugages import get_language
from datetime import datetime
from typing import List
from aiogram.types import (
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
    TelegramObject,
)
from aiogram import html

url = "https://aztester.uz/api-announcement/v1/category/tree"
response_uz = requests.get(url, headers={'language': "uz_latn"})
response_cyrl = requests.get(url, headers={'language': "uz_cyrl"})
response_ru = requests.get(url, headers={'language': "ru"})

admin_router = Router()
# admin_router.message.filter(AdminFilter())
# admin_router.message.middleware(MediaGroupMiddleware)


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def caption_text(got_data, status, status2, categories='none', media_files='none', ):
    categories_to_add = 'none' if categories == 'none' else ','.join(categories)
    
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
        ex_db_record.category = categories_to_add
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
            category=categories_to_add,
            media_files=media_files,
            datatime=datetime.now(),
            status=status2,
        )

    txt = f'''
⚡️ Statusi:  #{status}
👤 User: {html.link(got_data['user_name'], f"https://t.me/{got_data['user_link']}")} 
🔹 Group: {html.link(got_data['group_name'], f"https://t.me/{got_data['group_link']}")} ID: {html.bold(got_data['group_id'])}
👉 {html.link("Message Link", f"https://t.me/{got_data['group_link']}/{got_data['message_id']}")} ID: <b>{got_data['message_id']}</b> 
💬 Message: {remove_html_tags(got_data['message_text'])}
📝 Category: {categories_to_add}'''
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


@admin_router.message()
async def new_announcement(message: Message, bot: Bot, album: List[Message] = list()):
    # функция должна принятое сообщение переслать в другую группу и добавить к нему две инлайн кнопки
    # print(message)
    if message.media_group_id != None:
        """This handler will receive a complete album of any type."""
        group_elements = []
        caption = ''
        for element in album:
            caption_kwargs = {"caption": element.caption,
                            "caption_entities": element.caption_entities}
            if caption_kwargs['caption'] != None:
                caption = caption_kwargs['caption']
            if element.photo:
                input_media = element.photo[-1].file_id
            elif element.video:
                input_media = element.video.file_id
            elif element.document:
                input_media = element.document.file_id
            elif element.audio:
                input_media = element.audio.file_id
            else:
                return message.answer("This media type isn't supported!")

            group_elements.append(input_media)
        try:
            got_data = str_to_dict(caption)
        except:
            print(caption)
        if len(got_data['message_text'].split()) > 3:
            # message2 = await bot.send_media_group(chat_id=-1001527539668, media=group_elements)
            categories = get_language(
                got_data['message_text'], response_ru, response_cyrl, response_uz)
            if categories:
                txt = caption_text(
                    got_data=got_data, status="joylandi ✅", status2='1', media_files=group_elements, categories=categories)
                await bot.send_message(chat_id=-1001527539668, text=txt, reply_markup=categories_inl(categories), disable_web_page_preview=False)
            else:
                txt = caption_text(got_data=got_data, media_files=group_elements,
                                    status="joylanmadi ❌", status2='0')
                await bot.send_message(chat_id=-1001527539668, text=txt, reply_markup=categories_inl(categories), disable_web_page_preview=False)
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
                if categories:
                    txt = caption_text(got_data=got_data, status="joylandi ✅", status2='1',
                                       categories=categories, media_files=message.photo[0].file_id)
                    await bot.send_photo(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), photo=message.photo[0].file_id)
                else:
                    txt = caption_text(got_data=got_data, status="joylanmadi ❌",
                                       status2='0', media_files=message.photo[0].file_id)
                    await bot.send_photo(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), photo=message.photo[0].file_id)

        elif message.video:
            try:
                got_data = str_to_dict(message.caption)
            except:
                print(message)
            if len(got_data['message_text'].split()) > 3:
                categories = get_language(
                    got_data['message_text'], response_ru, response_cyrl, response_uz)
                if categories:
                    txt = caption_text(got_data=got_data, status="joylandi ✅", status2='1',
                                       categories=categories, media_files=message.video.file_id)
                    await bot.send_video(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), video=message.video.file_id)
                else:
                    txt = caption_text(got_data=got_data, status="joylanmadi ❌",
                                       status2='0', media_files=message.video.file_id)
                    await bot.send_video(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), video=message.video.file_id)

        else:
            try:
                got_data = str_to_dict(message.text)
            except:
                print(message)
            if len(got_data['message_text'].split()) > 3:
                categories = get_language(
                    got_data['message_text'], response_ru, response_cyrl, response_uz)
                if categories:
                    txt = caption_text(
                        got_data=got_data, status="joylandi ✅", status2='1', categories=categories)
                    await bot.send_message(-1001527539668, txt, reply_markup=categories_inl(categories), disable_web_page_preview=True)
                else:
                    txt = caption_text(got_data=got_data,
                                       status="joylanmadi ❌", status2='0')
                    await bot.send_message(-1001527539668, txt, reply_markup=categories_inl(categories), disable_web_page_preview=True)


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Привет, Админ!")



    