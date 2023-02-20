from aiogram import types

import locales
from dispatcher import CHANNELS
from db import BotDB
import random

async def markup_channels(message: types.Message):
    markup_channels = types.InlineKeyboardMarkup(row_width=1)
    for channel in CHANNELS:
        btn_channels = types.InlineKeyboardButton(text=channel[0], url=channel[2])
        markup_channels.insert(btn_channels)
    btn_done_sub = types.InlineKeyboardButton(text=locales.markup_channels[f'sub_channel_done_{BotDB.user_language(message.chat.id)}'], callback_data="sub_channel_done")
    markup_channels.insert(btn_done_sub)
    return markup_channels

async def markup_start(message: types.Message):
    markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    earn = types.KeyboardButton(locales.markup_start[f'markup_start_game_{BotDB.user_language(message.chat.id)}'])
    stat = types.KeyboardButton(locales.markup_start[f'markup_start_stat_{BotDB.user_language(message.chat.id)}'])
    sos = types.KeyboardButton(locales.markup_start[f'markup_start_sos_{BotDB.user_language(message.chat.id)}'])
    ref = types.KeyboardButton(locales.markup_start[f'markup_start_ref_{BotDB.user_language(message.chat.id)}'])
    ad = types.KeyboardButton(locales.markup_start[f'markup_start_ad_{BotDB.user_language(message.chat.id)}'])
    cabinet = types.KeyboardButton(locales.markup_start[f'markup_start_cabinet_{BotDB.user_language(message.chat.id)}'])
    bonus = types.KeyboardButton(locales.markup_start[f'markup_start_bon_{BotDB.user_language(message.chat.id)}'])
    achivments = types.KeyboardButton(locales.markup_start[f'markup_start_ach_{BotDB.user_language(message.chat.id)}'])
    say_hi = types.KeyboardButton(locales.markup_start[f'markup_start_say_hi_{BotDB.user_language(message.chat.id)}'])
    donation = types.KeyboardButton(locales.markup_start[f'markup_start_donation_{BotDB.user_language(message.chat.id)}'])
    patreon = types.KeyboardButton(locales.markup_start[f'markup_start_patreon_{BotDB.user_language(message.chat.id)}'])
    more_trx = types.KeyboardButton(locales.markup_start[f'markup_start_more_trx_{BotDB.user_language(message.chat.id)}'])
    markup_start.add(earn).row(cabinet, ref).row(bonus, achivments).row(stat, more_trx).add(say_hi).add(donation).add(patreon).add(ad, sos)
    return markup_start

async def markup_games(message: types.Message):
    markup_games = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    lot = types.KeyboardButton(locales.markup_games[f'markup_games_lot_{BotDB.user_language(message.from_user.id)}'])
    num = types.KeyboardButton(locales.markup_games[f'markup_games_num_{BotDB.user_language(message.from_user.id)}'])
    cases = types.KeyboardButton(locales.markup_games[f'markup_games_cases_{BotDB.user_language(message.from_user.id)}'])
    cub = types.KeyboardButton(locales.markup_games[f'markup_games_cub_{BotDB.user_language(message.from_user.id)}'])
    mines = types.KeyboardButton(locales.markup_games[f'markup_games_mines_{BotDB.user_language(message.from_user.id)}'])
    half = types.KeyboardButton(locales.markup_games[f'markup_games_half_{BotDB.user_language(message.from_user.id)}'])
    spin = types.KeyboardButton(locales.markup_games[f'markup_games_spin_{BotDB.user_language(message.from_user.id)}'])
    exit = types.KeyboardButton(locales.markup_games[f'markup_games_exit_{BotDB.user_language(message.from_user.id)}'])
    markup_games.add(lot).add(half, cases, num, cub, mines, spin).add(exit)
    return markup_games

async def markup_games_(message: types.Message):
    markup_games = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    lot = types.KeyboardButton(locales.markup_games[f'markup_games_lot_{BotDB.user_language(message.chat.id)}'])
    num = types.KeyboardButton(locales.markup_games[f'markup_games_num_{BotDB.user_language(message.chat.id)}'])
    cases = types.KeyboardButton(locales.markup_games[f'markup_games_cases_{BotDB.user_language(message.chat.id)}'])
    cub = types.KeyboardButton(locales.markup_games[f'markup_games_cub_{BotDB.user_language(message.chat.id)}'])
    mines = types.KeyboardButton(locales.markup_games[f'markup_games_mines_{BotDB.user_language(message.chat.id)}'])
    half = types.KeyboardButton(locales.markup_games[f'markup_games_half_{BotDB.user_language(message.chat.id)}'])
    spin = types.KeyboardButton(locales.markup_games[f'markup_games_spin_{BotDB.user_language(message.chat.id)}'])
    exit = types.KeyboardButton(locales.markup_games[f'markup_games_exit_{BotDB.user_language(message.chat.id)}'])
    markup_games.add(lot).add(half, cases, num, cub, mines, spin).add(exit)
    return markup_games

markup_select_language = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
ukrainian = types.KeyboardButton('🇺🇦 Українська')
russian = types.KeyboardButton('🇷🇺 Русский')
english = types.KeyboardButton('🇬🇧 English')
markup_select_language.add(ukrainian, russian, english)

