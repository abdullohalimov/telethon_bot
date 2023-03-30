import asyncio
import aiohttp
import json


async def register_new_product_and_user(user_id, user_name, categories, group_id, group_name, group_link, message_id, message_text, media_file, datatime, status):
    url = "http://62.209.129.42/product/"

    payload = json.dumps({
    "product_user": {
        "user_id": user_id,
        "user_name": f"{user_name}"
    },
    "category": categories,
    "group_id": group_id,
    "group_name": f"{group_name}",
    "group_link": f"{group_link}",
    "message_id": message_id,
    "message_text": f"{message_text}",
    "media_file": f"{media_file}",
    "datatime": datatime,
    "status": status
    })
    headers = {
    'Content-Type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            print(await response.text())

    # asyncio.run(send_request())

# asyncio.run(register_new_product_and_user(1123123131321, 'user_name', [1148], 45646, 'group_name', 'group_link', 987546, 'message_text', 'media_file', 465465, True))