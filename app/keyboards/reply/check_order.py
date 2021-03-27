from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(text='Запустить проверки вручную')]
], resize_keyboard=True)