markup_change_language = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=3)
ukrainian = types.InlineKeyboardButton('🇺🇦 Українська', callback_data="ua_lang")
russian = types.InlineKeyboardButton('🇷🇺 Русский', callback_data="ru_lang")
english = types.InlineKeyboardButton('🇬🇧 English', callback_data="en_lang")
markup_change_language.add(ukrainian, russian, english)

markup_select_bet = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
one_bet = types.KeyboardButton('1')
five_bet = types.KeyboardButton('5')
ten_bet = types.KeyboardButton('10')
quarter_bet = types.KeyboardButton('25')
half_bet = types.KeyboardButton('50')
hun_bet = types.KeyboardButton('100')
cancel_bet = types.KeyboardButton('/cancel')
markup_select_bet.add(one_bet, five_bet, ten_bet, quarter_bet, half_bet, hun_bet, cancel_bet)

async def markup_bonus(message: types.Message):
    markup_bonus = types.InlineKeyboardMarkup()
    day_bon = types.InlineKeyboardButton(locales.markup_bonus[f'day_bon_{BotDB.user_language(message.chat.id)}'], callback_data='day_bon_cab')
    wek_bon = types.InlineKeyboardButton(locales.markup_bonus[f'wek_bon_{BotDB.user_language(message.chat.id)}'], callback_data='wek_bon_cab')
    promo_bon = types.InlineKeyboardButton(locales.markup_bonus[f'promo_bon_{BotDB.user_language(message.chat.id)}'], callback_data='promo_bon_cab')
    markup_bonus.add(promo_bon).add(day_bon, wek_bon)
    return markup_bonus

async def markup_say(message: types.Message):
    markup_say_hi_add_photo = types.InlineKeyboardMarkup()
    markup_say_hi_add_audio = types.InlineKeyboardMarkup(row_width=2)
    markup_say_hi_add_audio_mod = types.InlineKeyboardMarkup(row_width=2)
    say_hi_add_photo = types.InlineKeyboardButton(locales.markup_say_hi[f'add_photo_{BotDB.user_language(message.from_user.id)}'], callback_data='add_photo')
    say_hi_add_audio = types.InlineKeyboardButton(locales.markup_say_hi[f'add_song_{BotDB.user_language(message.from_user.id)}'], callback_data='add_song')
    send_say_hi = types.InlineKeyboardButton(locales.markup_say_hi[f'next_{BotDB.user_language(message.from_user.id)}'], callback_data='next')
    send_say_hi_mod = types.InlineKeyboardButton(locales.markup_say_hi[f'send_text_msg_{BotDB.user_language(message.from_user.id)}'], callback_data='send_text_msg')
    next_say_hi = types.InlineKeyboardButton(locales.markup_say_hi[f'next_second_{BotDB.user_language(message.from_user.id)}'], callback_data='next')
    quit_say_hi = types.InlineKeyboardButton(locales.markup_say_hi[f'quit_{BotDB.user_language(message.from_user.id)}'], callback_data='quit')
    markup_say_hi_add_photo.add(say_hi_add_photo).add(next_say_hi, quit_say_hi)
    markup_say_hi_add_audio.add(say_hi_add_audio).add(send_say_hi, quit_say_hi)
    markup_say_hi_add_audio_mod.add(say_hi_add_audio).add(send_say_hi_mod, quit_say_hi)
    return [markup_say_hi_add_photo, markup_say_hi_add_audio, markup_say_hi_add_audio_mod]###############################################

markup_admin = types.InlineKeyboardMarkup(row_width=1)
del_trx_admin = types.InlineKeyboardButton(f'⬆ Заявки на вивід ({BotDB.count_del_trx_admin(0)})', callback_data='del_trx_admin')
add_trx_admin = types.InlineKeyboardButton(f'💶 Заявки на поповнення TRX ({BotDB.count_add_trx_admin(0)})', callback_data='add_trx_admin')
say_hi_admin_kb = types.InlineKeyboardButton(f'🗣 Поділитись історією/музикою ({BotDB.count_say_hi_admin(0)})', callback_data='say_hi_admin_kb')
add_usd_admin = types.InlineKeyboardButton(f'💲 Заявки на поповнення USDT ({BotDB.count_add_usd_admin(0)})', callback_data='add_usd_admin')
work_user_admin = types.InlineKeyboardButton(f'🤖 Робота з користувачем', callback_data='work_user_admin')
mailing_admin = types.InlineKeyboardButton(f'✍ Розсилка', callback_data='mailing_admin')
markup_admin.add(del_trx_admin, add_trx_admin, add_usd_admin, say_hi_admin_kb, mailing_admin, work_user_admin)

async def markup_cab(message: types.Message):
    markup_cab = types.InlineKeyboardMarkup(row_width=2)
    add_usd = types.InlineKeyboardButton(locales.markup_cab[f'add_usd_cab_{BotDB.user_language(message.chat.id)}'], callback_data='add_usd_cab')
    add_trx = types.InlineKeyboardButton(locales.markup_cab[f'add_trx_cab_{BotDB.user_language(message.chat.id)}'], callback_data='add_trx_cab')
    del_trx = types.InlineKeyboardButton(locales.markup_cab[f'del_trx_cab_{BotDB.user_language(message.chat.id)}'], callback_data='del_trx_cab')
    what_is_lvl = types.InlineKeyboardButton(locales.markup_cab[f'what_is_lvl_{BotDB.user_language(message.chat.id)}'], callback_data='what_is_lvl')
    check_lvl = types.InlineKeyboardButton(locales.markup_cab[f'check_lvl_{BotDB.user_language(message.chat.id)}'], callback_data='check_lvl')
    history_pay = types.InlineKeyboardButton(locales.markup_cab[f'history_pay_cab_{BotDB.user_language(message.chat.id)}'], callback_data='history_pay_cab')
    markup_cab.add(add_usd, add_trx, del_trx).add(what_is_lvl, check_lvl).add(history_pay)
    return markup_cab

