from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = "5910817033:AAGhbwBrBMgAexaMeCLRHQPjzHrxYPk1R7c"
BOT_NICKNAME = 'trx_games_bot'

CHANNELS = [
    ["👥 Group TRX BOT | EARN/GAME", "-1001839399117", "https://t.me/group_trx_bot"]
]
# PATREON = [
#     ["👥 Patreon TRX BOT | EARN/GAME", "-1001839399117", "patreon.com/TelegramTRXBot"]
# ]
NOT_SUB_MESSAGE = {
    'NOT_SUB_MESSAGE_ua': "ℹ Для отримання доступу до даної функції, потрібно підписатись на нашу групу в телеграм 💳\n\n👇 Силка тут 👇",
    'NOT_SUB_MESSAGE_ru': "ℹ Для получения доступа к данной функции, нужно подписаться на нашу группу в телеграмм 💳\n\n👇 Ссылка здесь 👇",
    'NOT_SUB_MESSAGE_en': "ℹ To get access to this function, you need to subscribe to our Telegram group 💳\n\n👇 Link here 👇"
}
SUB_MESSAGE = {
    'NOT_SUB_MESSAGE_ua': "✅ Виконано! Ви підписались на канал",
    'NOT_SUB_MESSAGE_ru': "✅ Выполнено! Вы подписались на канал",
    'NOT_SUB_MESSAGE_en': "✅ Done! You have subscribed to the channel"
}
admins = [
    663493672,
    5143177713
]

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

