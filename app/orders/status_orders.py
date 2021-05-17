import json
from datetime import datetime, date, time
import pytz
import re

from loguru import logger
import requests
from pydantic import BaseModel, ValidationError, Field

from app import config

# WORK_PATH = 'orders/types.json'
WORK_PATH = 'app/orders/types.json'
TZ = pytz.timezone('Europe/Moscow')


class Orders(BaseModel):
    id: str
    done_at: str = None
    status_deadline: str = None
    created_at: str
    status: dict
    custom_fields: dict
    id_label: str


class ListOrders(BaseModel):
    data: list[Orders]
    count_orders: int = Field(alias='count')


def get_token():
    page_token = requests.post('https://api.remonline.ru/token/new', {'api_key': config.API_KEY}).json()
    try:
        token = page_token.get('token')
    except Exception as e:
        logger.error(e)
        return
    return token


def get_page_orders(page: int, token: str, statuses: list):
    types_ = get_types()
    orders_row = requests.get('https://api.remonline.ru/order/',
                              {"token": token, 'statuses[]': statuses, 'types[]': types_, 'page': page})
    if orders_row.status_code != 200:
        return 'token_invalid'
    try:
        orders = ListOrders.parse_raw(orders_row.text)
    except ValidationError as e:
        logger.error(f'Exception: {e}')
        return
    return orders


def get_count_pages(count_orders: int):
    count_pages = int(count_orders / 50) + 1
    return count_pages


def check_date_today(date_check):
    if date_check is None:
        return False
    get_date = map(int, date_check.split('.'))
    need_date = date(day=next(get_date), month=next(get_date), year=next(get_date))
    if need_date != date.today():
        return False
    return True


def check_date_passed(date_check):
    if date_check is None:
        return False
    get_date = map(int, date_check.split('.'))
    need_date = date(day=next(get_date), month=next(get_date), year=next(get_date))
    if need_date < date.today():
        return False
    return True


def check_date_tomorrow(date_row):
    if date_row is None:
        return False
    list_date = map(int, date_row.split('.'))
    check_date = date(day=next(list_date), month=next(list_date), year=next(list_date))
    if check_date < date.today():
        return False
    return True


# def check_in_interval(interval_row):
#     if interval_row is None:
#         return False
#     interval = re.findall(r'\d+:\d+', interval_row)
#     now = datetime.now(tz=TZ).time()
#     try:
#         min_time = map(int, interval[0].split(':'))
#         max_time = map(int, interval[-1].split(':'))
#         if time(next(min_time), next(min_time)) < now < time(next(max_time), next(max_time)):
#             return True
#     except Exception as e:
#         logger.error(e)
#         return False
#     return False


def check_out_interval(interval_row):
    if interval_row is None:
        return False
    interval = re.findall(r'\d+:\d+', interval_row)
    now = datetime.now(tz=TZ).time()
    try:
        max_time = map(int, interval[-1].split(':'))
        valid_time = time(next(max_time), next(max_time))
        if now > valid_time:
            return False
    except Exception as e:
        logger.error(e)
        return False
    return True


def check_time(done_at):
    if done_at is None:
        return False
    done_time = datetime.fromtimestamp(int(done_at[:10]))
    done_time = datetime(year=done_time.year,
                         month=done_time.month,
                         day=done_time.day,
                         hour=done_time.hour,
                         minute=done_time.minute)

    now = datetime.now(tz=TZ)
    now = datetime(year=now.year,
                   month=now.month,
                   day=now.day,
                   hour=now.hour,
                   minute=now.minute)
    if done_time != now:
        return False
    return True


def join_message(status: str, messages: list):
    result = list()
    new_message = f'<b>{status}</b>\n\n\n'
    if len(messages) == 0:
        return [new_message.strip() + ' - нарушений нет.']
    cnt = 1
    for message in messages:
        new_message += message + '\n\n'
        if cnt % 20 == 0:
            result.append(new_message)
            new_message = f'<b>{status}</b>\n\n\n'
        cnt += 1
    if new_message:
        result.append(new_message)
    return result


