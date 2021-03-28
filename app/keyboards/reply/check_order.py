from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(text='Запустить проверки вручную')],
    [KeyboardButton(text='Изменить типы заказов')]
], resize_keyboard=True)
