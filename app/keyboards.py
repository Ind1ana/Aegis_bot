from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Задать вопрос')],
    [KeyboardButton(text='Поддержать')]
],
resize_keyboard=True,
input_field_placeholder='Выберите пункт меню.')

name = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать обращение', callback_data='name')],

])