markup_work_admin = types.InlineKeyboardMarkup(row_width=2)
work_admin_trx = types.InlineKeyboardButton('💳 Баланс TRX', callback_data='work_admin_trx')
work_admin_usd = types.InlineKeyboardButton('💲 Баланс USDT', callback_data='work_admin_usd')
work_admin_ban = types.InlineKeyboardButton('☠ Чорний список', callback_data='work_admin_ban')
work_admin_patreon = types.InlineKeyboardButton('🅿 Patreon', callback_data='work_admin_patreon')
markup_work_admin.add(work_admin_trx, work_admin_usd, work_admin_ban).add(work_admin_patreon)

markup_work_admin_select_trx = types.InlineKeyboardMarkup(row_width=2)
work_admin_trx_select_trx = types.InlineKeyboardButton('💷 Поповнення балансу TRX', callback_data='work_admin_trx_select_trx')
work_admin_trx_del_select_trx = types.InlineKeyboardButton('💸 Зняття з балансу TRX', callback_data='work_admin_trx_del_select_trx')
markup_work_admin_select_trx.add(work_admin_trx_select_trx, work_admin_trx_del_select_trx)

markup_work_admin_select_usd = types.InlineKeyboardMarkup(row_width=2)
work_admin_trx_select_usd = types.InlineKeyboardButton('💷 Поповнення балансу USDT', callback_data='work_admin_trx_select_usd')
work_admin_usd_del_select_usd = types.InlineKeyboardButton('💸 Зняття з балансу USDT', callback_data='work_admin_usd_del_select_usd')
markup_work_admin_select_usd.add(work_admin_trx_select_usd, work_admin_usd_del_select_usd)

markup_work_admin_select_patreon = types.InlineKeyboardMarkup(row_width=2)
work_admin_select_patreon = types.InlineKeyboardButton('✅ Став патроном', callback_data='work_admin_select_patreon')
work_admin_del_select_patreon = types.InlineKeyboardButton('❌ Перестав бути патроном', callback_data='work_admin_del_select_patreon')
work_admin_patreon_list = types.InlineKeyboardButton('📋 Список патронів', callback_data='work_admin_patreon_list')
markup_work_admin_select_patreon.add(work_admin_select_patreon, work_admin_del_select_patreon, work_admin_patreon_list)

markup_work_admin_select_ban = types.InlineKeyboardMarkup(row_width=2)
work_admin_trx_select_ban = types.InlineKeyboardButton('👎 Забанити', callback_data='work_admin_ban_select_ban')
work_admin_usd_del_select_ban = types.InlineKeyboardButton('👍 Розбанити', callback_data='work_admin_unban_select_ban')
work_admin_ban_list = types.InlineKeyboardButton('📋 Список забанених', callback_data='work_admin_ban_list')
markup_work_admin_select_ban.add(work_admin_trx_select_ban, work_admin_usd_del_select_ban, work_admin_ban_list)

async def markup_pay_history(message: types.Message):
    markup_pay_history = types.InlineKeyboardMarkup(row_width=3)
    pay_history_day = types.InlineKeyboardButton(locales.markup_pay_history[f'pay_history_day_cab_{BotDB.user_language(message.chat.id)}'], callback_data='pay_history_day_cab')
    pay_history_month = types.InlineKeyboardButton(locales.markup_pay_history[f'pay_history_month_cab_{BotDB.user_language(message.chat.id)}'], callback_data='pay_history_month_cab')
    pay_history_year = types.InlineKeyboardButton(locales.markup_pay_history[f'pay_history_year_cab_{BotDB.user_language(message.chat.id)}'], callback_data='pay_history_year_cab')
    markup_pay_history.add(pay_history_day, pay_history_month, pay_history_year)
    return markup_pay_history

markup_pay_history_admin = types.InlineKeyboardMarkup(row_width=2)
pay_history_day_admin = types.InlineKeyboardButton('🕐 День', callback_data='pay_history_day_admin')
pay_history_month_admin = types.InlineKeyboardButton('🕝 Місяць', callback_data='pay_history_month_admin')
pay_history_year_admin = types.InlineKeyboardButton('🕤 Рік', callback_data='pay_history_year_admin')
pay_history_all_admin = types.InlineKeyboardButton('🕧 Весь час', callback_data='pay_history_all_admin')
pay_admin = types.InlineKeyboardButton('👤 Адмін панель', callback_data='pay_admin')
pay_history_all_not_acces_admin_del_trx = types.InlineKeyboardButton('⭕ Тільки не виконані', callback_data='pay_history_all_not_acces_admin_del_trx')
pay_admin_kb_do_acces = types.InlineKeyboardButton('🚥 Змінити статус операції', callback_data='pay_admin_kb_do_acces')
markup_pay_history_admin.add(pay_history_day_admin, pay_history_month_admin, pay_history_year_admin, pay_history_all_admin).add(pay_admin_kb_do_acces).add(pay_history_all_not_acces_admin_del_trx).add(pay_admin)

