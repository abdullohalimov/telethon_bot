import requests
import json
from pprint import pprint

def get_catalog(catalog = 0, lan = 'uz_latn', c = ''):
    payload={}
    headers = {
        'content-type': 'application/json',
        'lan': f'{lan}'
    }

    if c == '':
        if catalog == 0:
            url = "http://62.209.129.42/category/"
            response = requests.request("GET", url, headers=headers, data=payload)
            categories = dict()
            for i in response.json()['categories']:
                print(i['id'], i['name'])
                categories[i['id']] = i['name']

            # return response.json()['data']
            return [categories, 0]
        else:
            url = f'http://62.209.129.42/catagory_name/?id={catalog}'
            response = requests.request("GET", url, headers=headers, data=payload)
            categories = dict()
            for i in response.json()['categories']:
                print(i['id'], i['name'])
                categories[i['id']] = i['name']

            # return response.json()['data'][0]['child_categories']
            return [categories, catalog]
    else:
        url = f"http://62.209.129.42/catagory_name/?id={c}"
        response = requests.request("GET", url, headers=headers, data=payload)
        #pprint(response.json()['data']['categories'][0])

        category_id = response.json()['data']['categories'][0]['category_id']
        category_id2 = response.json()['data']['categories'][0]['id']
        name = f"{response.json()['data']['categories'][0]['name']}"

        # aa = ''
        # try:
        #     aa = get_catalog(c=category_id)
        # except: pass

        cat = f"{name}:>:{category_id2}:>:{aa}"
        if category_id == None:
            return name
        else:
            return cat
        
# pprint(get_catalog(705, 'uz_latn', ''))