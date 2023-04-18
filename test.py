import requests
import json

def get_catalog(catalog = 0, lan = 'uz_latn', c = ''):
    payload={}
    headers = {
        'content-type': 'application/json',
        'lan': f'{lan}'
    }

    if c == '':
        if catalog == 0:
            url = "https://aztester.uz/api-announcement/v1/category/tree"
            response = requests.request("GET", url, headers=headers, data=payload)
            categories = dict()
            for i in response.json()['data']:
                categories[i['id']] = i['name']

            return categories
        else:
            url = f'https://aztester.uz/api-announcement/v1/category?category_id={catalog}'
            response = requests.request("GET", url, headers=headers, data=payload)
            for i in response.json()['data'][0]['child_categories']:
                categories[i['id']] = i['name']


            return categories
    else:
        url = f"https://aztester.uz/api-announcement/v1/category/breadcrumb?categories={c}"
        response = requests.request("GET", url, headers=headers, data=payload)

        category_id = response.json()['data']['categories'][0]['category_id']
        name = f"{response.json()['data']['categories'][0]['name']}"

        aa = ''
        try:
            aa = get_catalog(c=category_id)
        except: pass

        cat = f"{name}:>:{category_id}:>:{aa}"
        if category_id == None:
            return name
        else:
            return cat
        
