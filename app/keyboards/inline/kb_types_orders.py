from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

types_order = CallbackData('types', 'value', 'id_button')

name_types = {'104613': "3. БТ ВЫЕЗД", '107941': "4. ДОП_ДОСТАВКА", '115231': "5. Продажа запчастей",
              '89790': "1. ЗАКАЗ", '90261': "2. ЗАКАЗ/ГАРАНТИЯ", '128501': "8. Технический",
              '136945': "6. ЗАКАЗ. ПРОБЛЕМА"}

emoji = {1: '✔️', 0: '❌'}


def create_keyboard_types(order_types: dict):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for key, value in order_types.items():
        keyboard.add(InlineKeyboardButton(text=f'{name_types.get(key)}{emoji.get(value)}',
                                          callback_data=types_order.new(value=value, id_button=key)))
    return keyboard
