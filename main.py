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
    last_job = State()
    dismissal_reason = State()
    why_us = State()
    quick_learning = State()
    main_dream = State()
    favorite_drink = State()
    hobby = State()
    achievment = State()
    new_acquaintances = State()
    emotions = State()
    work_schedule = State()
    last_job_recommendation = State()
    know_vacancy = State()
    if_you_small = State()
    remark = State()
    what_closely = State()
    freeze_pinguin = State()
    why_you = State()
    theft = State()
    two_employers = State()

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
    await message.reply("Идём дальше ?")

@dp.message_handler(state=Form.job_preferences)
async def process_job_preferences(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['job_preferences'] = message.text

    await Form.next()
    await message.reply("Предыдущее место работы?(не официальное тоже считается)")

@dp.message_handler(state=Form.last_job)
async def process_last_job(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_job'] = message.text

    await Form.next()
    await message.reply("Причина ухода с предыдущего места работы?")

@dp.message_handler(state=Form.dismissal_reason)
async def process_dismissal_reason(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dismissal_reason'] = message.text

    await Form.next()
    await message.reply("Почему ты хочешь работать с кофе и выбираешь именно нашу компанию? (Мы конечно догадываемся, но все же)")

@dp.message_handler(state=Form.why_us)
async def process_why_us(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['why_us'] = message.text

    await Form.next()
    await message.reply("Легко ли ты воспринимаешь новую информацию, быстрообучаем?(варианты ответа: Да, Нет, Возможно, Другое(введи текстом))")

@dp.message_handler(state=Form.quick_learning)
async def process_quick_learning(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quick_learning'] = message.text

    await Form.next()
    await message.reply("Какая твоя главная мечта?")

@dp.message_handler(state=Form.main_dream)
async def process_main_dream(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['main_dream'] = message.text

    await Form.next()
    await message.reply("Какой твой любимый напиток?")

@dp.message_handler(state=Form.favorite_drink)
async def process_favorite_drink(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['favotite_drink'] = message.text

    await Form.next()
    await message.reply("Какое твоё увлечение, хобби?")

@dp.message_handler(state=Form.hobby)
async def process_hobby(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hobby'] = message.text

    await Form.next()
    await message.reply("Какими достижениями ты гордишься?")



@dp.message_handler(state=Form.achievment)
async def process_achievment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['achievment'] = message.text

    await Form.next()
    await message.reply("Ты легко находишь общий язык с людьми, заводишь новые знакомства?")

@dp.message_handler(state=Form.new_acquaintances)
async def process_new_acquaintances(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_acquaintances'] = message.text

    await Form.next()
    await message.reply("Бывает сложно сдерживать эмоции?")

@dp.message_handler(state=Form.emotions)
async def process_emotions(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['emotions'] = message.text

    await Form.next()
    await message.reply("Желаемый график работы?")


@dp.message_handler(state=Form.work_schedule)
async def process_work_schedule(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['work_schedule'] = message.text

    await Form.next()
    await message.reply("Кто может порекомендовать тебя с предыдущего места работы? (телефон, ФИО)")


@dp.message_handler(state=Form.last_job_recommendation)
async def process_last_job_recommendation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_job_recommendation'] = message.text

    await Form.next()
    await message.reply("Как ты узнал о вакансии?")


@dp.message_handler(state=Form.know_vacancy)
async def process_know_vacancy(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['know_vacancy'] = message.text

    await Form.next()
    await message.reply("Представь: ты в комнате, там стоит большой стол, а на столе стоит твоя любимая еда. Ты до жути голодный. Но есть одно ""но"", ты маленького роста, размером с мышку. Что ты будешь делать?")



@dp.message_handler(state=Form.if_you_small)
async def process_if_you_small(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['if_you_small'] = message.text

    await Form.next()
    await message.reply("Как ты отреагируешь на замечание коллеги на твою работу?")

@dp.message_handler(state=Form.remark)
async def process_remark(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['remark'] = message.text

    await Form.next()
    await message.reply("Что тебе ближе?(варианты ответа: Предлагать и продвигать новые методы и решения, Работать по инструкции/регламенту, Другое(напиши текстом))")


@dp.message_handler(state=Form.what_closely)
async def process_what_closely(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['what_closely'] = message.text

    await Form.next()
    await message.reply("Ты приходишь домой, и видишь в своей морозилке пингвина. Твои действия?")


@dp.message_handler(state=Form.freeze_pinguin)
async def process_freeze_pinguin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['freeze_pinguin'] = message.text

    await Form.next()
    await message.reply("Почему мы должны взять именно тебя?")


@dp.message_handler(state=Form.why_you)
async def process_why_you(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['why_you'] = message.text

    await Form.next()
    await message.reply("Коллега украл/а имущество компании, ты — свидетель. Что будешь делать с этой информацией?")

@dp.message_handler(state=Form.theft)
async def process_theft(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['theft'] = message.text

    await Form.next()
    await message.reply("Тебе предложили работу два работодателя. Как будещь выбирать?")


@dp.message_handler(state=Form.two_employers)
async def process_two_employers(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['two_employers'] = message.text

        # Формируем текст анкеты в удобочитаемом формате
        text = "Новая анкета:\n\n"
        text += f"Ссылка на телеграмм: {data.get('user_link')}\n \n"
        text += f"Имя и фамилия: {data.get('name')}\n \n"
        text += f"Дата рождения: {data.get('birth_date')}\n \n"
        text += f"Контактный номер телефона: {data.get('phone_number')}\n \n"
        text += f"Адрес электронной почты: {data.get('email')}\n \n"
        text += f"Ссылки на социальные сети: {data.get('social_links')}\n \n"
        text += f"На момент заполнения анкеты ты: {data.get('education_status')}\n \n"
        text += f"Учебное заведение: {data.get('education_details')}\n \n"
        text += f"Трудовая книжка: {data.get('has_work_book')}\n \n"
        text += f"Медицинская книжка: {data.get('has_medical_book')}\n \n"
        text += f"Наш гость: {data.get('is_our_guest')}\n \n"
        text += f"Приоритеты в работе: {data.get('job_preferences')}\n \n"
        text += f"Предыдущее место работы: {data.get('last_job')}\n \n"
        text += f"Причина ухода: {data.get('dismissal_reason')}\n \n"
        text += f"Почему хочешь работать с кофе и у нас: {data.get('why_us')}\n \n"
        text += f"Быстрообучаемость: {data.get('quick_learning')}\n \n"
        text += f"Главная мечта: {data.get('main_dream')}\n \n"
        text += f"Любимый напиток: {data.get('favorite_drink')}\n \n"
        text += f"Хобби: {data.get('hobby')}\n \n"
        text += f"Достижения: {data.get('achievment')}\n \n"
        text += f"Легко заводишь знакомства: {data.get('new_acquaintances')}\n \n"
        text += f"Сложно ли сдерживать эмоции: {data.get('emotions')}\n \n"
        text += f"График работы: {data.get('work_schedule')}\n \n"
        text += f"Кто может порекомендовать с прошлого места работы: {data.get('last_job_recommendation')}\n \n"
        text += f"Как узнал о вакансии: {data.get('know_vacancy')}\n \n"
        text += f"Комната, стол, еда, ты маленький: {data.get('if_you_small')}\n \n"
        text += f"Реакция на замечание коллеги: {data.get('remark')}\n \n"
        text += f"Что ближе: {data.get('what_closely')}\n \n"
        text += f"Пингвин в морозилке: {data.get('freeze_pinguin')}\n \n"
        text += f"Почему должны взять именно тебя: {data.get('why_you')}\n \n"
        text += f"Коллега вор, ты свидетель, варианты: {data.get('theft')}\n \n"
        text += f"Предложили работу двое, как будешь выбирать: {data.get('two_employers')}\n \n"

        # Отправляем анкету в чат и очищаем данные формы
        await bot.send_message(chat_id="-1001609605973", text=text)
        await state.finish()

    await message.reply("Спасибо за заполнение анкеты!")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



   
