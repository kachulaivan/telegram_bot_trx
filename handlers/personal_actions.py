import xlsxwriter
import datetime as dt
import random
import smtplib
from email.mime.text import MIMEText
import db
import sqlite3
from aiogram.utils.deep_linking import get_start_link
from dispatcher import dp, bot
from aiogram import types
import keyboards as kb
from bot import BotDB
from aiogram.dispatcher import FSMContext
import locales
import handlers.admin, handlers.pay_operations, handlers.callback, handlers.say_hi # don't delete!!!!!!!!!!!!!


#######################################################################################################################################
from handlers import states

global base, cur
base = sqlite3.connect('bot_db.sqlite3')
cur = base.cursor()


joinedFile = open("C:/Users/ivank/PycharmProjects/Telegram_TRX_Bot_iogram/joined.txt", "r")#(/home/Easy800/Telegram_TRX_Bot_iogram/joined.txt)

joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()


count = 1
workbook = xlsxwriter.Workbook('messages.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, 'Дата')
worksheet.write(0, 1, 'Час')
worksheet.write(0, 2, 'Тип повідомлення')
worksheet.write(0, 3, 'Відправник')
worksheet.write(0, 4, 'ID відправника')
worksheet.write(0, 5, 'Повідомлення та ID стікера')
worksheet.write(0, 6, 'Емоція стікера')

async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer(locales.anti_flood['anti_flood_en'])


#######################################################################################################################################


#######################################################################################################################################
def send_email(message: types.Message):
    sender = "bot.management.trx@gmail.com"
    password = "dztaoaixiiljstqi"
    recipient = BotDB.get_user_mail(message.from_user.id)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        with open("gmail.html") as file:
            template = file.read()
    except IOError:
        return "The template file doesn't found!"

    try:
        server.login(sender, password)
        msg = MIMEText(template, "html")
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = "Telegram TRX BOT registration confirmation"
        server.sendmail(sender, recipient, msg.as_string())
    except Exception as _ex:
        pass
#######################################################################################################################################


#######################################################################################################################################
@dp.message_handler(commands=['start', 'help'])
@dp.throttled(anti_flood, rate=1) #rate это количество секунд, при котором входящие сообщения считаются флудом.
async def start(message: types.Message):

    if message.chat.type == 'private':
        try:
            if (not BotDB.user_exists(message.from_user.id)):
                start_command = message.text
                first_referrer_id = str(start_command[7:])
                if first_referrer_id != "":
                    if str(first_referrer_id) != str(message.from_user.id):
                        BotDB.add_user(message.from_user.id, first_referrer_id)
                        for value in cur.execute(f"SELECT first_referrer_id FROM users WHERE user_id = {first_referrer_id}"):
                            second_referrer_id_mod = value[0]
                            if second_referrer_id_mod != "":
                                user_id_mod = message.from_user.id
                                cur.execute(f"UPDATE users SET second_referrer_id = '{second_referrer_id_mod}' WHERE `user_id` = {user_id_mod}")
                                base.commit()
                                for value_sec in cur.execute(f"SELECT second_referrer_id FROM users WHERE user_id = {first_referrer_id}"):
                                    third_referrer_id_mod = value_sec[0]
                                    if third_referrer_id_mod != "None":
                                        cur.execute(f"UPDATE users SET third_referrer_id = '{third_referrer_id_mod}' WHERE `user_id` = {user_id_mod}")
                                        base.commit()
                                        try:
                                            await db.give_bonus_ref_thi_ref(third_referrer_id_mod)
                                            await bot.send_message(third_referrer_id_mod, locales.reg_user[f'reg_user_third_ref_{BotDB.user_language(third_referrer_id_mod)}'].format(message.from_user.username))
                                        except:
                                            pass
                                try:
                                    await db.give_bonus_ref_sec_ref(second_referrer_id_mod)
                                    await bot.send_message(second_referrer_id_mod, locales.reg_user[f'reg_user_second_ref_{BotDB.user_language(second_referrer_id_mod)}'].format(message.from_user.username))
                                except:
                                    pass
                        await db.give_bonus_ref_start(message.from_user.id)
                        await bot.send_message(message.from_user.id, locales.reg_user[f'reg_user_in_ref_{BotDB.user_language(message.from_user.id)}'])
                        try:
                            await db.give_bonus_ref(first_referrer_id)
                            await bot.send_message(first_referrer_id, locales.reg_user[f'reg_user_first_ref_{BotDB.user_language(first_referrer_id)}'].format(message.from_user.username))
                        except:
                            pass
                    else:
                        BotDB.add_user(message.from_user.id)
                        await bot.send_message(message.from_user.id, locales.reg_user[f'reg_user_in_our_ref_{BotDB.user_language(message.from_user.id)}'])
                else:
                    BotDB.add_user(message.from_user.id)
            if not BotDB.daily_bonus_exists(message.from_user.id):
                BotDB.get_bonus_daily(message.from_user.id)
            if not BotDB.week_bonus_exists(message.from_user.id):
                BotDB.get_bonus_week(message.from_user.id)
            if not BotDB.achivement_exists(message.from_user.id):
                BotDB.add_achivement(message.from_user.id)

            if not str(message.from_user.id) in joinedUsers:
                joinedFile = open("C:/Users/ivank/PycharmProjects/Telegram_TRX_Bot_iogram/joined.txt", "a")  # (/home/Easy800/Telegram_TRX_Bot_iogram/joined.txt)
                joinedFile.write(str(message.from_user.id) + " " + str(message.from_user.first_name) + " " + str(message.from_user.last_name) + " " + str(dt.datetime.now().date()) + " " + str(dt.datetime.now().time())[0:8] + "\n")
                joinedUsers.add(message.from_user.id)

            for value_captcha in cur.execute(f"SELECT captcha, ban FROM users WHERE user_id = {message.from_user.id}"):
                if value_captcha[0] != 1:
                    await states.captcha.select_language.set()
                    pattern_captcha_1 = 0
                    pattern_captcha_2 = 633912
                    captcha_num = pattern_captcha_1 + pattern_captcha_2
                    await bot.send_message(message.from_user.id, f"💻 \n\nОберіть мову інтерфейсу \n\nВыберите язык интерфейса \n\nChoose the interface language \n\n💻", reply_markup=kb.markup_select_language)

                    @dp.message_handler(state=states.captcha.select_language)
                    async def promo_text(message: types.Message, state: FSMContext):
                        try:
                            if message.text == '🇺🇦 Українська':
                                await bot.send_message(message.from_user.id, f"🇺🇦 Вітаю\n\nВи обрали українську мову\n\nМову можна міняти в будь-який момент у розділі \n\n'🆘 Тех. Підтримка'", parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                                await bot.send_message(message.from_user.id, f"ℹ Підтвердіть що ви не бот\n\n📨 Введіть вашу пошту")
                                cur.execute(f"UPDATE users SET user_language = 'ua' WHERE user_id = {message.from_user.id}")
                                base.commit()
                                await states.captcha.next()
                            elif message.text == '🇷🇺 Русский':
                                await bot.send_message(message.from_user.id, f"🇷🇺 Поздравляю\n\nУ вас русский язык интерфейса\n\nЯзык можно менять в любой момент в разделе \n\n'🆘 Тех. Поддержка'", parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                                await bot.send_message(message.from_user.id, f"ℹ Подтвердите что вы не бот\n\n📨 Введите вашу почту")
                                cur.execute(f"UPDATE users SET user_language = 'ru' WHERE user_id = {message.from_user.id}")
                                base.commit()
                                await states.captcha.next()
                            elif message.text == '🇬🇧 English':
                                await bot.send_message(message.from_user.id, f"🇬🇧 Congratulations\n\n You have chosen English\n\n You can change the language at any time in the section \n\n'🆘 Support'", parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                                await bot.send_message(message.from_user.id, f"ℹ Confirm that you are not a bot\n\n📨 Enter your email")
                                cur.execute(f"UPDATE users SET user_language = 'en' WHERE user_id = {message.from_user.id}")
                                base.commit()
                                await states.captcha.next()
                            else:
                                await bot.send_message(message.from_user.id, f"ℹ Невідома мова! Неизвестный язык! Unknown language!", reply_markup=kb.markup_select_language)
                                await bot.send_message(message.from_user.id, f"ℹ \n\nОберіть із списку знизу \n\nВыберите из списка снизу \n\nChoose from the list below")

                        except:
                            await bot.send_message(message.from_user.id, f"ℹ Невідома мова! Неизвестный язык! Unknown language!", reply_markup=kb.markup_select_language)
                            await bot.send_message(message.from_user.id, f"ℹ \n\nОберіть із списку знизу \n\nВыберите из списка снизу \n\nChoose from the list below")

                    @dp.message_handler(state=states.captcha.type_mail)
                    async def promo_text(message: types.Message, state: FSMContext):
                        cur.execute(f"UPDATE users SET mail = '{message.text}' WHERE user_id = {message.from_user.id}")
                        base.commit()
                        markup_captcha = await kb.markup_mail(message)
                        await bot.send_message(message.from_user.id, locales.reg_operation[f'send_mail_done_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_captcha)
                        send_email(message=message)
                        await states.captcha.next()


                    @dp.message_handler(state=states.captcha.type_captcha)
                    async def promo_text(message: types.Message, state: FSMContext):
                        try:
                            if message.text.isdigit():
                                if int(message.text) == captcha_num:
                                    await bot.send_message(message.from_user.id, locales.reg_operation[f'done_captcha_{BotDB.user_language(message.from_user.id)}'])
                                    markup_phone = await kb.markup_phone(message)
                                    await bot.send_message(message.from_user.id, locales.reg_operation[f'send_phone_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_phone)
                                    await states.captcha.next()
                                else:
                                    markup_captcha = await kb.markup_mail(message)
                                    await bot.send_message(message.from_user.id, locales.reg_operation[f'false_captcha_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_captcha)
                                    await bot.send_message(message.from_user.id, locales.reg_operation[f'confirm_bot_{BotDB.user_language(message.from_user.id)}'])
                        except:
                            await bot.send_message(message.from_user.id, locales.reg_operation[f'number_false_{BotDB.user_language(message.from_user.id)}'])
                        if str(message.text) == 'Ввести іншу пошту' or message.text == "Ввести другую почту" or message.text == "Enter another mail":
                            await states.captcha.select_language.set()
                            await bot.send_message(message.from_user.id, locales.reg_operation[f'new_mail_{BotDB.user_language(message.from_user.id)}'], reply_markup=types.ReplyKeyboardRemove())
                            await states.captcha.next()
                        else:
                            pass
                    @dp.message_handler(content_types=types.ContentType.CONTACT, state=states.captcha.type_phone)
                    async def promo_text(message: types.Message, state: FSMContext):
                        try:
                            phone = message.contact.phone_number
                            # if phone[0] == '+' and phone[1] == '3' and phone[2] == '8' or phone[0] == '3' and phone[1] == '8':
                            try:
                                cur.execute(f"UPDATE users SET name = '{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username}' WHERE user_id = {message.from_user.id}")
                                base.commit()
                            except:
                                pass
                            cur.execute(f"UPDATE users SET captcha = 1 WHERE user_id = {message.from_user.id}")
                            cur.execute(f"UPDATE users SET phone = {phone} WHERE user_id = {message.from_user.id}")
                            base.commit()
                            markup_start = await kb.markup_start(message)
                            await bot.send_message(message.from_user.id, locales.reg_operation[f'done_reg_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_start)
                            if message.from_user.first_name == None:
                                markup_start = await kb.markup_start(message)
                                await bot.send_message(message.from_user.id, locales.hello_user[f'hello_with_last_{BotDB.user_language(message.from_user.id)}'].format(message.from_user.last_name), parse_mode='html', reply_markup=markup_start)
                            elif message.from_user.last_name == None:
                                markup_start = await kb.markup_start(message)
                                await bot.send_message(message.from_user.id, locales.hello_user[f'hello_with_first_{BotDB.user_language(message.from_user.id)}'].format(message.from_user.first_name), parse_mode='html', reply_markup=markup_start)
                            elif message.from_user.first_name == None and message.from_user.last_name == None:
                                markup_start = await kb.markup_start(message)
                                await bot.send_message(message.from_user.id, locales.hello_user[f'hello_without_name_{BotDB.user_language(message.from_user.id)}'], parse_mode='html', reply_markup=markup_start)
                            else:
                                markup_start = await kb.markup_start(message)
                                await bot.send_message(message.from_user.id, locales.hello_user[f'hello_with_all_name_{BotDB.user_language(message.from_user.id)}'].format(message.from_user.first_name, message.from_user.last_name), parse_mode='html', reply_markup=markup_start)
                            await bot.send_message(message.from_user.id,  locales.reg_operation[f'select_menu_{BotDB.user_language(message.from_user.id)}'])
                            await state.finish()
                            # else:
                            #     await state.finish()
                            #     await bot.send_message(message.from_user.id, f"🚫 Даний бот працює тільки для УКРАЇНЦІВ 🚫")
                        except:
                            await bot.send_message(message.from_user.id, f"🚫 Номер введено не коректно")
                else:
                    if value_captcha[1] == 0:
                        markup_start = await kb.markup_start(message)
                        await message.answer(locales.reg_operation[f'main_menu_{BotDB.user_language(message.from_user.id)}'], parse_mode='HTML', reply_markup=markup_start)
                        await bot.send_message(message.from_user.id, locales.reg_operation[f'select_menu_{BotDB.user_language(message.from_user.id)}'])
                    else:
                        await message.answer(locales.ban[f'ban_{BotDB.user_language(message.from_user.id)}'], parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

            @dp.message_handler(state=states.captcha.start)
            async def start_(message: types.Message, state: FSMContext):
                markup_start = await kb.markup_start(message)
                await message.answer(locales.reg_operation[f'main_menu_{BotDB.user_language(message.from_user.id)}'], parse_mode='HTML', reply_markup=markup_start)
                await bot.send_message(message.from_user.id, locales.reg_operation[f'select_menu_{BotDB.user_language(message.from_user.id)}'])
                await state.finish()
        except:
            await message.reply(locales.reg_operation[f'reg_error_{BotDB.user_language(message.from_user.id)}'])
    else:
        await message.reply(locales.reg_operation[f'reg_error_{BotDB.user_language(message.from_user.id)}'])
#######################################################################################################################################


#######################################################################################################################################
@dp.message_handler(commands='list_wins')
@dp.throttled(anti_flood, rate=1)
async def list_wins_combo(message: types.Message):
    await bot.send_message(message.from_user.id, locales.list_wins_slots[f'list_wins_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
#######################################################################################################################################


#######################################################################################################################################
@dp.message_handler(content_types=['text'])
@dp.throttled(anti_flood, rate=0.5) #rate это количество секунд, при котором входящие сообщения считаются флудом.
async def func(message: types.Message):
    for value_ban in cur.execute(f"SELECT ban FROM users WHERE user_id = {message.from_user.id}"):
        if value_ban[0] != 1:
            global count
            if(message.text == "🎯 Ігри 🎮" or message.text == "🎯 Игры 🎮" or message.text == "🎯 Games 🎮"):
                markup_games = await kb.markup_games(message)
                await bot.send_message(message.from_user.id, locales.list_games[f'games_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_games)
            elif (message.text == "🔢 Вгадай число" or message.text == "🔢 Угадай число" or message.text == "🔢 Guess the number"):
                await bot.send_message(message.chat.id, locales.list_games[f'guess_num_{BotDB.user_language(message.from_user.id)}'], reply_markup=kb.markup_guess_select, parse_mode='html')
            elif (message.text == "🎲 Кубик" or message.text == "🎲 Dice"):
                markup_dice_select = await kb.markup_dice_select(message)
                await bot.send_message(message.chat.id, locales.list_games[f'dice_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_dice_select, parse_mode='html')
            elif (message.text == "💣 Сапер" or message.text == "💣 Сапёр" or message.text == "💣 Minesweeper"):
                await bot.send_message(message.chat.id, locales.list_games[f'miner_{BotDB.user_language(message.from_user.id)}'], reply_markup=kb.markup_miner_select, parse_mode='html')
            elif (message.text == "🌗 50/50"):
                await bot.send_message(message.chat.id, locales.list_games[f'fifty_{BotDB.user_language(message.from_user.id)}'], reply_markup=kb.markup_fifty_select, parse_mode='html')
            elif (message.text == "🎰 Слоти" or message.text == "🎰 Слоты" or message.text == "🎰 Slots"):
                markup_spin_select = await kb.markup_spin_select(message)
                await bot.send_message(message.chat.id, locales.list_games[f'spin_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_spin_select, parse_mode='html')
            elif (message.text == "🎫 Взяти участь в лотереї" or message.text == "🎫 Принять участие в лотерее" or message.text == "🎫 Take part in the lottery"):
                markup_lot_buy = await kb.markup_lot_buy(message)
                await bot.send_message(message.chat.id, locales.list_games[f'lottery_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_lot_buy, parse_mode='html')
            elif (message.text == "📦 Кейси" or message.text == "📦 Кейсы" or message.text == "📦 Cases"):
                await bot.send_message(message.chat.id, locales.list_games[f'cases_{BotDB.user_language(message.from_user.id)}'], reply_markup=kb.markup_select_cases, parse_mode='html')
            elif (message.text == "🔙 Назад") or (message.text == "🔙 Back"):
                markup_start = await kb.markup_start(message)
                await bot.send_message(message.from_user.id, locales.reg_operation[f'main_menu_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_start, parse_mode='html')
                await bot.send_message(message.from_user.id, locales.reg_operation[f'select_menu_{BotDB.user_language(message.from_user.id)}'])
            elif (message.text == "🆘 Тех. Підтримка") or (message.text == "🆘 Тех. Поддержка") or (message.text == "🆘 Support"):
                markup = types.InlineKeyboardMarkup(row_width=1)
                change_language = types.InlineKeyboardButton('🔄 \n\nПоміняти мову | Сменить язык | Change the language', callback_data="change_language")
                up_button = types.InlineKeyboardButton(locales.tech_support[f'tech_support_button_{BotDB.user_language(message.from_user.id)}'], url="https://t.me/Christooo1")
                markup.add(change_language, up_button)
                photo = open('img/what-is-bot-management.png', 'rb')
                await bot.send_photo(message.from_user.id, photo, caption=locales.tech_support[f'tech_support_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup, parse_mode='html')
            elif (message.text == "🏆 Досягнення" or message.text == "🏆 Достижения" or message.text == "🏆 Achievements"):
                for value in cur.execute(f"SELECT daily_bonus, pay_trx, c_daily_bonus, c_pay_trx, pay_trx_th, c_pay_trx_th, c_f_ref, c_s_ref, c_a_ref, game_cub, c_game_cub, win_lot, c_win_lot, game_mine, c_game_mine FROM achivement WHERE user_id = {message.from_user.id}"):
                    cub = locales.achievement[f'minus_cube_{BotDB.user_language(message.from_user.id)}']
                    if value[9] >= 50:
                        cub = locales.achievement[f'plus_cube_{BotDB.user_language(message.from_user.id)}']

                    mine = locales.achievement[f'minus_miner_{BotDB.user_language(message.from_user.id)}']
                    if value[13] >= 40:
                        mine = locales.achievement[f'plus_miner_{BotDB.user_language(message.from_user.id)}']

                    f = locales.achievement[f'minus_f_ref_{BotDB.user_language(message.from_user.id)}']
                    if BotDB.count_ref(message.from_user.id) >= 35:
                        f = locales.achievement[f'plus_f_ref_{BotDB.user_language(message.from_user.id)}']

                    s = locales.achievement[f'minus_s_ref_{BotDB.user_language(message.from_user.id)}']
                    if BotDB.count_sec_ref(message.from_user.id) >= 15:
                        s = locales.achievement[f'plus_s_ref_{BotDB.user_language(message.from_user.id)}']

                    a = locales.achievement[f'minus_all_ref_{BotDB.user_language(message.from_user.id)}']
                    if (BotDB.count_ref(message.from_user.id) + BotDB.count_sec_ref(message.from_user.id) + BotDB.count_thi_ref(message.from_user.id)) >= 50:
                        a = locales.achievement[f'plus_all_ref_{BotDB.user_language(message.from_user.id)}']

                    day = locales.achievement[f'minus_day_bon_{BotDB.user_language(message.from_user.id)}']
                    if value[0] >= 30:
                        day = locales.achievement[f'plus_day_bon_{BotDB.user_language(message.from_user.id)}']

                    pay = locales.achievement[f'minus_pay_{BotDB.user_language(message.from_user.id)}']
                    if value[1] >= 250:
                        pay = locales.achievement[f'plus_pay_{BotDB.user_language(message.from_user.id)}']

                    pay_th = locales.achievement[f'minus_pay_th_{BotDB.user_language(message.from_user.id)}']
                    if value[4] >= 1000:
                        pay_th = locales.achievement[f'plus_pay_th_{BotDB.user_language(message.from_user.id)}']

                    win_lot = locales.achievement[f'minus_win_lot_{BotDB.user_language(message.from_user.id)}']
                    if value[11] >= 2:
                        win_lot = locales.achievement[f'plus_win_lot_{BotDB.user_language(message.from_user.id)}']

                    await bot.send_message(message.from_user.id, text=locales.achievement[f'achievement_{BotDB.user_language(message.from_user.id)}'].format(cub, value[9], mine, value[13], day, value[0], f, BotDB.count_ref(message.from_user.id), s, BotDB.count_sec_ref(message.from_user.id), a, BotDB.count_ref(message.from_user.id) + BotDB.count_sec_ref(message.from_user.id) + BotDB.count_thi_ref(message.from_user.id), win_lot, value[11], pay, value[1], pay_th, value[4]), parse_mode='html')

                    if value[0] >= 30:
                        if value[2] != 1:
                            await db.give_achivement_day(message.from_user.id)
                            await bot.send_message(message.chat.id, locales.achievement[f'done_day_bon_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                    if value[1] >= 250:
                        if value[3] != 1:
                            await db.give_achivement_pay(message.from_user.id)
                            await bot.send_message(message.chat.id, locales.achievement[f'done_pay_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                    if value[4] >= 1000:
                        if value[5] != 1:
                            await db.give_achivement_pay_th(message.from_user.id)
                            await bot.send_message(message.chat.id, locales.achievement[f'done_pay_th_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                    if BotDB.count_ref(message.from_user.id) >= 35:
                        if value[6] != 1:
                            await db.give_achivement_f(message.from_user.id)
                            await bot.send_message(message.chat.id, locales.achievement[f'done_f_ref_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                    if BotDB.count_sec_ref(message.from_user.id) >= 15:
                        if value[7] != 1:
                            await db.give_achivement_s(message.from_user.id)
                            await bot.send_message(message.chat.id, locales.achievement[f'done_s_ref_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                    if (BotDB.count_ref(message.from_user.id) + BotDB.count_sec_ref(message.from_user.id) + BotDB.count_thi_ref(message.from_user.id)) >= 50:
                        if value[8] != 1:
                            await db.give_achivement_a(message.from_user.id)
                            await bot.send_message(message.chat.id, locales.achievement[f'done_all_ref_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                    if value[9] >= 50:
                        if value[10] != 1:
                            await db.give_achivement_cub(message.from_user.id)
                            await bot.send_message(message.chat.id, locales.achievement[f'done_cube_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                    if value[11] >= 2:
                        if value[12] != 1:
                            await db.give_achivement_win_lot(message.from_user.id)
                            await bot.send_message(message.chat.id, locales.achievement[f'done_win_lot_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                    if value[13] >= 40:
                        if value[14] != 1:
                            await db.give_achivement_miner(message.from_user.id)
                            await bot.send_message(message.chat.id, locales.achievement[f'done_miner_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')

            elif (message.text == "👤 Партнерська програма" or message.text == "👤 Партнерская программа" or message.text == "👤 Partner program"):
                link = await get_start_link(message.from_user.id)
                photo = open('img/ref.jpg', 'rb')
                await bot.send_photo(message.from_user.id, photo, caption=locales.ref_program[f'ref_program_{BotDB.user_language(message.from_user.id)}'].format(link, BotDB.count_ref(message.from_user.id), BotDB.count_sec_ref(message.from_user.id), BotDB.count_thi_ref(message.from_user.id), BotDB.count_ref(message.from_user.id) + BotDB.count_sec_ref(message.from_user.id) + BotDB.count_thi_ref(message.from_user.id)), parse_mode='html')
            elif (message.text == "🎁 BONUS"):
                photo = open('img/bonus_img.jpg', 'rb')
                markup_bonus = await kb.markup_bonus(message)
                await bot.send_photo(message.from_user.id, photo, caption=locales.bonus[f'bonus_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_bonus, parse_mode='html')
            elif (message.text == "🅿 Наш Patreon" or message.text == "🅿 Our Patreon"):
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🅿 Patreon", url="patreon.com/TelegramTRXBot"))
                photo = open('img/patreon.png', 'rb')
                await bot.send_photo(message.from_user.id, photo, caption=locales.patreon[f'patreon_{BotDB.user_language(message.from_user.id)}'], parse_mode='html', reply_markup=markup)
            elif (message.text == "📳 Мій кабінет" or message.text == "📳 Мой кабинет" or message.text == "📳 My office"):
                for value in cur.execute(f"SELECT bal_dol, bal_trx, user_id, join_date, user_level, patron FROM users WHERE user_id = {message.from_user.id}"):
                    photo = open('img/my_cab.jpg', 'rb')
                    if value[5] == 0:
                        patron = '❌😞'
                    else:
                        patron = '〰   👑   〰'
                    markup_cab = await kb.markup_cab(message)
                    await bot.send_photo(message.from_user.id, photo, caption=locales.cabinet[f'cabinet_{BotDB.user_language(message.from_user.id)}'].format(value[2], value[4], patron, value[0], value[1], value[3], BotDB.count_ref(message.from_user.id) + BotDB.count_sec_ref(message.from_user.id) + BotDB.count_thi_ref(message.from_user.id), BotDB.count_ref(message.from_user.id), BotDB.count_sec_ref(message.from_user.id), BotDB.count_thi_ref(message.from_user.id)), reply_markup=markup_cab, parse_mode='html')
            elif (message.text == "📊 Статистика TRON" or message.text == "📊 TRON Statistics"):
                for value in cur.execute(f"SELECT all_acc, pay_trx, active_acc, day_acc FROM stats"):
                    photo = open('img/stat_img.jpg', 'rb')
                    await bot.send_photo(message.from_user.id, photo, caption=locales.stat[f'stat_{BotDB.user_language(message.from_user.id)}'].format(value[0], value[3], value[2], value[1]), parse_mode='html')
            elif (message.text == "🤑 Отримати до 1.000 TRX" or message.text == "🤑 Получить до 1.000 TRX" or message.text == "🤑 Get up to 1.000 TRX"):
                photo = open('img/thousend_trx.jpg', 'rb')
                await bot.send_photo(message.from_user.id, photo, caption=locales.more_trx[f'more_trx_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
            elif (message.text == "📱 Рекламний кабінет" or message.text == "📱 Рекламный кабинет" or message.text == "📱 Advertising office"):
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(locales.ad[f'ad_button_{BotDB.user_language(message.from_user.id)}'], url="https://t.me/Christooo1"))
                await bot.send_message(message.from_user.id, text=locales.ad[f'ad_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup, parse_mode='html')
            elif (message.text == "🗣 Поділитись історією/музикою" or message.text == "🗣 Поделиться историей/музыкой" or message.text == "🗣 Share a story/music"):#👋 Передати всім привіт
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(locales.say_hi[f'say_hi_button_{BotDB.user_language(message.from_user.id)}'], callback_data='say_hi_inline'))
                await bot.send_message(message.from_user.id, text=locales.say_hi[f'say_hi_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup, parse_mode='html')
            elif (message.text == "❤ Підтримати бота" or message.text == "❤ Поддержать бота" or message.text == "❤ Support bot"):
                await bot.send_message(message.from_user.id, text=locales.donation[f'donation_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
            else:
                await bot.send_message(message.from_user.id, locales.error_command[f'error_command_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
            if message.content_type == 'text':
                if message.text != 'Покажи переписки':
                    worksheet.write(count, 0, str(dt.datetime.now().date()))
                    worksheet.write(count, 1, str(dt.datetime.now().time())[0:8])
                    worksheet.write(count, 2, 'текст')
                    worksheet.write(count, 3, str(message.from_user.first_name) + ' ' + str(message.from_user.last_name))
                    worksheet.write(count, 4, message.from_user.id)
                    worksheet.write(count, 5, message.text)
                    count += 1
                else:
                    workbook.close()
        else:
            await message.answer(locales.ban[f'ban_{BotDB.user_language(message.from_user.id)}'], parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())


#######################################################################################################################################


#######################################################################################################################################
@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    markup_games = await kb.markup_games(message)
    await message.answer(locales.quit_game[f'quit_game_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_games)

@dp.message_handler(state='*', commands='cancel_promo_code')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    markup_start = await kb.markup_start(message)
    await message.answer(locales.quit_promo[f'quit_promo_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_start)
#######################################################################################################################################



#######################################################################################################################################
@dp.message_handler(content_types=['sticker'])
async def send_sticker(message : types.Message):
    global count
    if message.content_type == 'sticker':
        if message.text != 'Покажи переписки':
            worksheet.write(count, 0, str(dt.datetime.now().date()))
            worksheet.write(count, 1, str(dt.datetime.now().time())[0:8])
            worksheet.write(count, 2, 'стікер')
            worksheet.write(count, 3, str(message.from_user.first_name) + ' ' + str(message.from_user.last_name))
            worksheet.write(count, 4, message.from_user.id)
            worksheet.write(count, 5, message.sticker.file_id)
            worksheet.write(count, 6, message.sticker.emoji)
            count += 1
        else:
            workbook.close()
#######################################################################################################################################
