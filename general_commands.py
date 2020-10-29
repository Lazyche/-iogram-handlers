from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from config import dp, db, bot
from datetime import datetime


@dp.message_handler(commands="cancel", state="*")
@dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):  # обратите внимание на второй аргумент
    # Сбрасываем текущее состояние пользователя и сохранённые о нём данные
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=["start"], state="*")
async def cmd_start(message: types.Message, state: FSMContext):

    if db.admins_exists(message.from_user.id):
        #если пользователь администратор
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Добавить новый заказ"))
        await message.answer("👋 Приветсвую Вас, мой Администратор " + str(message.from_user.full_name) + "\n"
                            "Вам доступны следующие функции:\n"
                            "1️⃣ Добавление заказов(с выбором водителя)\n"
                            "2️⃣ Просмотр/Редактирование заказов у водителей\n"
                             ,reply_markup=keyboard)

    elif db.drivers_exists(message.from_user.id):
        #если пользователь водитель
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Добавить новый заказ"))
        await message.answer("👋 Приветсвую водителя " + str(message.from_user.full_name) + "\n"
                             "Вам доступны следующие функции:\n"
                             "1. Добавление заказов(с выбором водителя)\n"
                             ,reply_markup=keyboard)

    elif db.clients_exists(message.from_user.id):
        #если пользователь клиент
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Да хочу!! Заказать машину"))
        await message.answer("👋 Приветсвую Вас," + str(message.from_user.full_name) + "\n"
                             "Мы рады, что вы используете наши осенезаторские услуги\n"
                             "Хотите сделать заказ машины на откачку вашей ямы? \n"
                             ,reply_markup=keyboard)

    else:
        # если пользователь первый раз защел
        db.add_client(message.from_user.id, message.from_user.full_name, datetime.utcnow())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Да хочу!! Заказать машину"))
        await message.answer("👋 Приветсвую Вас," + str(message.from_user.full_name) + "\n"
                             "Мы рады видеть новых клиентов\n"
                             "Хотите сделать заказ машины на откачку вашей ямы? \n"
                             ,reply_markup=keyboard)

@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    if message.from_user.id == 877916659:  # Подставьте сюда свой Telegram ID
        commands = [types.BotCommand(command="/drinks", description="Заказать напитки"),
                    types.BotCommand(command="/food", description="Заказать блюда")]
        await bot.set_my_commands(commands)
        await message.answer("Команды настроены.")
