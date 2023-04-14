from typing import List
from aiogram import Router, Bot
from aiogram.types import Message
import requests
import re
from tgbot.keyboards.inline import categories_inl
from tgbot.models.database import Person
from tgbot.services.langugages import get_language
from tgbot.services.api import register_new_product_and_user
from datetime import datetime
from typing import List
from aiogram.types import Message
# import markdown
from aiogram.utils import markdown

url = "https://aztester.uz/api-announcement/v1/category/tree"
response_uz = requests.get(url, headers={'language': "uz_latn"})
response_cyrl = requests.get(url, headers={'language': "uz_cyrl"})
response_ru = requests.get(url, headers={'language': "ru"})

admin_router = Router()
# admin_router.message.filter(AdminFilter())
# admin_router.message.middleware(MediaGroupMiddleware)


def remove_markdown(text: str):
    """Berilgan matndan markdown elementlarini kesib tashlash funksiyasi

    Args:
        text (str): Markdowndan tozalanishi kerak bo'lgan matn

    Returns:
        str: Markdowndan tozalangan matn
    """
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`.*?`', '', text)
    # Remove bold and italic formatting
    text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
    text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
    # Remove headings
    text = re.sub(r'^\s*(#+)\s*(.*?)\s*$', r'\2', text, flags=re.MULTILINE)
    # Remove unordered lists
    text = re.sub(r'^\s*[-+*]\s+(.*)$', r'\1', text, flags=re.MULTILINE)
    # Remove ordered lists
    text = re.sub(r'^\s*\d+\.\s+(.*)$', r'\1', text, flags=re.MULTILINE)
    # Remove blockquotes
    text = re.sub(r'^\s*>+\s*(.*)$', r'\1', text, flags=re.MULTILINE)
    # Remove horizontal rules
    text = re.sub(r'^\s*[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', text)

    return text.strip()


