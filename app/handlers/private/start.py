from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Command

from app.loader import dp
from app.orders.create_message import hand_send
from app.keyboards.reply.check_order import keyboard


@dp.message_handler(CommandStart())
async def command_start_handler(msg: types.Message):
    await msg.answer(f'Hello, {msg.from_user.full_name}!', reply_markup=keyboard)
    print(msg.from_user.id)
    # await dp.bot.send_message(chat_id=-1001175182664, text='OK')


@dp.message_handler(text='Запустить проверки вручную')
async def send_orders(message: types.Message):
    await hand_send()
    await message.answer('Done')