markup_say_hi_admin_kb = types.InlineKeyboardMarkup(row_width=2)
say_hi_admin_kb_day_admin = types.InlineKeyboardButton('🕐 День', callback_data='say_hi_admin_kb_day_admin')
say_hi_admin_kb_month_admin = types.InlineKeyboardButton('🕝 Місяць', callback_data='say_hi_admin_kb_month_admin')
say_hi_admin_kb_year_admin = types.InlineKeyboardButton('🕤 Рік', callback_data='say_hi_admin_kb_year_admin')
say_hi_admin_kb_all_admin = types.InlineKeyboardButton('🕧 Весь час', callback_data='say_hi_admin_kb_all_admin')
pay_admin = types.InlineKeyboardButton('👤 Адмін панель', callback_data='pay_admin')
say_hi_all_not_acces_admin = types.InlineKeyboardButton('⭕ Тільки не виконані', callback_data='say_hi_all_not_acces_admin')
say_hi_admin_kb_do_acces = types.InlineKeyboardButton('🚥 Змінити статус операції', callback_data='say_hi_admin_kb_do_acces')
markup_say_hi_admin_kb.add(say_hi_admin_kb_day_admin, say_hi_admin_kb_month_admin, say_hi_admin_kb_year_admin, say_hi_admin_kb_all_admin, say_hi_all_not_acces_admin).add(say_hi_admin_kb_do_acces).add(pay_admin)

markup_pay_history_admin_add_trx = types.InlineKeyboardMarkup(row_width=2)
pay_history_day_admin_add_trx = types.InlineKeyboardButton('🕐 День', callback_data='pay_history_day_admin_add_trx')
pay_history_month_admin_add_trx = types.InlineKeyboardButton('🕝 Місяць', callback_data='pay_history_month_admin_add_trx')
pay_history_year_admin_add_trx = types.InlineKeyboardButton('🕤 Рік', callback_data='pay_history_year_admin_add_trx')
pay_history_all_admin_add_trx = types.InlineKeyboardButton('🕧 Весь час', callback_data='pay_history_all_admin_add_trx')
pay_history_all_not_acces_admin_add_trx = types.InlineKeyboardButton('⭕ Тільки не виконані', callback_data='pay_history_all_not_acces_admin_add_trx')
pay_admin_kb_do_acces_add_trx = types.InlineKeyboardButton('🚥 Змінити статус операції', callback_data='pay_admin_kb_do_acces_add_trx')
markup_pay_history_admin_add_trx.add(pay_history_day_admin_add_trx, pay_history_month_admin_add_trx, pay_history_year_admin_add_trx, pay_history_all_admin_add_trx).add(pay_admin_kb_do_acces_add_trx).add(pay_history_all_not_acces_admin_add_trx).add(pay_admin)

markup_pay_history_admin_add_usd = types.InlineKeyboardMarkup(row_width=2)
pay_history_day_admin_add_usd = types.InlineKeyboardButton('🕐 День', callback_data='pay_history_day_admin_add_usd')
pay_history_month_admin_add_usd = types.InlineKeyboardButton('🕝 Місяць', callback_data='pay_history_month_admin_add_usd')
pay_history_year_admin_add_usd = types.InlineKeyboardButton('🕤 Рік', callback_data='pay_history_year_admin_add_usd')
pay_history_all_admin_add_usd = types.InlineKeyboardButton('🕧 Весь час', callback_data='pay_history_all_admin_add_usd')
pay_history_all_not_acces_admin_add_usd = types.InlineKeyboardButton('⭕ Тільки не виконані', callback_data='pay_history_all_not_acces_admin_add_usd')
pay_admin_kb_do_acces_add_usd = types.InlineKeyboardButton('🚥 Змінити статус операції', callback_data='pay_admin_kb_do_acces_add_usd')
markup_pay_history_admin_add_usd.add(pay_history_day_admin_add_usd, pay_history_month_admin_add_usd, pay_history_year_admin_add_usd, pay_history_all_admin_add_usd).add(pay_admin_kb_do_acces_add_usd).add(pay_history_all_not_acces_admin_add_usd).add(pay_admin)

markup_pay_admin_kb_do_acces_add_usd = types.InlineKeyboardMarkup(row_width=2)
pay_admin_kb_do_acces_add_usd_set_null = types.InlineKeyboardButton('❌ Відмінити', callback_data='pay_admin_kb_do_acces_add_usd_set_null')
pay_admin_kb_do_acces_add_usd_set_one = types.InlineKeyboardButton('✅ Підтвердити', callback_data='pay_admin_kb_do_acces_add_usd_set_one')
pay_admin_kb_do_acces_add_usd_set_two = types.InlineKeyboardButton('💢 Помилка виконання', callback_data='pay_admin_kb_do_acces_add_usd_set_two')
markup_pay_admin_kb_do_acces_add_usd.add(pay_admin_kb_do_acces_add_usd_set_one, pay_admin_kb_do_acces_add_usd_set_null, pay_admin_kb_do_acces_add_usd_set_two)

