from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import dp, db
from datetime import datetime


class OrderMessAdmin(StatesGroup):
    wait_new_address = State()
    wait_new_tel_num = State()
    wait_new_price = State()
    wait_new_driver = State()
    wait_new_ready = State()


@dp.message_handler(content_types=types.ContentTypes.ANY) #lambda message: message.chat.id not in "877916659"
async def step_1_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="отмена"))
    await message.answer("Добавьте адресс:", reply_markup=keyboard)
    await OrderMessAdmin.next()


@dp.message_handler(state=OrderMessAdmin.wait_new_address, content_types=types.ContentTypes.TEXT)
async def step_2_address(message: types.Message, state: FSMContext):  # обратите внимание, есть второй аргумент
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="отмена"))
    await state.update_data(address=message.text.lower())
    await message.answer("укажите номер телефона:", reply_markup=keyboard)
    await OrderMessAdmin.next()


@dp.message_handler(state=OrderMessAdmin.wait_new_tel_num, content_types=types.ContentTypes.TEXT)
async def step_3_tel_num(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="отмена"))
    await state.update_data(tel_num=message.text.lower())
    await message.answer("укажите цену заказа:", reply_markup=keyboard)
    await OrderMessAdmin.next()


@dp.message_handler(state=OrderMessAdmin.wait_new_price, content_types=types.ContentTypes.TEXT)
async def step_4_price(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    drivers = db.get_drivers()
    for driver in drivers:
        keyboard.add(driver)
    keyboard.add(types.KeyboardButton(text="Автоматический выбор"))
    keyboard.add(types.KeyboardButton(text="отмена"))
    await state.update_data(price=message.text.lower())
    await message.answer("укажите водителя(по желанию)", reply_markup=keyboard)
    await OrderMessAdmin.next()


@dp.message_handler(state=OrderMessAdmin.wait_new_driver, content_types=types.ContentTypes.TEXT)
async def step_5_driver(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Сохранить заказ"))
    keyboard.add(types.KeyboardButton(text="отмена"))
    await state.update_data(driver=message.text.lower())
    user_data = await state.get_data()
    await message.answer(f"Вы заказали машину на адресс:{user_data['address']}\n"
                         f"Номер телефона:{user_data['tel_num']}\n"
                         f"Цена:{user_data['price']}\n"
                         f"Водитель:{user_data['driver']}.\n",
                         reply_markup=keyboard)
    await OrderMessAdmin.next()


@dp.message_handler(state=OrderMessAdmin.wait_new_ready, content_types=types.ContentTypes.TEXT)
async def step_6_ready(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="отмена"))
    user_data = await state.get_data()
    db.add_order(message.from_user.id, datetime.utcnow(), user_data['address'], " ", user_data['tel_num'], user_data['price'], user_data['driver'])

    #сдесь пишем что если заказ успешно сохранился
    await message.answer(f"Вы успешно сделали заказ", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
