import logging
import requests
import json
from pprint import pprint
import aiohttp


async def get_catalog_async(catalog=0, lan='uz_latn', c=''):
    payload={}
    headers = {
        'content-type': 'application/json',
        'lan': f'{lan}'
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        if c == '':
            if catalog == 0:
                url = "http://37.140.216.224/category/"
                async with session.get(url, data=payload) as response:
                    categories = dict()
                    for i in (await response.json())['categories']:
                        categories[i['id']] = i['name']
                    return [categories, 0]
            else:
                url = f'http://37.140.216.224/catagory_name/?id={catalog}'
                async with session.get(url, data=payload) as response:
                    categories = dict()
                    for i in (await response.json())['categories']:
                        categories[i['id']] = i['name']
                    return [categories, catalog]
        else:
            url = f"http://37.140.216.224/catagory_name/?id={c}"

            async with session.get(url, data=payload) as response:
                category_name = (await response.json())['category_name']
                category_id = c
                cat = f"{category_name}:>:{category_id}"
                logging.warning(cat)
                return cat
            #     pprint((await response.json())['data']['categories'][0])
            #     category_id2 = (await response.json())['data']['categories'][0]['id']
            #     name = f"{(await response.json())['data']['categories'][0]['name']}"
            #     aa = ''
            #     try:
            #         aa = await get_catalog_async(c=category_id)
            #     except:
            #         pass
            #     if category_id == None:
            #         return name
            #     else:

# pprint(get_catalog(705, 'uz_latn', ''))