def get_types():
    with open(WORK_PATH, 'r', encoding='utf-8') as file:
        types_ = json.load(file)
    result = [int(key) for key, value in types_.items() if value == 1]
    return result


def status_435390():
    """
    Водитель назначен. Привоз
    Проверка каждые 2 часа.
    """
    result = list()
    statuses = [435390]
    token = get_token()
    cnt = 1
    pages = 1
    while cnt <= pages:
        orders = get_page_orders(cnt, token, statuses)
        if orders == 'token_invalid':
            token = get_token()
            orders = get_page_orders(cnt, token, statuses)
        for order in orders.data:
            custom_fields = order.custom_fields
            check_date = check_date_today(custom_fields.get('f1482265'))
            check_interval = check_out_interval(custom_fields.get('f1620345'))
            if not check_interval or not check_date:
                result.append(
                    f'<b>Заказ №</b>: {order.id_label}\n'
                    f'<b>Статус</b>: {order.status.get("name")}\n'
                    f'<b>Тип курьера</b>: {order.custom_fields.get("f1620346")}\n'
                    f'<b>Курьер</b>: {custom_fields.get("f1482267")}\n'
                    f'<b>Дата привоза</b>: {custom_fields.get("f1482265") if check_date else "Нарушение"}\n'
                    f'<b>Интервалы привоза</b>: {custom_fields.get("f1620345") if check_interval else "Нарушение"}\n'
                    f'<b>Интервал:</b> {custom_fields.get("f1620345")}'
                )
        pages = get_count_pages(orders.count_orders)
        cnt += 1
    messages = join_message('1. Водитель назначен.Привоз', result)
    return messages

print(*status_435390(), sep='\n')

def status_323199():
    """
    Привоз назначен и Привоз назначен. Выезд
    Проверка каждые 10 минут 65819312edc03520c7967088a31f9a128330a162
    """
    statuses = [323199, 338355]
    result = list()
    token = get_token()
    cnt = 1
    pages = 1
    while cnt <= pages:
        orders = get_page_orders(cnt, token, statuses)
        if orders == 'token_invalid':
            token = get_token()
            orders = get_page_orders(cnt, token, statuses)
        for order in orders.data:
            custom_fields = order.custom_fields
            if custom_fields.get("f3592120") == 'Нет' or custom_fields.get("f3592120") is None:
                result.append(
                    f'<b>Заказ №</b>: {order.id_label}\n'
                    f'<b>Статус</b>: {order.status.get("name")}\n'
                    f'<b>Заказ подтверждён</b>: Нет'
                )
        pages = get_count_pages(orders.count_orders)
        cnt += 1
    messages = join_message('2. Подтверждение', result)
    return messages


def status_435391():
    """
    Водитель назначен. Отвоз
    Проверка 4 раза: 1. в 14:00, 2. в 16:00, 3. в 12:00, 4. в 20:00
    """
    statuses = [435391]
    result = list()
    token = get_token()
    cnt = 1
    pages = 1
    while cnt <= pages:
        orders = get_page_orders(cnt, token, statuses)
        if orders == 'token_invalid':
            token = get_token()
            orders = get_page_orders(cnt, token, statuses)
        for order in orders.data:
            custom_fields = order.custom_fields
            check_time_order = check_out_interval(custom_fields.get("f2045048"))
            if not check_time_order:
                result.append(
                    f'<b>Заказ №</b>: {order.id_label}\n'
                    f'<b>Статус</b>: {order.status.get("name")}\n'
                    f'<b>Дата отвоза:</b> {custom_fields.get("f1569111")}\n'
                    f'<b>Интервалы доставки</b>: Нарушение\n'
                    f'Интервал фактически: {custom_fields.get("f2045048")}\n'
                    f'<b>Курьер отвоза:</b> {custom_fields.get("f1569113")}'
                )
        pages = get_count_pages(orders.count_orders)
        cnt += 1
    messages = join_message('3. Водитель назначен.Отвоз', result)
    return messages


