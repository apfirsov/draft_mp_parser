import json
import logging
import sys
import time
from typing import Optional

import requests

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

LAST_PAGE_TRESHOLD: int = 95
MAX_PAGE: int = 101
FAT_PRICE_RANGES: list = []

RESULT: dict = {}


def main() -> None:
    # ctg_max_price - максимальная цена товара в обрабатываемом разделе
    # она будет нужна позже, но вычисляется сразу один раз и подается
    # на вход основного парсера general_parser(). Потому что general_parser
    # вызывает себя несколько раз рекурсивно, а я не хочу дергать ручку
    # лишний раз
    price_filter_url: str = (f'https://catalog.wb.ru/catalog/{shard}'
                             f'/v4/filters?appType=1&{query}&dest='
                             f'-1029256,-102269,-1304596,-1281263')
    response: dict = requests.get(price_filter_url).json()
    ctg_filters = response.get('data').get('filters')
    for ctg_filter in ctg_filters:
        if ctg_filter.get('key') == 'priceU':
            ctg_max_price: int = ctg_filter.get('maxPriceU') // 100
            break

    # первый шаг парсинга - эта функция
    general_parser(item_id, shard, query, 0, ctg_max_price)

    # второй шаг, про который рассказано в функции general_parser,
    # там где заполняется список FAT_PRICE_RANGES. Проблемные
    # запросы отправляются повторно, но на этом этапе они фильтруются
    # по брендам, чтобы уменьшить количество товаров
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

    # так как WB не дает парсить страницы выше 100, то если в разделе
    # более 10.000 товаров (по 100 товаров на странице), то получить их мы
    # не сможем. Для этого я разбиваю раздел на несколько запросов с разными
    # диапазонами цен. Первый запрос идет от 0 до максимальной цены, которую
    # мы получили ранее.
    price_lmt: str = f'&priceU={min_pr * 100};{max_pr * 100}'

    base_url: str = (f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1'
                     f'&{query}&dest=-1029256,-102269,-1304596,-1281263'
                     f'{price_lmt}')

    # сразу проверяю последнюю, сотую, страницу. Если она полная, значит я
    # сразу ухожу на дробление запроса по цене
    def check_last_page_is_full() -> bool:
        last_page_url: str = base_url + '&page=' + str(100)
        try:
            response = requests.get(last_page_url).json()
            response_data: dict = response.get('data').get('products')

            # страница может быть полной, но по какой-то причине в ответе
            # прилетает 99 товаров. То есть в любом случае мы получаем
            # какую-то погрешность. Чтобы ее обойти я считаю страницу
            # полной, если на ней более LAST_PAGE_TRESHOLD (сейчас он
            # равен 95) товаров
            return len(response_data) > LAST_PAGE_TRESHOLD

        # такая ошибка иногда ловится, валидный запрос не возвращает товары.
        # При повторном запросе все ок, поэтому эта ошибка просто логируется
        # и функция вызывает себя снова
        except json.decoder.JSONDecodeError:
            logger.debug('a JSONDecode error occured at: %s', last_page_url)
            check_last_page_is_full()

    if check_last_page_is_full():
        rnd_avg = round((max_pr + min_pr) // 2 + 1, -2)
        # если сотая страница полная, то функция запускается с
        # раздробленными диапазонами цен в запросе
        if rnd_avg - min_pr >= 200:
            general_parser(item_id, shard, query, min_pr, rnd_avg)
            general_parser(item_id, shard, query, rnd_avg, max_pr)
        else:
    # WB не позволяет сужать диапазон цен до любых значений. Минимальный
    # диапазон - 200 руб. Я столкнулся с проблемной категорией, где было
    # очень много товаров в минимально возможном диапазоне. Для этого ввел
    # второй шаг, который выполняется из функции main позже. Но на данном
    # этапе проблемный запрос сохраняется в список FAT_PRICE_RANGES
            FAT_PRICE_RANGES.append((shard, query, price_lmt))

    else:
        # если все ок и в выдаче менее 10.000 товаров - идем дальше
        # и итерируемся по страницам от 1 до 100
        parse_through_pages(item_id, base_url)


def parse_by_brand(item_id: str, item: tuple):
    shard: str
    query: str
    price_lmt: str
    shard, query, price_lmt = item

    base_url: str = (f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1'
                     f'&{query}&dest=-1029256,-102269,-1304596,-1281263'
                     f'{price_lmt}')

    # тут я собираю бренды, по которым можно фильтровать запрос,
    # который в первом шаге оказался проблемным
    brand_filter_url: str = (f'https://catalog.wb.ru/catalog/{shard}/v4/'
                             f'filters?filters=fbrand&{query}&appType=1&dest='
                             f'-1029256,-102269,-1304596,-1281263{price_lmt}')
    response = requests.get(brand_filter_url).json()
    brand_filters: list[dict] = response.get(
        'data').get('filters')[0].get('items')

    # задача этого блока - собрать строки запросов, в которых было бы не
    # более 20 брендов (ограничение WB) и чтобы по этому запросу возвращалось
    # не более 10.000 товаров. Для этого я выношу бренды, у которых более 500
    # товаров в отдельные запросы, остальные - соединяю в строку по 20 брендов.
    # На выходе - список строк с параметром запроса concatenated_ids_list
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

    # здесь я добавляю собранные строки запросов в урл и отправляю
    # запрос в уже использованную ранее функцию, которая проходит
    # по всем страницам выдачи. Так как в запросе не более 20 брендов,
    # у которых не более 500 товаров, то ихне может быть более 10.000,
    # и проверку на "заполненность" последней страницы я не применяю
    number_of_requests: int = len(concatenated_ids_list)
    for idx, string in enumerate(concatenated_ids_list, 1):
        request_url: str = base_url + '&fbrand=' + string
        parse_through_pages(item_id, request_url)

        logger.debug('%d / %d requests done', idx, number_of_requests)


def parse_through_pages(item_id: str, base_url: str) -> None:
    for page in range(1, MAX_PAGE):

        # тут я применил вложенную функцию, так как она постоена
        # на рекурсивной основе из-за ошибки JSONDecodeError, про
        # которую я писал ранее
        def scrape_single_page(page: int) -> Optional[bool]:
            url: str = base_url + '&page=' + str(page)

            try:
                response = requests.get(url).json()
                response_data: dict = response.get('data').get('products')

                # если товаров на страницы нет, то функция
                # возвращает False и ниже переменная continue_iteration
                # этот момент мониторит: если товары закончились,
                # внешний цикл range(1, MAX_PAGE) прерывается
                if len(response_data) == 0:
                    return False

                for item in response_data:
                    # тут заполняется результирующий файл
                    RESULT[item_id].append(item.get('id'))

            except json.decoder.JSONDecodeError:
                logger.debug('a JSONDecode error occured at: %s', url)
                scrape_single_page(page)

        continue_iteration: Optional[bool] = scrape_single_page(page)
        if continue_iteration is not None:
            break


if __name__ == '__main__':
    # входные данные - джейсон, который собирается в модуле get_catalog_tree
    # с разделами и подразделами. catalogue_sh.json - тестовый файл, в
    # котором только 3 тестовые подкатегории.
    with open('catalogue_sh.json', 'r') as file:
        catalogue = json.load(file)

    for item in catalogue:
        start: float = time.time()
        shard: str = item.get('shard')
        query: str = item.get('query')
        item_id: str = item.get('id')
        RESULT[item_id]: list = []

        # если у раздела нет товаров, его shard == blackhole, поэтому
        # такие исключаем
        if shard != 'blackhole':
            # точка входа - функция main
            main()
        finish: float = time.time()
        impl_time: float = round(finish - start, 2)
        logger.info('parsed %s %s in %d seconds', shard, query, impl_time)

    # результат работы модуля - словарь RESULT, у которого ключи - айди
    # подразделов, а значения - список айдишников товаров. Когда парсинг
    # закончен, словарь записывается в файл
    with open('goods_ids_list.json', 'w') as file:
        json.dump(RESULT, file, indent="   ", ensure_ascii=False)
