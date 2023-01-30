import json
import logging
import sys
import time
from typing import Optional

import requests
from constants import LAST_PAGE_TRESHOLD, MAX_PAGE

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def main() -> None:
    price_filter_url: str = (f'https://catalog.wb.ru/catalog/{shard}'
                             f'/v4/filters?appType=1&{query}&dest='
                             f'-1029256,-102269,-1304596,-1281263')
    response: dict = requests.get(price_filter_url).json()
    ctg_filters = response.get('data').get('filters')
    for ctg_filter in ctg_filters:
        if ctg_filter.get('key') == 'priceU':
            ctg_max_price: int = ctg_filter.get('maxPriceU') // 100
            break

    general_parser(item_id, shard, query, 0, ctg_max_price)

    for item in FAT_PRICE_RANGES:
        logger.debug('parsing by brand for %s %s, price range %s', *item)
        parse_by_brand(item_id, item)


def general_parser(item_id: str,
                   shard: str,
                   query: str,
                   min_pr: int,
                   max_pr: int) -> None:
    logger.debug('general parsing for %s %s, price range: %s;%s',
                 shard, query, min_pr, max_pr)

    price_lmt: str = f'&priceU={min_pr * 100};{max_pr * 100}'

    base_url: str = (f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1'
                     f'&{query}&dest=-1029256,-102269,-1304596,-1281263'
                     f'{price_lmt}')

    def check_last_page_is_full() -> bool:
        last_page_url: str = base_url + '&page=' + str(100)
        try:
            response = requests.get(last_page_url).json()
            response_data: dict = response.get('data').get('products')
            return len(response_data) > LAST_PAGE_TRESHOLD

        except json.decoder.JSONDecodeError:
            logger.debug('a JSONDecode error occured at: %s', last_page_url)
            check_last_page_is_full()

    if check_last_page_is_full():
        rnd_avg = round((max_pr + min_pr) // 2 + 1, -2)
        if rnd_avg - min_pr >= 200:
            general_parser(item_id, shard, query, min_pr, rnd_avg)
            general_parser(item_id, shard, query, rnd_avg, max_pr)
        else:
            FAT_PRICE_RANGES.append((shard, query, price_lmt))

    else:
        parse_through_pages(item_id, base_url)


def parse_by_brand(item_id: str, item: tuple):
    shard: str
    query: str
    price_lmt: str
    shard, query, price_lmt = item

    base_url: str = (f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1'
                     f'&{query}&dest=-1029256,-102269,-1304596,-1281263'
                     f'{price_lmt}')

    brand_filter_url: str = (f'https://catalog.wb.ru/catalog/{shard}/v4/'
                             f'filters?filters=fbrand&{query}&appType=1&dest='
                             f'-1029256,-102269,-1304596,-1281263{price_lmt}')
    response = requests.get(brand_filter_url).json()
    brand_filters: list[dict] = response.get(
        'data').get('filters')[0].get('items')

    concatenated_ids_list: list = []
    concatenated_ids: str = ''
    cnt: int = 1

    for brand in brand_filters:
        brand_id = brand.get('id')
        brand_count = brand.get('count')
        if brand_count > 500:
            concatenated_ids_list.append(str(brand_id))
        elif cnt < 20:
            concatenated_ids += str(brand_id) + ';'
            cnt += 1
        else:
            concatenated_ids_list.append(concatenated_ids[:-1])
            concatenated_ids = str(brand_id) + ';'
            cnt = 1

    concatenated_ids_list.append(concatenated_ids[:-1])

    number_of_requests: int = len(concatenated_ids_list)
    for idx, string in enumerate(concatenated_ids_list, 1):
        request_url: str = base_url + '&fbrand=' + string
        parse_through_pages(item_id, request_url)

        logger.debug('%d / %d requests done', idx, number_of_requests)


def parse_through_pages(item_id: str, base_url: str) -> None:
    for page in range(1, MAX_PAGE):

        def scrape_single_page(page: int) -> Optional[bool]:
            url: str = base_url + '&page=' + str(page)

            try:
                response = requests.get(url).json()
                response_data: dict = response.get('data').get('products')

                if len(response_data) == 0:
                    return False

                for item in response_data:
                    RESULT[item_id].append(item.get('id'))

            except json.decoder.JSONDecodeError:
                logger.debug('a JSONDecode error occured at: %s', url)
                scrape_single_page(page)

        continue_iteration: Optional[bool] = scrape_single_page(page)
        if continue_iteration is not None:
            break


if __name__ == '__main__':
    try:
        with open('catalogue_sh.json', 'r') as file:
            catalogue = json.load(file)
    except FileNotFoundError as error:
        logger.error(error, exc_info=True)

    RESULT: dict = {}
    FAT_PRICE_RANGES: list = []

    for item in catalogue:
        start: float = time.time()
        shard: str = item.get('shard')
        query: str = item.get('query')
        item_id: str = item.get('id')
        RESULT[item_id]: list = []

        if shard != 'blackhole':
            main()
        finish: float = time.time()
        impl_time: float = round(finish - start, 2)
        logger.info('parsed %s %s in %d seconds', shard, query, impl_time)

    with open('goods_ids_list.json', 'w') as file:
        json.dump(RESULT, file, indent="   ", ensure_ascii=False)
