import json
import asyncio
import time


async def open_json():
    """Download file"""
    with open("wb.json", "r") as file:
        src = json.load(file)
    await asyncio.sleep(4)  # fat task
    print("open_json sleep 4 sec")
    return src


async def simple_task():
    """Any task"""
    await asyncio.sleep(3)
    print("simple_task sleep 3 sec")


async def mega_parser(src) -> dict:
    """Parser"""
    prod_list = []
    prod_details = {}

    for prod in src:
        prod_details[prod.get('prod_id')] = {
            "prod_id": prod.get('prod_id'),
            "name": prod.get('name'),
            "price": prod.get('price'),
            "seller": prod.get('seller'),
            "category": prod.get('category'),
            "rest_goods": prod.get('rest_goods'),
        }
    await asyncio.sleep(1)  # fat task
    print("mega_parser sleep 1 sec")

    prod_list.append(prod_details)
    print(prod_list)


async def main():
    """Async manager"""
    start = time.time()
    task = [
        asyncio.create_task(simple_task(), name="simple_task"),
        # ожидаем загрузки файла а потом "парсим"
        asyncio.create_task(mega_parser(await open_json()), name="parser")
    ]
    await asyncio.wait(task)
    print(f"Time of task {int(time.time() - start)} sec")

ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main())
ioloop.close()
