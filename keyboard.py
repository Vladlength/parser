from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)  # default - False
list_brands = KeyboardButton('Список марок автомобилей')
start.add(list_brands)

# first_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# full_list = KeyboardButton('Смотреть все автомобили')
# first_keyboard.add(full_list)

inlineKB = InlineKeyboardMarkup(row_width=2)
inlineB1 = InlineKeyboardButton(text='Смотреть', callback_data='look')
inlineKB.add(inlineB1)

inlineKB_next = InlineKeyboardMarkup(row_width=3)
inlineB1 = InlineKeyboardButton(text='Следующие объявления', callback_data='next')
inlineKB_next.add(inlineB1)

back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
come_back = KeyboardButton('Вернуться в меню')
back_keyboard.add(come_back)