def status_960847():
    """
    Проблемная доставка
    Проверка 4 раза в день. 1. 9:00, 2. 13:00, 3. 17:00, 4. 21:00
    """
    statuses = [960847]
    result = list()
    token = get_token()
    cnt = 1
    pages = 1
    while cnt <= pages:
        orders = get_page_orders(cnt, token, statuses)
        if orders == 'token_invalid':
            token = get_token()
            orders = get_page_orders(cnt, token, statuses)
        for order in orders.data:
            custom_fields = order.custom_fields
            result.append(
                f'<b>Заказ №</b>: {order.id_label}\n'
                f'<b>Статус</b>: {order.status.get("name")}\n'
                f'<b>Курьер отвоза:</b> {custom_fields.get("f1569113")}\n'
                f'<b>Тип изделия:</b> {custom_fields.get("f1070009")}\n'
                f'<b>Сумма:</b> {custom_fields.get("f")}'  # ?
            )
        pages = get_count_pages(orders.count_orders)
        cnt += 1
    messages = join_message('4. Проблемная доставка', result)
    return messages


def status_324942():
    """
    Забрал обрудование
    Проверка 5 раз в день: 1. 9:00, 2. 13:00, 3. 17:00, 4. 21:00, 5. 23:00
    """
    result = list()
    statuses = [324942]
    token = get_token()
    cnt = 1
    pages = 1
    while cnt <= pages:
        orders = get_page_orders(cnt, token, statuses)
        if orders == 'token_invalid':
            token = get_token()
            orders = get_page_orders(cnt, token, statuses)
        for order in orders.data:
            custom_fields = order.custom_fields
            check_date = check_date_tomorrow(custom_fields.get('f1482265'))
            if not check_date:
                result.append(
                    f'<b>Заказ №</b>: {order.id_label}\n'
                    f'<b>Статус</b>: {order.status.get("name")}\n'
                    f'<b>Курьер</b>: {custom_fields.get("f1482267")}\n'
                    f'<b>Дата привоза</b>: {custom_fields.get("f1482265")}'
                )
        pages = get_count_pages(orders.count_orders)
        cnt += 1
    messages = join_message('5. Забрал', result)
    return messages


def status_355259():
    """
    Доставка.Октябрьское поле
    Проверка 2 раза: 1. 17:00, 2. 22:00
    """
    result = list()
    statuses = [355259]
    token = get_token()
    cnt = 1
    pages = 1
    while cnt <= pages:
        orders = get_page_orders(cnt, token, statuses)
        if orders == 'token_invalid':
            token = get_token()
            orders = get_page_orders(cnt, token, statuses)
        for order in orders.data:
            custom_fields = order.custom_fields
            check_date = check_date_today(custom_fields.get('f1482265'))
            if check_date or custom_fields.get('f1482265') is None:
                result.append(
                    f'<b>Заказ №</b>: {order.id_label}\n'
                    f'<b>Статус</b>: {order.status.get("name")}\n'
                    f'<b>Дата отвоза:</b> {custom_fields.get("f1569113") or "Неуказана"}\n'
                    f'<b>Курьер отвоза:</b> {custom_fields.get("f1569111") or "Неуказан"}'
                )
        pages = get_count_pages(orders.count_orders)
        cnt += 1
    messages = join_message('6. Доставка. Октябрьское поле', result)
    return messages


def status_349784():
    """
    Отдал товар
    Проверка 2 раза: 1. 17:00, 2. 22:00
    """
    result = list()
    statuses = [349784]
    token = get_token()
    cnt = 1
    pages = 1
    while cnt <= pages:
        orders = get_page_orders(cnt, token, statuses)
        if orders == 'token_invalid':
            token = get_token()
            orders = get_page_orders(cnt, token, statuses)
        for order in orders.data:
            custom_fields = order.custom_fields
            check_date = check_date_today(custom_fields.get('f1569111'))
            if not check_date:
                result.append(
                    f'<b>Заказ №</b>: {order.id_label}\n'
                    f'<b>Статус</b>: {order.status.get("name")}\n'
                    f'<b>Дата отвоза</b>: {custom_fields.get("f1569111")}\n'
                    f'<b>Курьер отвоза</b>: {custom_fields.get("f1569113")}'
                )
        pages = get_count_pages(orders.count_orders)
        cnt += 1
    messages = join_message('7. Отдал товар', result)
    return messages


