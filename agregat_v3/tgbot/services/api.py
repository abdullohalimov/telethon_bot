import asyncio
import aiohttp
import json
import logging
import requests


def write_to_file(text, filename, encoding="utf-8"):
    # open the file with write mode
    with open(filename, "w", encoding=encoding) as f:
        # write the text to the file
        f.write(text)


async def register_new_product_and_user(
    phone_number, media_files, datetime, got_data: dict, categories=[], status="1"
):    
    url = "http://62.209.129.42/product/"
    logging.critical("product added")
    lisst = [] 
    for i in categories: 
        lisst.append(int(i))
    logging.critical(lisst)
    payload = json.dumps(
        {
            "product_user": {
                "user_id": int(got_data["user_id"]),
                "user_name": f"{got_data['user_name']}",
                "user_link": f"{got_data['user_link']}",
                "phone_number": f"{phone_number}",
            },
            "categories": lisst,
            "group": {
                "group_id": got_data["group_id"],
                "group_name": f"{got_data['group_name']}",
                "group_link": f"{got_data['group_link']}",
            },
            "message_id": int(got_data["message_id"]),
            "message_text": f"{got_data['message_text']}",
            "media_file": f"{media_files}",
            "datetime": str(datetime),
            # "status": status,
        }
    )
    headers = {"Content-Type": "application/json"}
    logging.error(payload)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            logging.critical("product added")
            try:
                logging.error(await response.json())
                return await response.json()
            except:
                logging.critical("An CRITICAL error occured while adding product")
            write_to_file(await response.text(), "last_error.txt")


async def delete_product(message_id, group_id):
    url = f"http://62.209.129.42/product/?group_id={group_id}&message_id={message_id}"

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            logging.critical("product deleted")
            return response.status


async def get_product(group_id, message_id):
    url = f"http://62.209.129.42/product/?group_id={group_id}&message_id={message_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            logging.critical("product fetched")
            return await response.json()


async def update_product(message_id, group_id, categories: list):
    url = f"http://62.209.129.42/update_by_group_id/?group_id={group_id}&message_id={message_id}"
    payload = json.dumps({"categories": categories})
    headers = {"Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, data=payload) as response:
            logging.critical("product updated")
            return await response.json()