markup_pay_admin_kb_do_acces_add_trx = types.InlineKeyboardMarkup(row_width=2)
pay_admin_kb_do_acces_add_trx_set_null = types.InlineKeyboardButton('❌ Відмінити', callback_data='pay_admin_kb_do_acces_add_trx_set_null')
pay_admin_kb_do_acces_add_trx_set_one = types.InlineKeyboardButton('✅ Підтвердити', callback_data='pay_admin_kb_do_acces_add_trx_set_one')
pay_admin_kb_do_acces_add_trx_set_two = types.InlineKeyboardButton('💢 Помилка виконання', callback_data='pay_admin_kb_do_acces_add_trx_set_two')
markup_pay_admin_kb_do_acces_add_trx.add(pay_admin_kb_do_acces_add_trx_set_one, pay_admin_kb_do_acces_add_trx_set_null, pay_admin_kb_do_acces_add_trx_set_two)

markup_pay_admin_kb_do_acces_del_trx = types.InlineKeyboardMarkup(row_width=2)
pay_admin_kb_do_acces_del_trx_set_null = types.InlineKeyboardButton('❌ Відмінити', callback_data='pay_admin_kb_do_acces_del_trx_set_null')
pay_admin_kb_do_acces_del_trx_set_one = types.InlineKeyboardButton('✅ Підтвердити', callback_data='pay_admin_kb_do_acces_del_trx_set_one')
pay_admin_kb_do_acces_del_trx_set_two = types.InlineKeyboardButton('💢 Помилка виконання', callback_data='pay_admin_kb_do_acces_del_trx_set_two')
markup_pay_admin_kb_do_acces_del_trx.add(pay_admin_kb_do_acces_del_trx_set_one, pay_admin_kb_do_acces_del_trx_set_null, pay_admin_kb_do_acces_del_trx_set_two)

async def markup_succes(message: types.Message):
    markup_succes = types.InlineKeyboardMarkup(row_width=1)
    accept = types.InlineKeyboardButton(locales.markup_succes[f'markup_succes_{BotDB.user_language(message.chat.id)}'], callback_data='accept_cab')
    markup_succes.add(accept)
    return markup_succes

markup_work_add_trx_admin = types.InlineKeyboardMarkup(row_width=1)
work_add_trx_admin = types.InlineKeyboardButton('✅ Підтвердити', callback_data='work_add_trx_admin')
work_add_trx_admin_cancel = types.InlineKeyboardButton('❌ Відмінити', callback_data='work_add_trx_admin_cancel')
markup_work_add_trx_admin.add(work_add_trx_admin, work_add_trx_admin_cancel)

async def markup_succes_say_hi(message: types.Message):
    markup_succes_say_hi = types.InlineKeyboardMarkup(row_width=2)
    succes_say_hi = types.InlineKeyboardButton(locales.markup_succes_say_hi[f'succes_say_hi_{BotDB.user_language(message.from_user.id)}'], callback_data='succes_say_hi')
    quit_say_hi = types.InlineKeyboardButton(locales.markup_succes_say_hi[f'quit_{BotDB.user_language(message.from_user.id)}'], callback_data='quit')
    markup_succes_say_hi.add(succes_say_hi, quit_say_hi)
    return markup_succes_say_hi

async def markup_lot_buy(message: types.Message):
    markup_lot_buy = types.InlineKeyboardMarkup(row_width=1)
    lot_buy = types.InlineKeyboardButton(locales.markup_lot_buy[f'markup_lot_buy_{BotDB.user_language(message.chat.id)}'], callback_data='lot_buy_game')
    markup_lot_buy.add(lot_buy)
    return markup_lot_buy

async def markup_again_guess_five(message: types.Message):
    markup_again_guess_five = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.chat.id)}'], callback_data='again_guess_five')
    markup_again_guess_five.add(rules_exit)
    return markup_again_guess_five

async def markup_again_guess_ten(message: types.Message):
    markup_again_guess_ten = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.chat.id)}'], callback_data='again_guess_ten')
    markup_again_guess_ten.add(rules_exit)
    return markup_again_guess_ten

async def markup_again_guess_hun(message: types.Message):
    markup_again_guess_hun = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.chat.id)}'], callback_data='again_guess_hun')
    markup_again_guess_hun.add(rules_exit)
    return markup_again_guess_hun

async def markup_again_fifty_two(message: types.Message):
    markup_again_fifty_two = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.chat.id)}'], callback_data='again_fifty_two')
    markup_again_fifty_two.add(rules_exit)
    return markup_again_fifty_two

async def markup_again_fifty_four(message: types.Message):
    markup_again_fifty_four = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.chat.id)}'], callback_data='again_fifty_four')
    markup_again_fifty_four.add(rules_exit)
    return markup_again_fifty_four

async def markup_again_dice_classic(message: types.Message):
    markup_again_dice_classic = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.chat.id)}'], callback_data='again_dice_classic')
    markup_again_dice_classic.add(rules_exit)
    return markup_again_dice_classic

async def markup_again_dice_under(message: types.Message):
    markup_again_dice_under = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.chat.id)}'], callback_data='again_dice_under')
    markup_again_dice_under.add(rules_exit)
    return markup_again_dice_under

