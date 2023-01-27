# Собирает айдишники товаров для одной из категорий нижнего уровня.
# На вход функции подается связка shard + query.
# Для примера в блоке name == main взята категория, в которой 50 тыс товаров.
# В качестве результата на печать выводится длина собранного список,
# а также длина множества, полученного из этого списка (то есть убраны
# дубликаты). По идее они не должны различаться, но отличие есть, хоть и
# небольшое.

import json
import time
from typing import Optional
import requests

MAX_PAGE: int = 101
GOODS_QTY_LIMIT: int = 10000


def get_goods_ids(shard: str, query: str,
                  min_pr: int = 0, max_pr: int = 0) -> None:
    print(f'start parse_items iteration with price range: {min_pr};{max_pr}')
    current_goods_list: list = []
    price_lmt: str = f'&priceU={min_pr * 100};{max_pr * 100}' if max_pr else ''

    base_url: str = (f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1'
                     f'&{query}&dest=-1029256,-102269,-1304596,-1281263'
                     f'{price_lmt}&page=')

    price_filter_url: str = (f'https://catalog.wb.ru/catalog/{shard}/v4/'
                             f'filters?appType=1&{query}'
                             f'&dest=-1029256,-102269,-1304596,-1281263')

    for page in range(1, MAX_PAGE):

        def scrape_page(page: int) -> Optional[bool]:
            nonlocal base_url
            nonlocal current_goods_list
            items_count_at_start: int = len(current_goods_list)
            url: str = base_url + str(page)

            try:
                response = requests.get(url).json()
                response_data: dict = response.get('data').get('products')

                for item in response_data:
                    current_goods_list.append(item.get('id'))

                if len(current_goods_list) == items_count_at_start:
                    return False

            except json.decoder.JSONDecodeError:
                print(f'a JSONDecode error occured at: {url}')
                scrape_page(page)

        continue_iteration: Optional[bool] = scrape_page(page)
        if continue_iteration is not None:
            break

    if len(current_goods_list) < GOODS_QTY_LIMIT:
        GOODS.extend(current_goods_list)
        return
    else:
        response: dict = requests.get(price_filter_url).json()
        ctg_max_price: int = (response.get('data').get('filters')
                              [4].get('maxPriceU') // 100)
        for i in range(0, ctg_max_price, ctg_max_price // 100):
            get_goods_ids(shard, query, i, i + ctg_max_price // 100)


if __name__ == '__main__':
    start = time.time()
    GOODS: list = []
    shard = 'men_clothes1'
    query = 'cat=63011'

    get_goods_ids(shard, query)

    print(f'GOODS LIST qty: {len(GOODS)}')
    GOODS_SET = set(GOODS)
    print(f'GOODS SET qty: {len(GOODS_SET)}')
    finish = time.time()
    print(f'implementation time: {round(finish - start, 2)} sec')
