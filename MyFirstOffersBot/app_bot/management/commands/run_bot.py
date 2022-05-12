import logging
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, executor, types
from app_bot.models import Employer
from asgiref.sync import sync_to_async


API_TOKEN = '5354949675:AAF-tlHaCp4TS5OA0CvprizvHaINnMASZN0'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


command = ''


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    text = 'Привет, меня зовут Александр\n' \
           'Это бот для пассивного поиска работы' \
           'Информация обо мне /info\n' \
           'Прислать мне вакансию /vacancy'
    await message.answer(text)


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    text = 'Junior, опыт более полугода\n\n' \
           '» Python\n' \
           '» Django (+Django REST Framework)\n' \
           '» Работа со сторонними API\n' \
           '» Работа с SQL базами данных\n' \
           '» Работа с системами контроля версий (Git)\n' \
           '» Docker, Redis, Jenkins\n' \
           '» Основы Linux\n' \
           '» База Java\n' \
           '» База HTML\n' \
           '» CSS\n\n' \
           'Контакты:\n' \
           'Telegram: @Dreamis\n' \
           'Github: https://github.com/AwesomeDreamis\n' \
           'Резюме на хабр карьере: https://career.habr.com/dreamis\n'
    await message.answer(text)


@sync_to_async
def create_emp(message):
    try:
        Employer.objects.get(tg_chat_id=message.from_user.id)
    except:
        Employer.objects.create(
            name='-',
            tg_chat_id=message.from_user.id,
            url='-',
            description='-',
        )


@dp.message_handler(commands=['vacancy'])
async def vacancy(message: types.Message):
    text = 'Необходимо заполнить данные:\n' \
           'название компании /name\n' \
           'url вакансии (не обязательно) /url\n' \
           'описание вакансии /description\n\n' \
           'После того как всё заполните, введите /send чтобы отправить мне уведомление\n'
    await create_emp(message)

    await message.answer(text)


# ================================================================================

@dp.message_handler(commands=['name'])
async def name(message: types.Message):
    text = 'Введите название компании'
    global command
    command = message.text
    await message.answer(text)


@dp.message_handler(commands=['url'])
async def url(message: types.Message):
    text = 'Вставьте ссылку на вакансию'
    global command
    command = message.text
    await message.answer(text)


@dp.message_handler(commands=['description'])
async def description(message: types.Message):
    text = 'Введите описание вакансии'
    global command
    command = message.text
    await message.answer(text)


@sync_to_async
def get_emp(message):
    return Employer.objects.get(tg_chat_id=message.from_user.id)



@dp.message_handler(commands=['send'])
async def send(message: types.Message):
    success_text = 'Вакансия успешно отправлена'
    failed_text = 'Не все данные заполнены'
    emp = await get_emp(message)
    if emp.name == '-' or emp.description == '-':
        await message.answer(failed_text)
    else:
        await message.answer(success_text)
        await bot.send_message(chat_id='238897024', text=f'Компания {emp.name} хочет с вами связаться')


@sync_to_async
def set_name(message, name):
    emp = Employer.objects.get(tg_chat_id=message.from_user.id)
    emp.name = name
    emp.save()


@sync_to_async
def set_url(message, url):
    emp = Employer.objects.get(tg_chat_id=message.from_user.id)
    emp.url = url
    emp.save()


@sync_to_async
def set_desc(message, desc):
    emp = Employer.objects.get(tg_chat_id=message.from_user.id)
    emp.description = desc
    emp.save()


@dp.message_handler()
async def echo(message: types.Message):
    if command == '/name':
        name = message.text
        await set_name(message, name)
        await message.answer(f'название компании: {name}')
    elif command == '/url':
        url = message.text
        await set_url(message, url)
        await message.answer(f'ссылка на вакансию: {url}')
    elif command == '/description':
        description = message.text
        await set_desc(message, description)
        await message.answer(f'краткое описание вакансии: {description}')
    else:
        await message.answer('попробуйте другую команду')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        executor.start_polling(dp, skip_updates=True)
