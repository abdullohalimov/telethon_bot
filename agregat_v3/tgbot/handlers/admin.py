from typing import List
from aiogram import Router, Bot
from aiogram.types import Message
import requests
import re
from tgbot.keyboards.inline import main_menu_keyboard
# from tgbot.models.database import Product
from tgbot.services.langugages import get_language, get_categoriesv2
from tgbot.services.api import register_new_product_and_user
from datetime import datetime
from typing import List
from aiogram.types import Message
# import markdown
from aiogram.utils import markdown

url = "https://agrozamin.uz/api-announcement/v1/category/tree"
response_uz = requests.get(url, headers={'language': "uz_latn"})
response_cyrl = requests.get(url, headers={'language': "uz_cyrl"})
response_ru = requests.get(url, headers={'language': "ru"})

admin_router = Router()
# admin_router.message.filter(AdminFilter())
# admin_router.message.middleware(MediaGroupMiddleware)


def remove_markdown_and_links(text: str):
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

    # Define a regular expression pattern to match links
    pattern = r"https?://\S+"
    # Replace all links with an empty string
    text = re.sub(pattern, "", text)

    return text.strip().replace('+998', '')


def caption_or_message_text(got_data, status, status2, categories='none', media_files='none', is_album=False):
    """
    Generate a caption or message text for a given set of data.

    Args:
    - got_data (dict): a dictionary containing information about the message
    - status (str): the status of the message
    - status2 (str): a second status of the message
    - categories (str): a string of categories to add to the message (default: 'none')
    - media_files (str): a string of media files to add to the message (default: 'none')
    - is_album (bool): whether or not the message contains an album (default: False)

    Returns:
    - txt (str): a formatted string containing the message text and metadata
    """

    categories_to_add = 'none' if categories == 'none' else ','.join(
        categories)

    txt = f'''
⚡️ Statusi:  #{status}
👤 User: {markdown.link(got_data['user_name'], f"https://t.me/{got_data['user_link']}") if got_data['user_link'] != 'none' else got_data['user_name']} 
🔹 Group: {markdown.link(got_data['group_name'], f"https://t.me/{got_data['group_link']}")} ID: {markdown.bold(got_data['group_id'])}
👉 {markdown.link("Message Link", f"https://t.me/{got_data['group_link']}/{got_data['message_id']}")} ID: {markdown.bold(got_data['message_id'])}
💬 Message: {remove_markdown_and_links(got_data['message_text'])}\n\n{'Contains Album' if is_album else ""}
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
    dictionary['user_link'] = data[2] if '998' not in data[2] else f"+{data[2]}"
    dictionary['group_id'] = data[3]
    dictionary['group_name'] = data[4]
    dictionary['group_link'] = data[5]
    dictionary['message_id'] = data[6]
    dictionary['message_text'] = data[7]
    return dictionary


@admin_router.message()
async def new_announcement(message: Message, bot: Bot, album: List[Message] = list()):
    """
    This function creates a new announcement message and sends it to a specified chat. 
    It takes a Telegram message object, a bot object, and an optional album of messages as input. 
    If the input message is an album of media, it extracts the relevant information from each element of the album and sends a media group message to the specified chat. 
    If the input message is a single photo or video, it sends a photo or video message to the specified chat. 
    If the input message is text, it sends a text message to the specified chat. 
    If the input message does not meet the criteria for any of these types, it returns an error message. 
    If the message meets the criteria for a valid announcement, it registers the announcement and the user who sent it in a database.

    Args:
    - message (telegram.Message): The Telegram message object that triggered the function call.
    - bot (telegram.Bot): The Telegram bot object that is handling the message.
    - album (List[telegram.Message], optional): A list of Telegram message objects that are part of the same media group as the input message. Defaults to an empty list.

    Returns:
    - None
    """

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
            pass
        if len(got_data['message_text'].split()) > 3:
            # message2 = await bot.send_media_group(chat_id=-1001527539668, media=group_elements)
            categories = get_categoriesv2(
                got_data['message_text'])
            phone = f"+{got_data['user_link']}" if '998' in got_data['user_link'] else ''
            if categories:
                txt = caption_or_message_text(
                    got_data=got_data, status="joylandi ✅", status2='1', media_files=group_elements, categories=categories, is_album=True)
                await bot.send_message(chat_id=-1001527539668, text=txt, reply_markup=await main_menu_keyboard(categories), disable_web_page_preview=False)
                await register_new_product_and_user(got_data=got_data, media_files=group_elements, phone_number=phone, categories=categories, datetime=datetime.now())
            else:
                txt = caption_or_message_text(got_data=got_data, media_files=group_elements, is_album=True,
                                              status="joylanmadi ❌", status2='0')
                await bot.send_message(chat_id=-1001527539668, text=txt, reply_markup=await main_menu_keyboard(categories), disable_web_page_preview=False)
                await register_new_product_and_user(got_data=got_data, media_files=group_elements, phone_number=phone, datetime=datetime.now(), status='0')

        pass
    else:
        if message.photo:
            # agar xabar photo bo'lsa:
            try:
                got_data = str_to_dict(message.caption)
            except:
                pass
            if len(got_data['message_text'].split()) > 3:
                categories = get_categoriesv2(
                    got_data['message_text'])
                phone = f"+{got_data['user_link']}" if '998' in got_data['user_link'] else ''
                if categories:
                    txt = caption_or_message_text(got_data=got_data, status="joylandi ✅", status2='1',
                                                  categories=categories, media_files=message.photo[0].file_id)
                    await bot.send_photo(chat_id=-1001527539668, caption=txt, reply_markup=await main_menu_keyboard(categories), photo=message.photo[0].file_id)
                    await register_new_product_and_user(got_data=got_data, media_files=message.photo[0].file_id, phone_number=phone, categories=categories, datetime=datetime.now())
                else:
                    txt = caption_or_message_text(got_data=got_data, status="joylanmadi ❌",
                                                  status2='0', media_files=message.photo[0].file_id)
                    await bot.send_photo(chat_id=-1001527539668, caption=txt, reply_markup=await main_menu_keyboard(categories), photo=message.photo[0].file_id)
                    await register_new_product_and_user(got_data=got_data, media_files=message.photo[0].file_id, phone_number=phone, datetime=datetime.now(), status='0')

        elif message.video:
            # agar xabar video bo'lsa:
            try:
                got_data = str_to_dict(message.caption)
            except:
                pass
            if len(got_data['message_text'].split()) > 3:
                categories = get_categoriesv2(
                    got_data['message_text'])
                phone = f"+{got_data['user_link']}" if '998' in got_data['user_link'] else ''
                if categories:
                    txt = caption_or_message_text(got_data=got_data, status="joylandi ✅", status2='1',
                                                  categories=categories, media_files=message.video.file_id)
                    await bot.send_video(chat_id=-1001527539668, caption=txt, reply_markup=await main_menu_keyboard(categories), video=message.video.file_id)
                    await register_new_product_and_user(got_data=got_data, media_files=message.video.file_id, phone_number=phone, categories=categories, datetime=datetime.now())
                else:
                    txt = caption_or_message_text(got_data=got_data, status="joylanmadi ❌",
                                                  status2='0', media_files=message.video.file_id)
                    await bot.send_video(chat_id=-1001527539668, caption=txt, reply_markup=await main_menu_keyboard(categories), video=message.video.file_id)
                    await register_new_product_and_user(got_data=got_data, media_files=message.video.file_id, phone_number=phone, datetime=datetime.now(), status='0')

        else:
            # agar xabar matn bo'lsa
            try:
                got_data = str_to_dict(message.text)
            except:
                pass
            if len(got_data['message_text'].split()) > 3:
                categories = get_categoriesv2(
                    got_data['message_text'])
                phone = f"+{got_data['user_link']}" if '998' in got_data['user_link'] else ''
                if categories:
                    txt = caption_or_message_text(
                        got_data=got_data, status="joylandi ✅", status2='1', categories=categories)
                    await bot.send_message(-1001527539668, txt, reply_markup=await main_menu_keyboard(categories), disable_web_page_preview=True)
                    await register_new_product_and_user(got_data=got_data, media_files='none', phone_number=phone, categories=categories, datetime=datetime.now())
                else:
                    txt = caption_or_message_text(got_data=got_data,
                                                  status="joylanmadi ❌", status2='0')
                    await bot.send_message(-1001527539668, txt, reply_markup=await main_menu_keyboard(categories), disable_web_page_preview=True)
                    await register_new_product_and_user(got_data=got_data, media_files='none', phone_number=phone, datetime=datetime.now(), status='0')


# @admin_router.message(CommandStart())
# async def admin_start(message: Message):
#     await message.reply("Привет, Админ!")
