from aiogram.utils import executor
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram import Bot, types
from math import ceil
import config
import keyboard
import logging
import parser_for_bot

storage = MemoryStorage()  # хранилище состояний

bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)  # инициализируем бота
dp = Dispatcher(bot, storage=storage)  # инициализируем диспатчер к нащему боту

with open('log.txt', 'w') as f:  # очищаем логи
    pass

logging.basicConfig(filename='log.txt',
                    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)  # включаем логирование


class Me_info(StatesGroup):
    zero_state = State()
    first_state = State()  # задаем состояние 1
    second_state = State()  # задаем состояние 2
    third_state = State()


async def on_startup_(_):
    print('бот запущен')


response_for_count = None


@dp.message_handler(Command('start'), state=None)  # указываем боту на какую команду надо реагировать
async def welcome(message: types.Message):
    with open("user.txt", "r") as JoinedFile:
        # создаем множество из ид пользователей
        JoinedUsers = set()
        for line in JoinedFile:
            JoinedUsers.add(line.strip())

    if not str(message.chat.id) in JoinedUsers:  # если в множестве нет ид этого пользователя
        # дописываем его в файл и в множество
        with open("user.txt", "a") as JoinedFile:
            JoinedFile.write(str(message.chat.id) + '\n')
            JoinedUsers.add(message.chat.id)

    await bot.send_sticker(message.chat.id,
                           sticker='CAACAgIAAxkBAAEI97VkX4FYcaOmu8Gn4Q1iaZOQysD0ywACCQAD7oG0D59YD8ib1v_PLwQ')
    # бот отправляет стикер (с указанным ID) в чат message.chat.id. ID стикера - Get Sticker ID
    await bot.send_message(message.chat.id, f"ПРИВЕТ, *{message.from_user.first_name}, *БОТ РАБОТАЕТ",
                           reply_markup=keyboard.start, parse_mode="Markdown")
    await Me_info.zero_state.set()


# -------state none выбор марки
@dp.message_handler(text='Список марок автомобилей', state=Me_info.zero_state)
async def get_car_brands(message: types.Message):
    global response_for_count
    response_for_count = await parser_for_bot.get_list_car_brands()
    str_brands = '\n'.join(response_for_count)
    await message.answer('Введите номер интересующей вас марки')
    await message.answer(text=str_brands)
    await Me_info.first_state.set()


# --------first_state выбор модели
# @dp.message_handler(text='Вернуться на шаг назад', state=Me_info.first_state)
# async def come_back(message: types.Message, state: FSMContext):
#     await bot.send_message(message.chat.id, 'Вы вернулись на шаг назад',
#                            reply_markup=keyboard.start)
#     await Me_info.zero_state.set()


@dp.message_handler(lambda mes: mes.text.isdigit(),
                    lambda message: int(message.text.strip()) in [i for i in range(1, len(response_for_count) + 1)],
                    state=Me_info.first_state)
async def get_brand_page(message: types.Message, state: FSMContext):
    response = await parser_for_bot.get_list_car_brands()
    obj_brand = response[int(message.text) - 1].strip(f'{int(message.text)}: ')
    link, count = await parser_for_bot.get_link_brand(obj_brand)
    await state.update_data(answer1=link)
    await message.answer(f'Найдено: {count} объявлений')
    content = await state.get_data()
    global response_for_count
    response_for_count = await parser_for_bot.get_list_car_brands(content['answer1'])
    str_models = '\n'.join(response_for_count)
    await message.answer('Введите номер интересующей вас модели', reply_markup=keyboard.back_keyboard)
    await message.answer(text=str_models)
    await Me_info.second_state.set()


# --------second_state вывод информации по моделям машин

@dp.message_handler(text='Вернуться в меню', state=Me_info.second_state)
async def come_back(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Вы вернулись в меню',
                           reply_markup=keyboard.start)
    await Me_info.zero_state.set()


@dp.message_handler(lambda mes: mes.text.isdigit(),
                    lambda message: int(message.text.strip()) in [i for i in range(1, len(response_for_count) + 1)],
                    state=Me_info.second_state)
async def get_inf_cars(message: types.Message, state: FSMContext):
    content = await state.get_data()
    response = await parser_for_bot.get_list_car_brands(content['answer1'])
    obj_brand = response[int(message.text) - 1].strip(f'{int(message.text)}: ')
    link, count = await parser_for_bot.get_link_brand(obj_brand, content['answer1'])
    link = 'https://cars.av.by' + link
    await state.update_data(answer2=link)
    await message.answer(f'Найдено {count} объявлений', reply_markup=keyboard.inlineKB)

    # await message.answer(reply_markup=keyboard.back_keyboard)
    await Me_info.third_state.set()


# -----------------------third_state вывод информации пользователю
@dp.message_handler(text='Вернуться в меню', state=Me_info.third_state)
async def come_back(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Вы вернулись в меню',
                           reply_markup=keyboard.start)
    await Me_info.zero_state.set()


@dp.callback_query_handler(state=Me_info.third_state)
async def vote_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'look':
        flag = False
        content = await state.get_data()
        link = content['answer2']
        try:
            button = await parser_for_bot.parse_button_link(link)
            button = button.replace('page=2', 'page=1')
            global response_for_count
            response_for_count = 1
            ads = await parser_for_bot.parse_ads(button)
            flag = True
        except:
            ads = await parser_for_bot.parse_ads(link)
        for i in ads:
            await callback.message.answer('https://cars.av.by' + i)

        if flag and ads.index(i) in (23, 24):
            i = 1 + ads.index(i)
            await callback.message.answer(str(i) + ' объявлений', reply_markup=keyboard.inlineKB_next)
    elif callback.data == 'next':
        content = await state.get_data()
        link = content['answer2']
        button = await parser_for_bot.parse_button_link(link)
        response_for_count += 1
        button = button.replace(f'page=2', f'page={response_for_count}')
        try:
            ads = await parser_for_bot.parse_ads(button)
            for i in ads:
                await callback.message.answer('https://cars.av.by' + i)
            if ads.index(i) == 24:
                await callback.message.answer(f'{25 * response_for_count} объявлений',
                                              reply_markup=keyboard.inlineKB_next)
            else:
                await callback.message.answer('Объявления закончились')

        except:
            await callback.message.answer('Объявления закончились')


# @dp.message_handler(text='Смотреть все автомобили', state=Me_info.second_state)
# async def all_inf_cars(message: types.Message, state: FSMContext):
#     pass


# ---------позже
@dp.message_handler(content_types='text')
async def asd(message):
    print(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup_, skip_updates=True)