def status_349471():
    """
    СКК. Не выходит на связь📵, СКК. Клиент сливается🚽, СКК. Подтверждение доставки✔️, СКК. Уточнение интервала🕙,
    СКК. Уточнение адреса❓, СКК. Уточнение км от МКАД🌉
    Проверка каждый час
    """
    result = list()
    statuses = [349471, 349470, 349473, 349472, 349474, 349475]
    token = get_token()
    cnt = 1
    pages = 1
    while cnt <= pages:
        orders = get_page_orders(cnt, token, statuses)
        if orders == 'token_invalid':
            token = get_token()
            orders = get_page_orders(cnt, token, statuses)
        for order in orders.data:
            custom_fields = order.custom_fields
            if not check_time(order.done_at):
                result.append(
                    f'<b>Заказ №</b>: {order.id_label}\n'
                    f'<b>Статус</b>: {order.status.get("name")}\n'
                    f'<b>Дата отвоза</b>: {custom_fields.get("f1569111")}\n'
                    f'<b>Курьер отвоза</b>: {custom_fields.get("f1569113")}'
                )
        pages = get_count_pages(orders.count_orders)
        cnt += 1
    messages = join_message('8. СКК', result)
    return messages


def status_325119():
    """Запрос в закупку	Поле "Просрочено" если есть значение, оно и является нарушением"""
    statuses = [325119]
    result = list()
    token = get_token()
    cnt = 1
    pages = 1
    while cnt <= pages:
        orders = get_page_orders(cnt, token, statuses)
        if orders == 'token_invalid':
            token = get_token()
            orders = get_page_orders(cnt, token, statuses)
        for order in orders.data:
            custom_fields = order.custom_fields
            if order.status_deadline and datetime.fromtimestamp(int(order.status_deadline[:10])) < datetime.now():
                deadline_time = datetime.fromtimestamp(int(order.status_deadline[:10]))
                deadline = datetime.now() - deadline_time
                days = divmod(deadline.total_seconds(), (3600 * 24))
                hours = divmod(days[1], 3600)[0]
                result.append(
                    f'<b>Заказ №</b>: {order.id_label}\n'
                    f'<b>Статус</b>: {order.status.get("name")}\n'
                    f'<b>Просрочено</b>:\nДней - {int(days[0])} Часов - {int(hours)}'
                )
        pages = get_count_pages(orders.count_orders)
        cnt += 1
    messages = join_message('9. Запрос в закупку', result)
    return messages


def status_324856():
    """
    Предварительный заказ ЗЧ, Ожидаются запчасти
    Проверка 2 раза: 1. 9:00, 2. 19:00
    """
    statuses = [324856, 323209]
    result = list()
    token = get_token()
    cnt = 1
    pages = 1
    while cnt <= pages:
        orders = get_page_orders(cnt, token, statuses)
        if orders == 'token_invalid':
            token = get_token()
            orders = get_page_orders(cnt, token, statuses)
        for order in orders.data:
            custom_fields = order.custom_fields
            check_date = check_date_passed(custom_fields.get('f1465924'))
            count_transfers = custom_fields.get('f2055930')
            count_transfers = count_transfers if count_transfers else 0
            if not check_date or count_transfers > 3:
                result.append(
                    f'<b>Заказ №</b>: {order.id_label}\n'
                    f'<b>Статус</b>: {order.status.get("name")}\n'
                    f'<b>Дата поставки запчастей</b>: {custom_fields.get("f1465924") or "Неуказана"}\n'
                    f'<b>Количество переносов</b>: {count_transfers}'
                )
        pages = get_count_pages(orders.count_orders)
        cnt += 1
    messages = join_message('10. Ожидаются запчасти', result)
    return messages
