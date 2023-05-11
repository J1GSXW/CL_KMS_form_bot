import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

# установка уровня логирования
logging.basicConfig(level=logging.INFO)

# инициализация бота и диспетчера
bot = Bot(token="6070617064:AAEp2BEdWtlQYq6GsDNvAV7KPv8yRrhVCAs")
dp = Dispatcher(bot, storage=MemoryStorage())

# инициализация состояний
class Form(StatesGroup):
    name = State()
    age = State()
    gender = State()

# команда для запуска анкеты
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """
    Обрабатывает команду /start и начинает процесс анкеты.
    """
    await Form.name.set()
    await message.reply("Как вас зовут?")

# обработка имени пользователя
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Обрабатывает имя пользователя и переходит к следующему вопросу.
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Сколько вам лет?")

# обработка возраста пользователя
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    """
    Обрабатывает возраст пользователя, если он не число.
    """
    return await message.reply("Возраст должен быть числом.\nСколько вам лет? (цифрами)")

@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    """
    Обрабатывает возраст пользователя и переходит к следующему вопросу.
    """
    async with state.proxy() as data:
        data['age'] = message.text

    await Form.next()
    await message.reply("Какой у вас пол?")

# обработка пола пользователя (продолжение)
@dp.message_handler(lambda message: message.text not in ['Мужской', 'Женский'], state=Form.gender)
async def process_gender_invalid(message: types.Message):
    """
    Обрабатывает пол пользователя, если он введен неправильно.
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('Мужчина', 'Женщина')
    return await message.reply("Выберите ваш пол из предложенных вариантов.", reply_markup=keyboard)

@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    """
    Обрабатывает пол пользователя и завершает процесс анкеты.
    """
    async with state.proxy() as data:
        data['gender'] = message.text

        # вывод результатов анкеты в одно сообщение
        result = f"Результаты анкеты:\n\nИмя: {data['name']}\nВозраст: {data['age']}\nПол: {data['gender']}"

        # отправка результата анкеты в беседу
        await bot.send_message(chat_id="-1001609605973", text=result)

        # завершение процесса анкеты
        await state.finish()

        # уведомление пользователя о завершении анкеты
        await message.reply("Спасибо за заполнение анкеты! Результаты были отправлены в беседу.")

# обработка некорректных сообщений
@dp.message_handler(lambda message: message.text not in ['/start'], state='*')
async def process_invalid_command(message: types.Message):
    """
    Обрабатывает некорректные сообщения.
    """
    await message.reply("Чтобы заполнить анкету, используйте команду /start.")

# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






   
