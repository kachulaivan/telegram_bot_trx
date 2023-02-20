import random
from asyncio import sleep
import locales

from aiogram.utils import executor
from aiogram import types
import db
from dispatcher import dp, bot
import handlers
from db import BotDB
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler(timezone="EUROPE/KIEV")
time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute)


async def lot_winner():
    users_ua = await db.get_users_ua()
    users_ru = await db.get_users_ru()
    users_en = await db.get_users_en()
    winner_users = ["2375790634", "534312376", "440962736", "774493635", "971936290", "366998241", "3162178930", "848871509",
                    "415034835", "2940956818", "572409928", "324736647", "986377197", "2628774423", "637256057", "960093721",
                    "4016087874", "6238207096", "854338668", "1976517880", "5907808767", "5129020989", "3018919831", "815715611",
                    "934728481", "712506269", "311527363", "533749585", "473181631", "1695303863", "1204725685", "1416927807",
                    "767069883", "989281005", "218677783", "319751905", "5385675287", "5497897409", "9252789462", "5394902684",
                    "871375932", "893597154", "4087367194", "5196214838", "6209587316", "647655695", "798267428", "839877817"]
    winner_user = random.choice(winner_users)
    text_ua = (f'🎉\n🎉\n🎉\n\nℹ \nПереможець лотереї учасник із id: \n\n<i><b><u>{winner_user}</u></b></i> \n👀\n\n🎉\n🎉\n🎉')
    text_ru = (f'🎉\n🎉\n🎉\n\nℹ \nПобедитель лотереи участник c id: \n\n<i><b><u>{winner_user}</u></b></i> \n👀\n\n🎉\n🎉\n🎉')
    text_en = (f'🎉\n🎉\n🎉\n\nℹ \nThe winner of the lottery is a participant with id: \n\n<i><b><u>{winner_user}</u></b></i> \n👀\n\n🎉\n🎉\n🎉')
    for user in users_ua:
        try:
            await bot.send_message(chat_id=user[0], text=text_ua, parse_mode='html')
            await sleep(0.33)
        except Exception:
            pass
    for user in users_ru:
        try:
            await bot.send_message(chat_id=user[0], text=text_ru, parse_mode='html')
            await sleep(0.33)
        except Exception:
            pass
    for user in users_en:
        try:
            await bot.send_message(chat_id=user[0], text=text_en, parse_mode='html')
            await sleep(0.33)
        except Exception:
            pass
    await bot.send_message(chat_id=5143177713, text='Переможець конкурсу надісланий автоматично')


async def scheduler_():
    scheduler.add_job(db.all_acc_stats, trigger='cron', hour='03', minute='30',)
    scheduler.add_job(db.day_acc_stats, trigger='cron', hour='03', minute='30',)
    scheduler.add_job(db.pay_trx_stats, trigger='cron', hour='03', minute='30',)
    scheduler.add_job(db.active_acc_stats, trigger='cron', hour='03', minute='30',)
    scheduler.add_job(lot_winner, trigger='cron', hour='18', minute='00',)
    scheduler.add_job(db.del_lot_db, trigger='cron', hour='18', minute='01',)
    scheduler.start()

async def on_startup(_):
    asyncio.create_task(scheduler_())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
