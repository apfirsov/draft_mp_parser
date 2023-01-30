import json
import logging
import sys
import time

import requests

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

MAX_GOODS_IN_REQUEST: int = 750
CARDS: list = []


def concatenate_ids(goods: dict) -> list[str]:
    concatenated_ids_list: list = []
    concatenated_ids: str = ''
    cnt: int = 0

    for goods_ids in goods.values():
        for good_id in goods_ids:
            if cnt < MAX_GOODS_IN_REQUEST:
                concatenated_ids += str(good_id) + ';'
                cnt += 1
            else:
                concatenated_ids_list.append(concatenated_ids[:-1])
                concatenated_ids = str(good_id) + ';'
                cnt = 0

        concatenated_ids_list.append(concatenated_ids[:-1])
    return concatenated_ids_list


def get_cards(idx: int, string: str) -> None:
    url: str = base_url + string
    response: dict = requests.get(url).json()
    products: list[dict] = response.get('data').get('products')

    for product in products:
        colors: list = [_.get('name') for _ in product.get('colors')]
        sizes: list[str] = []
        qty: int = 0
        sizes_raw: list = product.get('sizes')
        for size in sizes_raw:
            size_qty: int = 0
            for item in size.get('stocks'):
                item_qty = item.get('qty')
                if item_qty:
                    size_qty += item_qty
            qty += size_qty
            size_name = size.get('name')
            if size_name:
                sizes.append(size_name)

        card = {
            'id': product.get('id'),
            'name': product.get('name'),
            'brand': product.get('brand'),
            'brandId': product.get('brandId'),
            'sale': product.get('sale'),
            'price_full': product.get('priceU'),
            'price_with_discount': product.get('salePriceU'),
            'in_stock': qty,
            'rating': product.get('rating'),
            'colors': colors,
            'sizes': sizes
        }
        CARDS.append(card)

    logger.info('%d / %d requests done, got %d products',
                idx, number_of_requests, len(CARDS))


if __name__ == '__main__':
    with open('goods_ids_list.json', 'r') as file:
        goods: dict = json.load(file)

    # предполагаем, что принадлежность товара к дереву каталога уже присвоена,
    # поэтому просто беру все товары из goods_ids_list.json и иду по ним
    concatenated_ids_list: list[str] = concatenate_ids(goods)

    base_url: str = ('https://card.wb.ru/cards/detail?spp=30&appType=1'
                     '&dest=-1029256,-102269,-1304596,-1281263&nm=')

    number_of_requests: int = len(concatenated_ids_list)

    start: float = time.time()

    for idx, string in enumerate(concatenated_ids_list, 1):
        get_cards(idx, string)

    finish: float = time.time()
    impl_time: float = finish - start
    logger.info('done in %d seconds', impl_time)

    with open('product_cards.json', 'w') as file:
        json.dump(CARDS, file, indent="   ", ensure_ascii=False)
