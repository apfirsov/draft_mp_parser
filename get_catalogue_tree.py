import json

import requests
from constants import MAIN_MENU


def get_catalogue_tree(dictionary: dict) -> None:
    for item in dictionary:
        global RESULT
        RESULT.append({
            'id': item.get('id'),
            'name': item.get('name'),
            'parent': item.get('parent'),
            'landing': item.get('landing'),
            'seo': item.get('seo'),
            'url': item.get('url'),
            'shard': item.get('shard'),
            'query': item.get('query')
        })
        item_childs: dict = item.get('childs')
        if item_childs is not None:
            get_catalogue_tree(item_childs)


if __name__ == '__main__':
    RESULT: list = []
    catalogue_url: str = MAIN_MENU
    response: dict = requests.get(catalogue_url).json()

    get_catalogue_tree(response)

    with open('catalogue.json', 'w') as file:
        json.dump(RESULT, file, indent="   ", ensure_ascii=False)