async def markup_again_br_case(message: types.Message):
    markup_again_br_case = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.from_user.id)}'], callback_data='again_br_case')
    markup_again_br_case.add(rules_exit)
    return markup_again_br_case

async def markup_again_si_case(message: types.Message):
    markup_again_si_case = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.from_user.id)}'], callback_data='again_si_case')
    markup_again_si_case.add(rules_exit)
    return markup_again_si_case

async def markup_again_go_case(message: types.Message):
    markup_again_go_case = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.from_user.id)}'], callback_data='again_go_case')
    markup_again_go_case.add(rules_exit)
    return markup_again_go_case

async def markup_again_miner_three(message: types.Message):
    markup_again_miner_three = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.chat.id)}'], callback_data='again_miner_three')
    markup_again_miner_three.add(rules_exit)
    return markup_again_miner_three

async def markup_again_miner_five(message: types.Message):
    markup_again_miner_five = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.chat.id)}'], callback_data='again_miner_five')
    markup_again_miner_five.add(rules_exit)
    return markup_again_miner_five

async def markup_again_miner_seven(message: types.Message):
    markup_again_miner_seven = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.chat.id)}'], callback_data='again_miner_seven')
    markup_again_miner_seven.add(rules_exit)
    return markup_again_miner_seven

async def markup_again_slot(message: types.Message):
    markup_again_slot = types.InlineKeyboardMarkup(row_width=1)
    rules_exit = types.InlineKeyboardButton(locales.markup_again[f'markup_again_{BotDB.user_language(message.chat.id)}'], callback_data='again_slot')
    markup_again_slot.add(rules_exit)
    return markup_again_slot

markup_guess_select = types.InlineKeyboardMarkup(row_width=3)
five_num_guess = types.InlineKeyboardButton('5️⃣', callback_data='five_num_guess_game')
ten_num_guess = types.InlineKeyboardButton('1️⃣0️⃣', callback_data='ten_num_guess_game')
hun_num_guess = types.InlineKeyboardButton('1️⃣0️⃣0️⃣', callback_data='hun_num_guess_game')
markup_guess_select.add(five_num_guess, ten_num_guess, hun_num_guess)

markup_fifty_select = types.InlineKeyboardMarkup(row_width=2)
two_num_fifty = types.InlineKeyboardButton('2️⃣', callback_data='two_num_fifty_game')
four_num_fifty = types.InlineKeyboardButton('4️⃣', callback_data='four_num_fifty_game')
markup_fifty_select.add(two_num_fifty, four_num_fifty)

markup_select_cases = types.InlineKeyboardMarkup(row_width=3)
br_case = types.InlineKeyboardButton('📦', callback_data='br_case_game')
si_case = types.InlineKeyboardButton('🎒', callback_data='si_case_game')
go_cale = types.InlineKeyboardButton('💼', callback_data='go_case_game')
markup_select_cases.add(br_case, si_case, go_cale)

async def markup_accept_cases(message: types.Message):
    markup_accept_cases = types.InlineKeyboardMarkup()
    accept = types.InlineKeyboardButton(locales.markup_accept_cases[f'markup_accept_cases_{BotDB.user_language(message.chat.id)}'], callback_data='accept_case_game')
    markup_accept_cases.add(accept)
    return markup_accept_cases

list_buts = [("️⃣", "field_1"), ("️⃣", "field_2"), ("️⃣", "field_3"), ("⃣", "field_4"), ("⃣", "field_5"), ("⃣", "field_6"), ("⃣", "field_7"), ("⃣", "field_8"), ("⃣", "field_9")]

async def markup_dice_select(message: types.Message):
    markup_dice_select = types.InlineKeyboardMarkup(row_width=2)
    under_s = types.InlineKeyboardButton(locales.markup_dice_select[f'under_s_game_{BotDB.user_language(message.chat.id)}'], callback_data='under_s_game')
    classic_dice = types.InlineKeyboardButton(locales.markup_dice_select[f'under_s_game_{BotDB.user_language(message.chat.id)}'], callback_data='classic_dice_game')
    markup_dice_select.add(under_s, classic_dice)
    return markup_dice_select

async def markup_spin_select(message: types.Message):
    markup_spin_select = types.InlineKeyboardMarkup()
    accept = types.InlineKeyboardButton(locales.markup_spin_select[f'markup_spin_select_{BotDB.user_language(message.chat.id)}'], callback_data='accept_spin')
    markup_spin_select.add(accept)
    return markup_spin_select

markup_miner_select = types.InlineKeyboardMarkup(row_width=3)
miner_three = types.InlineKeyboardButton('3️⃣', callback_data='miner_three_game')
miner_five = types.InlineKeyboardButton('5️⃣', callback_data='miner_five_game')
miner_seven = types.InlineKeyboardButton('7️⃣', callback_data='miner_seven_game')
markup_miner_select.add(miner_three, miner_five, miner_seven)


