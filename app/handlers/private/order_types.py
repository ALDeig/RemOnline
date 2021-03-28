from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Command

from app.loader import dp
from app.orders import types_orders
from app.keyboards.inline.kb_types_orders import create_keyboard_types, types_order


@dp.message_handler(text='Изменить типы заказов')
async def send_types(message: types.Message):
    types_ = types_orders.read_types()
    keyboard = create_keyboard_types(types_)
    await message.answer(text='Выберите типы', reply_markup=keyboard)


@dp.callback_query_handler(types_order.filter())
async def change_types(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    types_ = types_orders.read_types()
    changed_type = callback_data.get('id_button')
    value = callback_data.get('value')
    new_value = 1 if value == '0' else 0
    types_[changed_type] = new_value
    keyboard = create_keyboard_types(types_)
    types_orders.write_types(types_)
    await call.message.edit_reply_markup(reply_markup=keyboard)

