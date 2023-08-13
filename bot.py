from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from keyboards.client_keyboard import markup
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher import filters
import conf
import datetime
from aiogram.dispatcher.middlewares import BaseMiddleware
from bd.bdnew import botBDnew
from loguru import logger
from aiogram.utils.executor import start_webhook

TEST_MODE = True

if conf.VPS:
    TEST_MODE = False

##------------------Блок ініціалізації-----------------##
if TEST_MODE:
    API_Token = conf.API_TOKEN_Test
else:
    API_Token = conf.TOKEN

ADMIN_ID = conf.ADMIN_ID
bot = Bot(token=API_Token)  # os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
botbdnew = botBDnew()
logger.add("debug.txt")
# webhook settings
WEBHOOK_HOST = 'https://vmi957205.contaboserver.net'
WEBHOOK_PATH = '/prod_famstat'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip 127.0.0.1
WEBAPP_PORT = 3005


##--------------Машини станів----------------------------##
class FSMzapCredet(StatesGroup):
    cash = State()
    description = State()


##---------------------Midelware-------------------------------##


class MidlWare(BaseMiddleware):

    async def on_process_update(self, update: types.Update, date: dict):
        logger.debug(update)
        logger.debug(update.message.from_user.id)
        if update.message.from_user.id not in ADMIN_ID:
            logger.debug(f"Хтось лівий зайшов {update.message.from_user.id}")
            raise CancelHandler()


##-------------------handlers--------------------------------------##
@dp.message_handler(commands=['start', 'help'], state=None)
async def send_welcome(message: types.Message):
    await message.reply("Вітаю! Щоб розпочати натисніть кнопку внизу!", reply_markup=markup)


##--------------------------видатки-----------------------##
@dp.message_handler(filters.Text(
    equals=["Продукти🧀", "Одяг👗", "Подарунки🎁", "Красота👠", "Дитині👧", "Аптека💊", "Хімія🧴", "Господарство🏡", "Інше🧾"]),
                    state=None)
async def credet(message: types.Message, state: FSMContext):
    await FSMzapCredet.cash.set()
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")

    async with state.proxy() as data:
        data['category'] = message.text[0:-1]
    logger.debug(f"Category - {message.text}")
    await message.answer("Напишіть суму:", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=[types.ContentType.TEXT], state=FSMzapCredet.cash)
async def getcash(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    if message.text.isdigit():
        async with state.proxy() as data:
            data['viruhka'] = message.text
            logger.debug(f"Витрати - {message.text}")
            if data['category'] in ["Продукти", "Одяг", "Подарунки", "Красота", "Дитині", "Аптека", "Хімія",
                                    "Господарство"]:
                botbdnew.recCredet(data['category'], data['viruhka'], data['category'])
                await bot.send_message(conf.ADMIN_ULIA,
                                       f"Витрати за {data['category']} {data['viruhka']} грн. внесено!",
                                       reply_markup=markup)
                await bot.send_message(conf.ADMIN_SERG,
                                       f"Витрати за {data['category']} {data['viruhka']} грн. внесено!",
                                       reply_markup=markup)

                await state.finish()
            else:
                await message.answer("Опишіть за що саме:")
                await FSMzapCredet.next()
    else:
        await message.answer("Напишіть число без грн.")


@dp.message_handler(content_types=[types.ContentType.TEXT], state=FSMzapCredet.description)
async def description(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    async with state.proxy() as data:
        data['desr'] = message.text
    logger.debug(f"Опис - {message.text}")
    botbdnew.recCredet(data['category'], data['viruhka'], data["desr"])
    await bot.send_message(conf.ADMIN_ULIA, f"Витрати за {data['desr']} {data['viruhka']} грн. внесено!",
                           reply_markup=markup)
    await bot.send_message(conf.ADMIN_SERG, f"Витрати за {data['desr']} {data['viruhka']} грн. внесено!",
                           reply_markup=markup)
    await state.finish()


##----------------------Статистика------------------------##
@dp.message_handler(filters.Text(equals="Статистика за місяць 📊"), state=None)
async def month_statistic(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    now = datetime.datetime.now()
    te = botBDnew.statYearbyMonth(month=now.month, year=now.year)
    doc = open('testplor.png', 'rb')
    await message.answer(te)
    await message.reply_photo(doc)


@dp.message_handler(filters.Text(equals="Минулий місяць"), state=None)
async def month_statistic(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    if month > 1:
        month = now.month - 1
    else:
        year = now.year - 1
        month = 12

    te = botBDnew.statYearbyMonth(month=month, year=year)
    doc = open('testplor.png', 'rb')
    await message.answer(te)
    await message.reply_photo(doc)


@dp.message_handler(filters.Text(equals="Рік"), state=None)
async def month_statistic(message: types.Message):
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    for month in range(1, month + 1):
        await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
        te = botBDnew.statYearbyMonth(month=month,year=year)
        if te:
            try:
                doc = open('testplor.png', 'rb')
                await message.answer(te)
                await message.reply_photo(doc)
            except:
                pass

    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    te = botBDnew.StatAllYear(year=year)
    doc = open('testplor.png', 'rb')
    await message.answer(te)
    await message.reply_photo(doc)


# @dp.message_handler(filters.Text(equals="Сторінка"), state=None)
# async def site(message: types.Message):
#     await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
#     botbdnew.statHTML()
#     await message.answer("<a href='https://vmi957205.contaboserver.net/famstat/statistic.html'>Натисни тут</a>", reply_markup=markup, parse_mode="HTML")


##----------------------------Різне----------------------##
@dp.message_handler()
async def echo(message: types.Message):
    if message.text == "Файл12":
        doc = open('debug.txt', 'rb')
        await message.reply_document(doc)
    elif message.text == "html":
        await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
        botbdnew.statHTML()
        await message.answer("<a href='https://vmi957205.contaboserver.net/famstat/statistic.html'>Натисни тут</a>",
                             reply_markup=markup, parse_mode="HTML")

    else:
        await message.answer("Не розумію!", reply_markup=markup)


##-------------------Запуск бота-------------------------##
if TEST_MODE:
    print("Bot running...")
    dp.middleware.setup(MidlWare())
    executor.start_polling(dp, skip_updates=True)
else:
    async def on_startup(dp):
        await bot.set_webhook(WEBHOOK_URL)
        logger.debug("Бот запущено!")


    async def on_shutdown(dp):
        logger.debug('Зупиняюся!')
        await bot.delete_webhook()
        await dp.storage.close()
        await dp.storage.wait_closed()


    if __name__ == '__main__':
        dp.middleware.setup(MidlWare())
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