markup_select_rand_num_hun = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=10)
markup_select_rand_num_ten = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
markup_select_rand_num_five = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
markup_select_fifty_two = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup_select_fifty_four = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup_select_fifty_ten = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup_select_dice_classic = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
markup_select_del_trx = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
markup_select_add_trx = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
markup_select_add_usdt = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
markup_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
one_num = types.KeyboardButton('1')
two_num = types.KeyboardButton('2')
three_num = types.KeyboardButton('3')
four_num = types.KeyboardButton('4')
five_num = types.KeyboardButton('5')
six_num = types.KeyboardButton('6')
seven_num = types.KeyboardButton('7')
eight_num = types.KeyboardButton('8')
nine_num = types.KeyboardButton('9')
ten_num = types.KeyboardButton('10')
t_one_num = types.KeyboardButton('11')
t_two_num = types.KeyboardButton('12')
t_three_num = types.KeyboardButton('13')
t_four_num = types.KeyboardButton('14')
t_five_num = types.KeyboardButton('15')
t_six_num = types.KeyboardButton('16')
t_seven_num = types.KeyboardButton('17')
t_eight_num = types.KeyboardButton('18')
t_nine_num = types.KeyboardButton('19')
t_ten_num = types.KeyboardButton('20')
tw_one_num = types.KeyboardButton('21')
tw_two_num = types.KeyboardButton('22')
tw_three_num = types.KeyboardButton('23')
tw_four_num = types.KeyboardButton('24')
tw_five_num = types.KeyboardButton('25')
tw_six_num = types.KeyboardButton('26')
tw_seven_num = types.KeyboardButton('27')
tw_eight_num = types.KeyboardButton('28')
tw_nine_num = types.KeyboardButton('29')
tw_ten_num = types.KeyboardButton('30')
th_one_num = types.KeyboardButton('31')
th_two_num = types.KeyboardButton('32')
th_three_num = types.KeyboardButton('33')
th_four_num = types.KeyboardButton('34')
th_five_num = types.KeyboardButton('35')
th_six_num = types.KeyboardButton('36')
th_seven_num = types.KeyboardButton('37')
th_eight_num = types.KeyboardButton('38')
th_nine_num = types.KeyboardButton('39')
th_ten_num = types.KeyboardButton('40')
f_one_num = types.KeyboardButton('41')
f_two_num = types.KeyboardButton('42')
f_three_num = types.KeyboardButton('43')
f_four_num = types.KeyboardButton('44')
f_five_num = types.KeyboardButton('45')
f_six_num = types.KeyboardButton('46')
f_seven_num = types.KeyboardButton('47')
f_eight_num = types.KeyboardButton('48')
f_nine_num = types.KeyboardButton('49')
f_ten_num = types.KeyboardButton('50')
fi_one_num = types.KeyboardButton('51')
fi_two_num = types.KeyboardButton('52')
fi_three_num = types.KeyboardButton('53')
fi_four_num = types.KeyboardButton('54')
fi_five_num = types.KeyboardButton('55')
fi_six_num = types.KeyboardButton('56')
fi_seven_num = types.KeyboardButton('57')
fi_eight_num = types.KeyboardButton('58')
fi_nine_num = types.KeyboardButton('59')
fi_ten_num = types.KeyboardButton('60')
s_one_num = types.KeyboardButton('61')
s_two_num = types.KeyboardButton('62')
s_three_num = types.KeyboardButton('63')
s_four_num = types.KeyboardButton('64')
s_five_num = types.KeyboardButton('65')
s_six_num = types.KeyboardButton('66')
s_seven_num = types.KeyboardButton('67')
s_eight_num = types.KeyboardButton('68')
s_nine_num = types.KeyboardButton('69')
s_ten_num = types.KeyboardButton('70')
se_one_num = types.KeyboardButton('71')
se_two_num = types.KeyboardButton('72')
se_three_num = types.KeyboardButton('73')
se_four_num = types.KeyboardButton('74')
se_five_num = types.KeyboardButton('75')
se_six_num = types.KeyboardButton('76')
se_seven_num = types.KeyboardButton('77')
se_eight_num = types.KeyboardButton('78')
se_nine_num = types.KeyboardButton('79')
se_ten_num = types.KeyboardButton('80')
e_one_num = types.KeyboardButton('81')
e_two_num = types.KeyboardButton('82')
e_three_num = types.KeyboardButton('83')
e_four_num = types.KeyboardButton('84')
e_five_num = types.KeyboardButton('85')
e_six_num = types.KeyboardButton('86')
e_seven_num = types.KeyboardButton('87')
e_eight_num = types.KeyboardButton('88')
e_nine_num = types.KeyboardButton('89')
e_ten_num = types.KeyboardButton('90')
n_one_num = types.KeyboardButton('91')
n_two_num = types.KeyboardButton('92')
n_three_num = types.KeyboardButton('93')
n_four_num = types.KeyboardButton('94')
n_five_num = types.KeyboardButton('95')
n_six_num = types.KeyboardButton('96')
n_seven_num = types.KeyboardButton('97')
n_eight_num = types.KeyboardButton('98')
n_nine_num = types.KeyboardButton('99')
n_ten_num = types.KeyboardButton('100')
n_ten_five_num = types.KeyboardButton('150')
two_hun_num = types.KeyboardButton('200')
two_hun_fiv_num = types.KeyboardButton('250')
five_hun_num = types.KeyboardButton('500')
se_hun_five = types.KeyboardButton('750')
th_num = types.KeyboardButton('1000')
cancel_num = types.KeyboardButton('/cancel')
markup_select_rand_num_hun.add(one_num, two_num, three_num, four_num, five_num, six_num, seven_num, eight_num, nine_num, ten_num,
                               t_one_num, t_two_num, t_three_num, t_four_num, t_five_num, t_six_num, t_seven_num, t_eight_num, t_nine_num, t_ten_num,
                               tw_one_num, tw_two_num, tw_three_num, tw_four_num, tw_five_num, tw_six_num, tw_seven_num, tw_eight_num, tw_nine_num, tw_ten_num,
                               th_one_num, th_two_num, th_three_num, th_four_num, th_five_num, th_six_num, th_seven_num, th_eight_num, th_nine_num, th_ten_num,
                               f_one_num, f_two_num, f_three_num, f_four_num, f_five_num, f_six_num, f_seven_num, f_eight_num, f_nine_num, f_ten_num,
                               fi_one_num, fi_two_num, fi_three_num, fi_four_num, fi_five_num, fi_six_num, fi_seven_num, fi_eight_num, fi_nine_num, fi_ten_num,
                               s_one_num, s_two_num, s_three_num, s_four_num, s_five_num, s_six_num, s_seven_num, s_eight_num, s_nine_num, s_ten_num,
                               se_one_num, se_two_num, se_three_num, se_four_num, se_five_num, se_six_num, se_seven_num, se_eight_num, se_nine_num, se_ten_num,
                               e_one_num, e_two_num, e_three_num, e_four_num, e_five_num, e_six_num, e_seven_num, e_eight_num, e_nine_num, e_ten_num,
                               n_one_num, n_two_num, n_three_num, n_four_num, n_five_num, n_six_num, n_seven_num, n_eight_num, n_nine_num, n_ten_num, cancel_num)