def caption_text(got_data, status, status2, categories='none', media_files='none', is_album=False):
    """Filtr qilingan xabarni bazaga joylash va kanalga yuborish funksiyasi. Funksiya guruxga yuborilishi kerak bolgan xabarni qaytaradi.

    Args:
        got_data (_type_): Botga kelgan xabar malumotlari
        status (_type_): joylangan yoki joylanmaganlik statusi
        status2 (_type_): Bazadagi statusi
        categories (str, optional): Kategoriyalar. Default 'none'.
        media_files (str, optional): Media fayllar. Default 'none'.
        is_album (bool, optional): Album yoki yo'qligi. Default False.
    """
    categories_to_add = 'none' if categories == 'none' else ','.join(
        categories)
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
👤 User: {markdown.link(got_data['user_name'], f"https://t.me/{got_data['user_link']}")} 
🔹 Group: {markdown.link(got_data['group_name'], f"https://t.me/{got_data['group_link']}")} ID: {markdown.bold(got_data['group_id'])}
👉 {markdown.link("Message Link", f"https://t.me/{got_data['group_link']}/{got_data['message_id']}")} ID: {markdown.bold(got_data['message_id'])}
💬 Message: {remove_markdown(got_data['message_text'])}
📝 Category: {categories_to_add}'''
    return txt


def str_to_dict(string):
    """User-Agentdan kelgan xabarni botda foydalanish uchun tayyorlovchi funksiya

    Args:
        string (str): User-Agent xabari

    Returns:
        str: Bot ishlashi uchun tayyor xabar
    """
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
    if message.media_group_id != None:
        # agar xabar album bo'lsa:
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
            phone = f"+{got_data['user_link']}" if '998' in got_data['user_link'] else ''
            if categories:
                txt = caption_text(
                    got_data=got_data, status="joylandi ✅", status2='1', media_files=group_elements, categories=categories, is_album=True)
                await bot.send_message(chat_id=-1001527539668, text=txt, reply_markup=categories_inl(categories), disable_web_page_preview=False)
                await register_new_product_and_user(got_data=got_data, media_files=group_elements, phone_number=phone, categories=categories, datetime=int(datetime.now().timestamp()))
            else:
                txt = caption_text(got_data=got_data, media_files=group_elements, is_album=True,
                                   status="joylanmadi ❌", status2='0')
                await bot.send_message(chat_id=-1001527539668, text=txt, reply_markup=categories_inl(categories), disable_web_page_preview=False)
                await register_new_product_and_user(got_data=got_data, media_files=group_elements, phone_number=phone, datetime=int(datetime.now().timestamp()), status='0')

        pass
    else:
        if message.photo:
            # agar xabar photo bo'lsa:
            try:
                got_data = str_to_dict(message.caption)
            except:
                print(message)
            if len(got_data['message_text'].split()) > 3:
                categories = get_language(
                    got_data['message_text'], response_ru, response_cyrl, response_uz)
                phone = f"+{got_data['user_link']}" if '998' in got_data['user_link'] else ''
                if categories:
                    txt = caption_text(got_data=got_data, status="joylandi ✅", status2='1',
                                       categories=categories, media_files=message.photo[0].file_id)
                    await bot.send_photo(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), photo=message.photo[0].file_id)
                    await register_new_product_and_user(got_data=got_data, media_files=message.photo[0].file_id, phone_number=phone, categories=categories, datetime=int(datetime.now().timestamp()))
                else:
                    txt = caption_text(got_data=got_data, status="joylanmadi ❌",
                                       status2='0', media_files=message.photo[0].file_id)
                    await bot.send_photo(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), photo=message.photo[0].file_id)
                    await register_new_product_and_user(got_data=got_data, media_files=message.photo[0].file_id, phone_number=phone, datetime=int(datetime.now().timestamp()), status='0')


        elif message.video:
            # agar xabar video bo'lsa:
            try:
                got_data = str_to_dict(message.caption)
            except:
                print(message)
            if len(got_data['message_text'].split()) > 3:
                categories = get_language(
                    got_data['message_text'], response_ru, response_cyrl, response_uz)
                phone = f"+{got_data['user_link']}" if '998' in got_data['user_link'] else ''
                if categories:
                    txt = caption_text(got_data=got_data, status="joylandi ✅", status2='1',
                                       categories=categories, media_files=message.video.file_id)
                    await bot.send_video(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), video=message.video.file_id)
                    await register_new_product_and_user(got_data=got_data, media_files=message.video.file_id, phone_number=phone, categories=categories, datetime=int(datetime.now().timestamp()))
                else:
                    txt = caption_text(got_data=got_data, status="joylanmadi ❌",
                                       status2='0', media_files=message.video.file_id)
                    await bot.send_video(chat_id=-1001527539668, caption=txt, reply_markup=categories_inl(categories), video=message.video.file_id)
                    await register_new_product_and_user(got_data=got_data, media_files=message.video.file_id, phone_number=phone, datetime=int(datetime.now().timestamp()), status='0')


        else:
            # agar xabar matn bo'lsa
            try:
                got_data = str_to_dict(message.text)
            except:
                print(message)
            if len(got_data['message_text'].split()) > 3:
                categories = get_language(
                    got_data['message_text'], response_ru, response_cyrl, response_uz)
                phone = f"+{got_data['user_link']}" if '998' in got_data['user_link'] else ''
                if categories:
                    txt = caption_text(
                        got_data=got_data, status="joylandi ✅", status2='1', categories=categories)
                    await bot.send_message(-1001527539668, txt, reply_markup=categories_inl(categories), disable_web_page_preview=True)
                    await register_new_product_and_user(got_data=got_data, media_files='none', phone_number=phone, categories=categories, datetime=int(datetime.now().timestamp()))
                else:
                    txt = caption_text(got_data=got_data,
                                       status="joylanmadi ❌", status2='0')
                    await bot.send_message(-1001527539668, txt, reply_markup=categories_inl(categories), disable_web_page_preview=True)
                    await register_new_product_and_user(got_data=got_data, media_files='none', phone_number=phone, datetime=int(datetime.now().timestamp()), status='0')



# @admin_router.message(CommandStart())
# async def admin_start(message: Message):
#     await message.reply("Привет, Админ!")
