import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

TOKEN = '6070617064:AAEp2BEdWtlQYq6GsDNvAV7KPv8yRrhVCAs'
CHAT_ID = '-1001609605973'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Определяем состояния FSM
class Form(StatesGroup):
    name = State()
    birth_date = State()
    phone_number = State()
    email = State()
    social_links = State()
    education_status = State()
    education_details = State()
    has_work_book = State()
    has_medical_book = State()
    is_our_guest = State()
    user_link = State()
    job_preferences = State()

# Функция для начала анкеты
@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    """
    Хэндлер для команды /start
    """
    # Удаляем предыдущую клавиатуру (если была)
    await message.reply('Добрый день! Для начала анкеты нажмите "Начать"', 
                        reply_markup=types.ReplyKeyboardRemove())
    # Предлагаем начать анкету
    await Form.name.set()
    await message.reply("Введите ваше имя и фамилию:")

# Функции для обработки ответов на вопросы анкеты
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Введите дату рождения в формате ДД.ММ.ГГГГ:")

@dp.message_handler(state=Form.birth_date)
async def process_birth_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['birth_date'] = message.text

    await Form.next()
    await message.reply("Введите контактный номер телефона:")

@dp.message_handler(state=Form.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    await Form.next()
    await message.reply("Введите адрес электронной почты:")

@dp.message_handler(state=Form.email)
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    await Form.next()
    await message.reply("Введите ссылки на страницу в ВК, Instagram, Telegram (мы просто хотим поставить лайк):")

@dp.message_handler(state=Form.social_links)
async def process_social_links(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['social_links'] = message.text

    await Form.next()
    await message.reply("На момент заполнения анкеты ты:\n"
                        "1. Учусь очно\n"
                        "2. Учусь заочно\n"
                        "3. Закончил/Не учусь")

@dp.message_handler(state=Form.education_status)
async def process_current_status(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['education_status'] = message.text

    await Form.next()
    await message.reply("Напиши пожалуйста наименование учебного заведения, специальность и год выпуска.")

@dp.message_handler(state=Form.education_details)
async def process_education_details(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['education_details'] = message.text

    await Form.next()
    await message.reply("Наличие трудовой книжки (Да/Нет):")

@dp.message_handler(state=Form.has_work_book)
async def process_work_book(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['has_work_book'] = message.text

    await Form.next()
    await message.reply("Наличие медицинской книжки (Да/Нет):")

@dp.message_handler(state=Form.has_medical_book)
async def process_medical_book(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['has_medical_book'] = message.text

    await Form.next()
    await message.reply("Являешься ли ты нашим гостем (Да/Нет):")

@dp.message_handler(state=Form.is_our_guest)
async def process_is_guest(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_our_guest'] = message.text

    await Form.next()
    await message.reply("Что для тебя важно при выборе работы?")

@dp.message_handler(state=Form.user_link)
async def start_command(message: types.Message, state: FSMContext):
    user_link = f'https://t.me/{message.from_user.username}'
    async with state.proxy() as data:
        data['user_link'] = user_link
    await Form.next()


@dp.message_handler(state=Form.job_preferences)
async def process_job_preferences(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['job_preferences'] = message.text

        # Формируем текст анкеты в удобочитаемом формате
        text = "Новая анкета:\n\n"
        text += f"Ссылка на телеграмм: {data.get('user_link')}\n"
        text += f"Имя и фамилия: {data.get('name')}\n"
        text += f"Дата рождения: {data.get('birth_date')}\n"
        text += f"Контактный номер телефона: {data.get('phone_number')}\n"
        text += f"Адрес электронной почты: {data.get('email')}\n"
        text += f"Ссылки на социальные сети: {data.get('social_links')}\n"
        text += f"На момент заполнения анкеты ты: {data.get('education_status')}\n"
        text += f"Учебное заведение: {data.get('education_details')}\n"
        text += f"Трудовая книжка: {data.get('has_work_book')}\n"
        text += f"Медицинская книжка: {data.get('has_medical_book')}\n"
        text += f"Наш гость: {data.get('is_our_guest')}\n"
        text += f"Приоритеты в работе: {data.get('job_preferences')}\n"

        # Отправляем анкету в чат и очищаем данные формы
        await bot.send_message(chat_id="-1001609605973", text=text)
        await state.finish()

    await message.reply("Спасибо за заполнение анкеты!")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



   