markup_select_rand_num_ten.add(one_num, two_num, three_num, four_num, five_num, six_num, seven_num, eight_num, nine_num, ten_num, cancel_num)
markup_select_rand_num_five.add(one_num, two_num, three_num, four_num, five_num, cancel_num)
markup_select_fifty_two.add(one_num, two_num, cancel_num)
markup_select_fifty_four.add(one_num, two_num, three_num, four_num, cancel_num)
markup_select_dice_classic.add(one_num, two_num, three_num, four_num, five_num, six_num, cancel_num)
markup_select_del_trx.add(n_ten_num, two_hun_num, two_hun_fiv_num, five_hun_num, se_hun_five, th_num, cancel_num)
markup_select_add_trx.add(n_ten_num, two_hun_num, two_hun_fiv_num, five_hun_num, se_hun_five, th_num, cancel_num)
markup_select_add_usdt.add(ten_num, t_five_num, tw_five_num, se_five_num, n_ten_num, two_hun_num, cancel_num)
markup_cancel.add(cancel_num)

async def markup_select_dice_under(message: types.Message):
    markup_select_dice_under = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    behind_seven = types.InlineKeyboardButton(locales.markup_select_dice_under[f'markup_select_dice_under_less_{BotDB.user_language(message.chat.id)}'])
    seven_und_bih = types.InlineKeyboardButton(locales.markup_select_dice_under[f'markup_select_dice_under_equal_{BotDB.user_language(message.chat.id)}'])
    under_seven = types.InlineKeyboardButton(locales.markup_select_dice_under[f'markup_select_dice_under_more_{BotDB.user_language(message.chat.id)}'])
    markup_select_dice_under.add(behind_seven, seven_und_bih, under_seven, cancel_num)
    return markup_select_dice_under

async def markup_cancel_promo(message: types.Message):
    markup_cancel_promo = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_promo = types.KeyboardButton(locales.markup_cancel_promo[f'markup_cancel_promo_{BotDB.user_language(message.chat.id)}'])
    markup_cancel_promo.add(cancel_promo)
    return markup_cancel_promo

async def markup_mail(message: types.Message):
    markup_captcha = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    captcha_true = types.KeyboardButton(f'633912')
    captcha_false_q = types.KeyboardButton(f'{random.randint(100000, 999999)}')
    captcha_false_w = types.KeyboardButton(f'{random.randint(100000, 999999)}')
    captcha_false_r = types.KeyboardButton(f'{random.randint(100000, 999999)}')
    captcha_false_t = types.KeyboardButton(f'{random.randint(100000, 999999)}')
    captcha_false_y = types.KeyboardButton(f'{random.randint(100000, 999999)}')
    captcha_false_a = types.KeyboardButton(f'{random.randint(100000, 999999)}')
    captcha_false_s = types.KeyboardButton(f'{random.randint(100000, 999999)}')
    captcha_false_d = types.KeyboardButton(f'{random.randint(100000, 999999)}')
    return_captcha = types.KeyboardButton(locales.markup_mail[f'markup_mail_{BotDB.user_language(message.chat.id)}'])
    markup_captcha.add(captcha_true, captcha_false_q, captcha_false_w, captcha_false_r, captcha_false_t, captcha_false_y, captcha_false_a, captcha_false_s, captcha_false_d).add(return_captcha)
    return markup_captcha

async def markup_phone(message: types.Message):
    markup_phone = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    phone_num = types.KeyboardButton(locales.markup_phone[f'markup_phone_{BotDB.user_language(message.chat.id)}'], request_contact=True)
    markup_phone.add(phone_num)
    return markup_phone


