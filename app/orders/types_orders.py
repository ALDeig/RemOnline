import json

WORK_PATH = 'orders/types.json'
# WORK_PATH = 'app/orders/types.json'


def read_types() -> dict:
    with open(WORK_PATH, 'r', encoding='utf-8') as file:
        order_types = json.load(file)
    return order_types


def write_types(order_types: dict):
    with open(WORK_PATH, 'w', encoding='utf-8') as file:
        json.dump(order_types, file, ensure_ascii=False, indent=4)
    return True
