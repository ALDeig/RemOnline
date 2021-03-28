import json


def read_types() -> dict:
    with open('orders/types.json', 'r', encoding='utf-8') as file:
        order_types = json.load(file)
    return order_types


def write_types(order_types: dict):
    with open('orders/types.json', 'w', encoding='utf-8') as file:
        json.dump(order_types, file, ensure_ascii=False, indent=4)
    return True
