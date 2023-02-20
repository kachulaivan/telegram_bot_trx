import asyncio
import random
import sqlite3
from typing import List

import locales
from handlers.states import say_hi, mailing, pay_operation
from asyncio import sleep

import db
from db import BotDB
from dispatcher import dp, bot, NOT_SUB_MESSAGE, CHANNELS, SUB_MESSAGE
from aiogram import types
import keyboards as kb
from handlers import states
from datetime import datetime
from datetime import timedelta
from aiogram.dispatcher import FSMContext


base = sqlite3.connect('bot_db.sqlite3')
cur = base.cursor()

async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer(locales.anti_flood['anti_flood_en'])

#######################################################################################################################################

async def check_sub_channels(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True

#######################################################################################################################################


@dp.callback_query_handler()
@dp.throttled(anti_flood, rate=0.5)
async def callback_guess(call: types.callback_query):
    for value_ban in cur.execute(f"SELECT ban FROM users WHERE user_id = {call.message.chat.id}"):
        if value_ban[0] != 1:
            if call.message:
                if call.data == 'sub_channel_done':
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    if await check_sub_channels(CHANNELS, call.message.chat.id):
                        await bot.send_message(call.message.chat.id, SUB_MESSAGE[f'NOT_SUB_MESSAGE_{BotDB.user_language(call.message.chat.id)}'])
                    else:
                        markup_channels = await kb.markup_channels(call.message)
                        await bot.send_message(call.message.chat.id, NOT_SUB_MESSAGE[f'NOT_SUB_MESSAGE_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_channels)

                if call.data == 'change_language':
                    await bot.send_message(call.message.chat.id, '🇺🇦 Оберіть мову інтерфейсу\n\n🇷🇺 Выберите язык интерфейса\n\n🇬🇧 Choose the interface language', reply_markup=kb.markup_change_language, parse_mode='html')
                if call.data == "ua_lang":
                    cur.execute(f"UPDATE users SET user_language = 'ua' WHERE user_id = {call.message.chat.id}")
                    base.commit()
                    markup_start = await kb.markup_start(call.message)
                    await bot.send_message(call.message.chat.id, '🇺🇦 Вітаю\n\nВи обрали українську мову\n\nМову можна міняти в будь-який момент у розділі "🆘 Тех. Підтримка"', reply_markup=markup_start, parse_mode='html')
                    await bot.send_message(call.message.chat.id, locales.reg_operation[f'main_menu_{BotDB.user_language(call.message.chat.id)}'], parse_mode='HTML')
                if call.data == "ru_lang":
                    cur.execute(f"UPDATE users SET user_language = 'ru' WHERE user_id = {call.message.chat.id}")
                    base.commit()
                    markup_start = await kb.markup_start(call.message)
                    await bot.send_message(call.message.chat.id, '🇷🇺 Поздравляю\n\nУ вас русский язык интерфейса\n\nЯзык можно менять в любой момент в разделе "🆘 Тех. Поддержка"', reply_markup=markup_start, parse_mode='html')
                    await bot.send_message(call.message.chat.id, locales.reg_operation[f'main_menu_{BotDB.user_language(call.message.chat.id)}'], parse_mode='HTML')
                if call.data == "en_lang":
                    cur.execute(f"UPDATE users SET user_language = 'en' WHERE user_id = {call.message.chat.id}")
                    base.commit()
                    markup_start = await kb.markup_start(call.message)
                    await bot.send_message(call.message.chat.id, '🇬🇧 Congratulations\n\n You have chosen English\n\n You can change the language at any time in the section "🆘 Support"', reply_markup=markup_start, parse_mode='html')
                    await bot.send_message(call.message.chat.id, locales.reg_operation[f'main_menu_{BotDB.user_language(call.message.chat.id)}'], parse_mode='HTML')

                if call.data == 'del_trx_cab':
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.pay_cab[f'del_trx_bal_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_del_trx, parse_mode='html')
                        await bot.send_message(call.message.chat.id, locales.pay_cab[f'del_trx_sum_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                        await pay_operation.del_trx.set()

                if call.data == 'add_trx_cab':
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.pay_cab[f'add_trx_bal_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_add_trx, parse_mode='html')
                        await bot.send_message(call.message.chat.id, locales.pay_cab[f'add_trx_sum_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                        await pay_operation.add_trx.set()

                if call.data == 'add_usd_cab':
                    for value in cur.execute(f"SELECT bal_dol FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.pay_cab[f'add_usd_bal_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_add_usdt, parse_mode='html')
                        await bot.send_message(call.message.chat.id, locales.pay_cab[f'add_usd_sum_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                        await pay_operation.add_usd.set()

                if call.data == 'say_hi_inline':
                    await call.message.answer(locales.say_hi_inline[f'say_hi_inline_{BotDB.user_language(call.message.chat.id)}'], reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
                    await say_hi.text.set()

                if call.data == 'what_is_lvl':
                    await bot.send_message(call.message.chat.id, locales.what_is_lvl[f'what_is_lvl_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')

                if call.data == 'check_lvl':
                    f = int(BotDB.count_ref(call.message.chat.id))
                    a = int(BotDB.count_ref(call.message.chat.id) + BotDB.count_sec_ref(call.message.chat.id) + BotDB.count_thi_ref(call.message.chat.id))
                    for value in cur.execute(f"SELECT user_level FROM users WHERE user_id = {call.message.chat.id}"):
                        for value_rules in cur.execute(f"SELECT game_fifty, game_case, game_slot, game_num, pay_trx, daily_bonus, week_bonus, game_num_win_hun FROM `achivement` WHERE `user_id` = {call.message.chat.id}"):
                            for value_lvl in cur.execute(f"SELECT user_level FROM `users` WHERE `user_id` = {call.message.chat.id}"):
                                try:
                                    if (value_lvl[0] == 1):
                                        fifty = locales.check_lvl[f'minus_fifty_{BotDB.user_language(call.message.chat.id)}']
                                        if value_rules[0] >= 50:
                                            fifty = locales.check_lvl[f'plus_fifty_{BotDB.user_language(call.message.chat.id)}']
                                        case = locales.check_lvl[f'minus_cases_{BotDB.user_language(call.message.chat.id)}']
                                        if value_rules[1] >= 150:
                                            case = locales.check_lvl[f'plus_cases_{BotDB.user_language(call.message.chat.id)}']
                                        f_ref = locales.check_lvl[f'minus_f_ref_{BotDB.user_language(call.message.chat.id)}']
                                        if BotDB.count_ref(call.message.chat.id) >= 7:
                                            f_ref = locales.check_lvl[f'plus_f_ref_{BotDB.user_language(call.message.chat.id)}']
                                        a_ref = locales.check_lvl[f'minus_a_ref_{BotDB.user_language(call.message.chat.id)}']
                                        if (BotDB.count_ref(call.message.chat.id) + BotDB.count_sec_ref(call.message.chat.id) + BotDB.count_thi_ref(call.message.chat.id)) >= 10:
                                            a_ref = locales.check_lvl[f'plus_a_ref_{BotDB.user_language(call.message.chat.id)}']
                                        await bot.send_message(call.message.chat.id, locales.check_lvl[f'first_lvl_{BotDB.user_language(call.message.chat.id)}'].format(fifty, value_rules[0], case, value_rules[1], f_ref, BotDB.count_ref(call.message.chat.id), a_ref, BotDB.count_ref(call.message.chat.id) + BotDB.count_sec_ref(call.message.chat.id) + BotDB.count_thi_ref(call.message.chat.id)), parse_mode='html')
                                    if (f >= 7 and a >= 10 and value_rules[0] >= 50 and value_rules[1] >= 150) and value_lvl[0] == 1:
                                        if value_lvl[0] != 2:
                                            await bot.send_message(call.message.chat.id, locales.check_lvl[f'congr_sec_lvl_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                            await db.give_level_2(call.message.chat.id)
                                        else:
                                            pass
                                    if value_lvl[0] == 2:
                                        spin = locales.check_lvl[f'minus_spin_{BotDB.user_language(call.message.chat.id)}']
                                        if value_rules[2] >= 185:
                                            spin = locales.check_lvl[f'plus_spin_{BotDB.user_language(call.message.chat.id)}']
                                        num = locales.check_lvl[f'minus_num_{BotDB.user_language(call.message.chat.id)}']
                                        if value_rules[3] >= 225:
                                            num = locales.check_lvl[f'plus_num_{BotDB.user_language(call.message.chat.id)}']
                                        num_hun = locales.check_lvl[f'minus_num_hun_{BotDB.user_language(call.message.chat.id)}']
                                        if value_rules[7] >= 2:
                                            num_hun = locales.check_lvl[f'plus_num_hun_{BotDB.user_language(call.message.chat.id)}']
                                        f_ref = locales.check_lvl[f'minus_f_ref_second_{BotDB.user_language(call.message.chat.id)}']
                                        if BotDB.count_ref(call.message.chat.id) >= 22:
                                            f_ref = locales.check_lvl[f'plus_f_ref_second_{BotDB.user_language(call.message.chat.id)}']
                                        a_ref = locales.check_lvl[f'minus_a_ref_second_{BotDB.user_language(call.message.chat.id)}']
                                        if (BotDB.count_ref(call.message.chat.id) + BotDB.count_sec_ref(call.message.chat.id) + BotDB.count_thi_ref(call.message.chat.id)) >= 30:
                                            a_ref = locales.check_lvl[f'plus_a_ref_second_{BotDB.user_language(call.message.chat.id)}']
                                        pay_trx_to_lvl = locales.check_lvl[f'minus_pay_trx_to_lvl_{BotDB.user_language(call.message.chat.id)}']
                                        if value_rules[4] >= 500 or value_rules[5] >= 150 and value_rules[6] >= 6:
                                            pay_trx_to_lvl = locales.check_lvl[f'plus_pay_trx_to_lvl_{BotDB.user_language(call.message.chat.id)}']
                                        await bot.send_message(call.message.chat.id, locales.check_lvl[f'second_lvl_{BotDB.user_language(call.message.chat.id)}'].format(spin, value_rules[2], num, value_rules[3], num_hun, value_rules[7], f_ref, BotDB.count_ref(call.message.chat.id), a_ref, BotDB.count_ref(call.message.chat.id) + BotDB.count_sec_ref(call.message.chat.id) + BotDB.count_thi_ref(call.message.chat.id), pay_trx_to_lvl, value_rules[4], value_rules[5], value_rules[6]), parse_mode='html')
                                    if (f >= 22 and a >= 30 and value_rules[2] >= 185 and value_rules[3] >= 225 and value_rules[7] >= 2 and value_lvl[0] == 2):
                                        if value_rules[4] >= 500 or value_rules[5] >= 150 and value_rules[6] >= 6:
                                            if value_lvl[0] != 3:
                                                await bot.send_message(call.message.chat.id, locales.check_lvl[f'congr_thi_lvl_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                                await db.give_level_3(call.message.chat.id)
                                            else:
                                                pass
                                    if value[0] == 3:
                                        await bot.send_message(call.message.chat.id, locales.check_lvl[f'max_lvl_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                except:
                                    await bot.send_message(call.message.chat.id, locales.check_lvl[f'error_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')

                if call.data == 'again_guess_five':
                    await states.guess_number.bet_five.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_guess_five_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'again_dice_classic':
                    await states.dice.bet_classic.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_dice_classic_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'again_dice_under':
                    await states.dice.bet_under.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_dice_under_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'again_guess_ten':
                    await states.guess_number.bet_ten.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_guess_ten_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'again_guess_hun':
                    await states.guess_number.bet_hun.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_guess_hun_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'again_fifty_two':
                    await states.fifty_fifty.bet_two.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_fifty_two_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'again_fifty_four':
                    await states.fifty_fifty.bet_four.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_fifty_four_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'again_fifty_ten':
                    await states.fifty_fifty.bet_ten.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_fifty_ten_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'again_br_case':
                    await states.cases.case_br_buy.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        markup_accept_cases = await kb.markup_accept_cases(call.message)
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_br_case_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=markup_accept_cases, parse_mode='html')

                if call.data == 'again_si_case':
                    await states.cases.case_si_buy.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        markup_accept_cases = await kb.markup_accept_cases(call.message)
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_si_case_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=markup_accept_cases, parse_mode='html')

                if call.data == 'again_go_case':
                    await states.cases.case_go_buy.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        markup_accept_cases = await kb.markup_accept_cases(call.message)
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_go_case_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=markup_accept_cases, parse_mode='html')

                if call.data == 'again_miner_three':
                    await states.miner.bet_three.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_miner_three_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'again_miner_five':
                    await states.miner.bet_five.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_miner_five_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'again_miner_seven':
                    await states.miner.bet_seven.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_miner_seven_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'again_slot':
                    await states.spin.bet_spin.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.again_game[f'again_slot_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                if call.data == 'accept_cab':
                    await call.answer(locales.accept_cab[f'accept_cab_{BotDB.user_language(call.message.chat.id)}'])

                if call.data == 'history_pay_cab':
                    within_als = {
                        "day": ('today', 'day', 'СЬОГОДНІ', locales.history_pay[f'history_pay_day_{BotDB.user_language(call.message.chat.id)}']),
                        "month": ('month', locales.history_pay[f'history_pay_month_{BotDB.user_language(call.message.chat.id)}']),
                        "year": ('year', locales.history_pay[f'history_pay_year_{BotDB.user_language(call.message.chat.id)}']),
                    }
                    within = 'month'
                    cur.execute(f"DELETE FROM paymants WHERE adress = '/cancel'")
                    base.commit()
                    records = BotDB.get_records(call.message.chat.id, within)
                    if (len(records)):
                        answer = ( locales.history_pay[f'history_pay_text_{BotDB.user_language(call.message.chat.id)}'].format(within_als[within][-1]))
                        for r in records:
                            answer += ("<b>" + ("➕ " if not r[4] else "➖ ") + "</b>")
                            if r[2] != 0:
                                answer += f"<b><u><i>{r[2]} USDT</i></u></b>"
                            if r[3] != 0:
                                answer += f"<b><u><i>{r[3]} TRX</i></u></b>"
                            if r[4] != 0:
                                answer += f"<b><u><i>{r[4]} TRX</i></u></b>"
                            answer += f"\n🕐 {r[5]}  "
                            answer += ("<b>" + ( locales.history_pay[f'history_pay_add_{BotDB.user_language(call.message.chat.id)}'] if not r[4] else  locales.history_pay[f'history_pay_del_{BotDB.user_language(call.message.chat.id)}']) + "</b>\n")
                            if r[7] == 0:
                                answer +=  locales.history_pay[f'history_pay_not_{BotDB.user_language(call.message.chat.id)}']
                            elif r[7] == 1:
                                answer += locales.history_pay[f'history_pay_acc_{BotDB.user_language(call.message.chat.id)}']
                            else:
                                answer += locales.history_pay[f'history_pay_err_{BotDB.user_language(call.message.chat.id)}']
                        markup_pay_history = await kb.markup_pay_history(call.message)
                        await call.message.answer(answer, parse_mode='html', reply_markup=markup_pay_history)
                    else:
                        markup_pay_history = await kb.markup_pay_history(call.message)
                        await call.message.answer(locales.history_pay[f'history_pay_emp_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_pay_history)

                if call.data == 'pay_history_day_cab':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', locales.history_pay[f'history_pay_day_{BotDB.user_language(call.message.chat.id)}']),
                            "month": ('month', locales.history_pay[f'history_pay_month_{BotDB.user_language(call.message.chat.id)}']),
                            "year": ('year', locales.history_pay[f'history_pay_year_{BotDB.user_language(call.message.chat.id)}']),
                        }
                        within = 'day'
                        records = BotDB.get_records(call.message.chat.id, within)
                        if (len(records)):
                            answer = (
                                locales.history_pay[f'history_pay_text_{BotDB.user_language(call.message.chat.id)}'].format(
                                    within_als[within][-1]))
                            for r in records:
                                answer += ("<b>" + ("➕ " if not r[4] else "➖ ") + "</b>")
                                if r[2] != 0:
                                    answer += f"<b><u><i>{r[2]} USDT</i></u></b>"
                                if r[3] != 0:
                                    answer += f"<b><u><i>{r[3]} TRX</i></u></b>"
                                if r[4] != 0:
                                    answer += f"<b><u><i>{r[4]} TRX</i></u></b>"
                                answer += f"\n🕐 {r[5]}  "
                                answer += ("<b>" + (
                                    locales.history_pay[f'history_pay_add_{BotDB.user_language(call.message.chat.id)}'] if not
                                    r[4] else locales.history_pay[f'history_pay_del_{BotDB.user_language(call.message.chat.id)}']) + "</b>\n")
                                if r[7] == 0:
                                    answer += locales.history_pay[f'history_pay_not_{BotDB.user_language(call.message.chat.id)}']
                                elif r[7] == 1:
                                    answer += locales.history_pay[f'history_pay_acc_{BotDB.user_language(call.message.chat.id)}']
                                else:
                                    answer += locales.history_pay[f'history_pay_err_{BotDB.user_language(call.message.chat.id)}']
                            markup_pay_history = await kb.markup_pay_history(call.message)
                            await call.message.edit_text(answer, parse_mode='html', reply_markup=markup_pay_history)
                        else:
                            markup_pay_history = await kb.markup_pay_history(call.message)
                            await call.message.answer(locales.history_pay[f'history_pay_emp_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_pay_history)
                    except:
                        pass

                if call.data == 'pay_history_month_cab':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', locales.history_pay[f'history_pay_day_{BotDB.user_language(call.message.chat.id)}']),
                            "month": ('month', locales.history_pay[f'history_pay_month_{BotDB.user_language(call.message.chat.id)}']),
                            "year": ('year', locales.history_pay[f'history_pay_year_{BotDB.user_language(call.message.chat.id)}']),
                        }
                        within = 'month'
                        records = BotDB.get_records(call.message.chat.id, within)
                        if (len(records)):
                            answer = (
                                locales.history_pay[f'history_pay_text_{BotDB.user_language(call.message.chat.id)}'].format(
                                    within_als[within][-1]))
                            for r in records:
                                answer += ("<b>" + ("➕ " if not r[4] else "➖ ") + "</b>")
                                if r[2] != 0:
                                    answer += f"<b><u><i>{r[2]} USDT</i></u></b>"
                                if r[3] != 0:
                                    answer += f"<b><u><i>{r[3]} TRX</i></u></b>"
                                if r[4] != 0:
                                    answer += f"<b><u><i>{r[4]} TRX</i></u></b>"
                                answer += f"\n🕐 {r[5]}  "
                                answer += ("<b>" + (
                                    locales.history_pay[f'history_pay_add_{BotDB.user_language(call.message.chat.id)}'] if not
                                    r[4] else locales.history_pay[
                                        f'history_pay_del_{BotDB.user_language(call.message.chat.id)}']) + "</b>\n")
                                if r[7] == 0:
                                    answer += locales.history_pay[f'history_pay_not_{BotDB.user_language(call.message.chat.id)}']
                                elif r[7] == 1:
                                    answer += locales.history_pay[f'history_pay_acc_{BotDB.user_language(call.message.chat.id)}']
                                else:
                                    answer += locales.history_pay[f'history_pay_err_{BotDB.user_language(call.message.chat.id)}']
                            markup_pay_history = await kb.markup_pay_history(call.message)
                            await call.message.edit_text(answer, parse_mode='html', reply_markup=markup_pay_history)
                        else:
                            markup_pay_history = await kb.markup_pay_history(call.message)
                            await call.message.answer(locales.history_pay[f'history_pay_emp_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_pay_history)
                    except:
                        pass

                if call.data == 'pay_history_year_cab':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', locales.history_pay[f'history_pay_day_{BotDB.user_language(call.message.chat.id)}']),
                            "month": ('month', locales.history_pay[f'history_pay_month_{BotDB.user_language(call.message.chat.id)}']),
                            "year": ('year', locales.history_pay[f'history_pay_year_{BotDB.user_language(call.message.chat.id)}']),
                        }
                        within = 'year'
                        records = BotDB.get_records(call.message.chat.id, within)
                        if (len(records)):
                            answer = (
                                locales.history_pay[f'history_pay_text_{BotDB.user_language(call.message.chat.id)}'].format(
                                    within_als[within][-1]))
                            for r in records:
                                answer += ("<b>" + ("➕ " if not r[4] else "➖ ") + "</b>")
                                if r[2] != 0:
                                    answer += f"<b><u><i>{r[2]} USDT</i></u></b>"
                                if r[3] != 0:
                                    answer += f"<b><u><i>{r[3]} TRX</i></u></b>"
                                if r[4] != 0:
                                    answer += f"<b><u><i>{r[4]} TRX</i></u></b>"
                                answer += f"\n🕐 {r[5]}  "
                                answer += ("<b>" + (
                                    locales.history_pay[f'history_pay_add_{BotDB.user_language(call.message.chat.id)}'] if not
                                    r[4] else locales.history_pay[f'history_pay_del_{BotDB.user_language(call.message.chat.id)}']) + "</b>\n")
                                if r[7] == 0:
                                    answer += locales.history_pay[f'history_pay_not_{BotDB.user_language(call.message.chat.id)}']
                                elif r[7] == 1:
                                    answer += locales.history_pay[f'history_pay_acc_{BotDB.user_language(call.message.chat.id)}']
                                else:
                                    answer += locales.history_pay[f'history_pay_err_{BotDB.user_language(call.message.chat.id)}']
                            markup_pay_history = await kb.markup_pay_history(call.message)
                            await call.message.edit_text(answer, parse_mode='html', reply_markup=markup_pay_history)
                        else:
                            markup_pay_history = await kb.markup_pay_history(call.message)
                            await call.message.answer(locales.history_pay[f'history_pay_emp_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_pay_history)
                    except:
                        pass

                if call.data == 'day_bon_cab':
                    if (not BotDB.daily_bonus_exists(call.message.chat.id)):
                        BotDB.get_bonus_daily(call.message.chat.id)
                        await call.answer(locales.day_bon[f'day_bon_first_lvl_answer_{BotDB.user_language(call.message.chat.id)}'])
                        await bot.send_message(call.message.chat.id, locales.day_bon[f'day_bon_first_lvl_message_{BotDB.user_language(call.message.chat.id)}'])
                        await db.give_bonus_daily(call.message.chat.id)
                    access = False
                    curr_datetime = datetime.now()
                    for value in cur.execute(f"SELECT `date` FROM `daily_bonus` WHERE `user_id` = {call.message.chat.id}"):
                        date_time_daily_bonus = datetime.strptime(value[0], '%Y-%m-%d %H:%M:%S')
                        if (curr_datetime - date_time_daily_bonus).total_seconds() > 86400:  # 86400 секунд = 24 часа
                            access = True
                            photo = open('img/bonus_img.jpg', 'rb')
                            for value_lvl in cur.execute(f"SELECT `user_level` FROM `users` WHERE `user_id` = {call.message.chat.id}"):
                                if (value_lvl[0] == 1):
                                    await call.answer(locales.day_bon[f'day_bon_first_lvl_answer_{BotDB.user_language(call.message.chat.id)}'])
                                    await bot.send_photo(call.message.chat.id, photo, caption=locales.day_bon[f'day_bon_first_lvl_message_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                    await db.give_bonus_daily(call.message.chat.id)
                                    await db.update_bonus_daily(call.message.chat.id)
                                elif (value_lvl[0] == 2):
                                    await call.answer(locales.day_bon[f'day_bon_second_lvl_answer_{BotDB.user_language(call.message.chat.id)}'])
                                    await bot.send_photo(call.message.chat.id, photo, caption=locales.day_bon[f'day_bon_second_lvl_message_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                    await db.give_bonus_daily_lvl_2(call.message.chat.id)
                                    await db.update_bonus_daily(call.message.chat.id)
                                else:
                                    await call.answer(locales.day_bon[f'day_bon_third_lvl_answer_{BotDB.user_language(call.message.chat.id)}'])
                                    await bot.send_photo(call.message.chat.id, photo, caption=locales.day_bon[f'day_bon_third_lvl_message_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                    await db.give_bonus_daily_lvl_3(call.message.chat.id)
                                    await db.update_bonus_daily(call.message.chat.id)
                        else:
                            left_time = timedelta(hours=25, minutes=59, seconds=59) - (curr_datetime - date_time_daily_bonus)
                            photo = open('img/bonus_img.jpg', 'rb')
                            await call.answer(locales.day_bon[f'next_day_bon_answer_{BotDB.user_language(call.message.chat.id)}'].format(str(left_time)[:8]))
                            await bot.send_photo(call.message.chat.id, photo, caption=locales.day_bon[f'next_day_bon_message_{BotDB.user_language(call.message.chat.id)}'].format(str(left_time)[:8]), parse_mode='html')
                    return access

                if call.data == 'wek_bon_cab':
                    if await check_sub_channels(CHANNELS, call.message.chat.id):
                        if (not BotDB.week_bonus_exists(call.message.chat.id)):
                            BotDB.get_bonus_week(call.message.chat.id)
                            await call.answer(locales.week_bon[f'week_bon_first_lvl_answer_{BotDB.user_language(call.message.chat.id)}'])
                            await bot.send_message(call.message.chat.id, locales.week_bon[f'week_bon_first_lvl_message_{BotDB.user_language(call.message.chat.id)}'])
                            await db.give_bonus_week(call.message.chat.id)
                        access = False
                        curr_datetime = datetime.now()
                        for value in cur.execute(f"SELECT `date` FROM `week_bonus` WHERE `user_id` = {call.message.chat.id}"):
                            date_time_week_bonus = datetime.strptime(value[0], '%Y-%m-%d %H:%M:%S')
                            if (curr_datetime - date_time_week_bonus).total_seconds() > 604800:  # 86400 секунд = 24 часа
                                access = True
                                photo = open('img/bonus_img.jpg', 'rb')
                                for value_lvl in cur.execute(f"SELECT `user_level` FROM `users` WHERE `user_id` = {call.message.chat.id}"):
                                    if (value_lvl[0] == 3):
                                        await call.answer(locales.week_bon[f'week_bon_second_lvl_answer_{BotDB.user_language(call.message.chat.id)}'])
                                        await bot.send_photo(call.message.chat.id, photo, caption=locales.week_bon[f'week_bon_second_lvl_message_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                        await db.give_bonus_week_lvl_3(call.message.chat.id)
                                        await db.update_bonus_week(call.message.chat.id)
                                    else:
                                        await call.answer(locales.week_bon[f'week_bon_first_lvl_answer_{BotDB.user_language(call.message.chat.id)}'])
                                        await bot.send_photo(call.message.chat.id, photo, caption=locales.week_bon[f'week_bon_first_lvl_message_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                        await db.give_bonus_week(call.message.chat.id)
                                        await db.update_bonus_week(call.message.chat.id)
                            else:
                                left_time = timedelta(days=6, hours=25, minutes=59, seconds=59) - (curr_datetime - date_time_week_bonus)
                                photo = open('img/bonus_img.jpg', 'rb')
                                await call.answer(locales.week_bon[f'next_week_bon_answer_{BotDB.user_language(call.message.chat.id)}'].format(str(left_time)[:16]))
                                await bot.send_photo(call.message.chat.id, photo, caption=locales.week_bon[f'next_week_bon_message_{BotDB.user_language(call.message.chat.id)}'].format(str(left_time)[:16]), parse_mode='html')
                                return access
                    else:
                        markup_channels = await kb.markup_channels(call.message)
                        await bot.send_message(call.message.chat.id, NOT_SUB_MESSAGE[f'NOT_SUB_MESSAGE_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_channels)

                if call.data == 'five_num_guess_game':
                    await states.guess_number.bet_five.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_intro_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')
                    @dp.message_handler(state=states.guess_number.bet_five)
                    async def random_number_five(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['bet_five'] = float(message.text)
                            betting = data['bet_five']
                            if betting <= 1000:
                                if betting > 0:
                                    user_id_mod = message.from_user.id
                                    for value_bet_five in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = ?", (user_id_mod,)):
                                        if betting <= value_bet_five[0]:
                                            await states.guess_number.next()
                                            await bot.send_message(message.chat.id, locales.num_guess_game[f'num_guess_five_game_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_rand_num_five)
                                        else:
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                else:
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_min_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_max_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()
                    @dp.message_handler(state=states.guess_number.random_number_five)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.guess_number.random_number_five.set()
                            data['random_number_five'] = random.randint(1, 5)
                        try:
                            betting = data['bet_five']
                            cur.execute(f"UPDATE achivement SET game_num = game_num + 1 WHERE user_id = {call.message.chat.id}")
                            base.commit()
                            if int(message.text) >= 1 and int(message.text) <= 5:
                                if int(message.text) == data['random_number_five']:
                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 3.95 WHERE user_id = {message.chat.id}")
                                    base.commit()
                                    anim_num = random.sample(range(1, 5), 3)
                                    for rand_anim in anim_num:
                                        await asyncio.sleep(0.5)
                                        await message.answer(locales.for_all_games[f'for_all_games_rand_num_{BotDB.user_language(message.chat.id)}']+'<b>'+str(rand_anim)+'</b> ❓', parse_mode='html')
                                    for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_win_game_{BotDB.user_language(message.chat.id)}'].format(betting * 4.5), reply_markup=markup_games)
                                        markup_again_guess_five = await kb.markup_again_guess_five(message)
                                        await message.answer(locales.num_guess_game[f'num_guess_result_{BotDB.user_language(message.chat.id)}'].format(values[0], data['random_number_five']), reply_markup=markup_again_guess_five, parse_mode='html')
                                        await state.finish()
                                else:
                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} WHERE user_id = {message.chat.id}")
                                    base.commit()
                                    anim_num = random.sample(range(1, 5), 3)
                                    for rand_anim in anim_num:
                                        await asyncio.sleep(0.5)
                                        await message.answer(locales.for_all_games[f'for_all_games_rand_num_{BotDB.user_language(message.chat.id)}']+'<b>'+str(rand_anim)+'</b> ❓', parse_mode='html')
                                    for valuess in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_lose_game_{BotDB.user_language(message.chat.id)}'].format(betting), parse_mode='html', reply_markup=markup_games)
                                        markup_again_guess_five = await kb.markup_again_guess_five(message)
                                        await message.answer(locales.num_guess_game[f'num_guess_result_{BotDB.user_language(message.chat.id)}'].format(valuess[0], data['random_number_five']), reply_markup=markup_again_guess_five, parse_mode='html')
                                        await state.finish()
                            else:
                                await bot.send_message(message.chat.id, locales.num_guess_game[f'num_guess_game_five_range_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await message.answer(locales.num_guess_game[f'num_guess_game_five_error_range_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_rand_num_five, parse_mode='html')

                if call.data == 'ten_num_guess_game':
                    await states.guess_number.bet_ten.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_intro_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                    @dp.message_handler(state=states.guess_number.bet_ten)
                    async def random_number_ten(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['bet_ten'] = float(message.text)
                            betting = data['bet_ten']
                            if betting <= 1000:
                                if betting > 0:
                                    user_id_mod = message.from_user.id
                                    for value_bet_ten in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = ?", (user_id_mod,)):
                                        if betting <= value_bet_ten[0]:
                                            await states.guess_number.next()
                                            await bot.send_message(message.chat.id, locales.num_guess_game[f'num_guess_ten_game_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_rand_num_ten)
                                        else:
                                            await bot.send_message(message.chat.id,  locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                else:
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_min_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_max_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()

                    @dp.message_handler(state=states.guess_number.random_number_ten)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.guess_number.random_number_ten.set()
                            data['random_number_ten'] = random.randint(1, 10)
                        try:
                            betting = data['bet_ten']
                            cur.execute(f"UPDATE achivement SET game_num = game_num + 1 WHERE user_id = {call.message.chat.id}")
                            base.commit()
                            if int(message.text) >= 1 and int(message.text) <= 10:
                                if int(message.text) == data['random_number_ten']:
                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 8.9 WHERE user_id = {message.chat.id}")
                                    base.commit()
                                    anim_num = random.sample(range(1, 10), 3)
                                    for rand_anim in anim_num:
                                        await asyncio.sleep(0.5)
                                        await message.answer(locales.for_all_games[f'for_all_games_rand_num_{BotDB.user_language(message.chat.id)}']+'<b>'+str(rand_anim)+'</b> ❓', parse_mode='html')
                                    for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_win_game_{BotDB.user_language(message.chat.id)}'].format(betting * 9.9), reply_markup=markup_games)
                                        markup_again_guess_ten = await kb.markup_again_guess_ten(message)
                                        await message.answer(locales.num_guess_game[f'num_guess_result_{BotDB.user_language(message.chat.id)}'].format(values[0], data['random_number_ten']), reply_markup=markup_again_guess_ten, parse_mode='html')
                                        await state.finish()
                                else:
                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} WHERE user_id = {message.chat.id}")
                                    base.commit()
                                    anim_num = random.sample(range(1, 10), 3)
                                    for rand_anim in anim_num:
                                        await asyncio.sleep(0.5)
                                        await message.answer(locales.for_all_games[f'for_all_games_rand_num_{BotDB.user_language(message.chat.id)}']+'<b>'+str(rand_anim)+'</b> ❓', parse_mode='html')
                                    for valuess in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_lose_game_{BotDB.user_language(message.chat.id)}'].format(betting), parse_mode='html', reply_markup=markup_games)
                                        markup_again_guess_ten = await kb.markup_again_guess_ten(message)
                                        await message.answer(locales.num_guess_game[f'num_guess_result_{BotDB.user_language(message.chat.id)}'].format(valuess[0], data['random_number_ten']), reply_markup=markup_again_guess_ten, parse_mode='html')
                                        await state.finish()
                            else:
                                await bot.send_message(message.chat.id, locales.num_guess_game[f'num_guess_game_ten_range_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await message.answer(locales.num_guess_game[f'num_guess_game_ten_error_range_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_rand_num_ten, parse_mode='html')

                if call.data == 'hun_num_guess_game':
                    await states.guess_number.bet_hun.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_intro_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                    @dp.message_handler(state=states.guess_number.bet_hun)
                    async def random_number_hun(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['bet_hun'] = float(message.text)
                            betting = data['bet_hun']
                            if betting <= 1000:
                                if betting > 0:
                                    user_id_mod = message.from_user.id
                                    for value_bet_hun in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = ?", (user_id_mod,)):
                                        if betting <= value_bet_hun[0]:
                                            await states.guess_number.next()
                                            await bot.send_message(message.chat.id, locales.num_guess_game[f'num_guess_hun_game_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_rand_num_hun)
                                        else:
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                else:
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_min_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_max_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()

                    @dp.message_handler(state=states.guess_number.random_number_hun)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.guess_number.random_number_hun.set()
                            data['random_number_hun'] = random.randint(1, 100)
                        try:
                            betting = data['bet_hun']
                            cur.execute(f"UPDATE achivement SET game_num = game_num + 1 WHERE user_id = {call.message.chat.id}")
                            base.commit()
                            if int(message.text) >= 1 and int(message.text) <= 100:
                                if int(message.text) == data['random_number_hun']:
                                    cur.execute(f"UPDATE achivement SET game_num_win_hun = game_num_win_hun + 1 WHERE user_id = {call.message.chat.id}")
                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 94 WHERE user_id = {message.chat.id}")
                                    base.commit()
                                    anim_num = random.sample(range(1, 100), 3)
                                    for rand_anim in anim_num:
                                        await asyncio.sleep(0.5)
                                        await message.answer(locales.for_all_games[f'for_all_games_rand_num_{BotDB.user_language(message.chat.id)}']+'<b>'+str(rand_anim)+'</b> ❓', parse_mode='html')
                                    for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_win_game_{BotDB.user_language(message.chat.id)}'].format(betting * 95), reply_markup=markup_games)
                                        markup_again_guess_hun = await kb.markup_again_guess_hun(message)
                                        await message.answer(locales.num_guess_game[f'num_guess_result_{BotDB.user_language(message.chat.id)}'].format(values[0], data['random_number_hun']), reply_markup=markup_again_guess_hun, parse_mode='html')
                                        await state.finish()
                                else:
                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} WHERE user_id = {message.chat.id}")
                                    base.commit()
                                    anim_num = random.sample(range(1, 100), 3)
                                    for rand_anim in anim_num:
                                        await asyncio.sleep(0.5)
                                        await message.answer(locales.for_all_games[f'for_all_games_rand_num_{BotDB.user_language(message.chat.id)}']+'<b>'+str(rand_anim)+'</b> ❓', parse_mode='html')
                                    for valuess in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_lose_game_{BotDB.user_language(message.chat.id)}'].format(betting), parse_mode='html', reply_markup=markup_games)
                                        markup_again_guess_hun = await kb.markup_again_guess_hun(message)
                                        await message.answer(locales.num_guess_game[f'num_guess_result_{BotDB.user_language(message.chat.id)}'].format(valuess[0], data['random_number_hun']), reply_markup=markup_again_guess_hun, parse_mode='html')
                                        await state.finish()
                            else:
                                await bot.send_message(message.chat.id, locales.num_guess_game[f'num_guess_game_hun_range_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await message.answer(locales.num_guess_game[f'num_guess_game_hun_error_range_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_rand_num_hun, parse_mode='html')

                if call.data == 'two_num_fifty_game':
                    await states.fifty_fifty.bet_two.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_intro_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')
                    @dp.message_handler(state=states.fifty_fifty.bet_two)
                    async def random_number_two(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['bet_two'] = float(message.text)
                            betting = data['bet_two']
                            if betting <= 1000:
                                if betting > 0:
                                    user_id_mod = message.from_user.id
                                    for value_bet_two in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = ?", (user_id_mod,)):
                                        if betting <= value_bet_two[0]:
                                            await states.fifty_fifty.next()
                                            await bot.send_message(message.chat.id, locales.fifty_game[f'fifty_two_game_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_fifty_two)
                                        else:
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                else:
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_min_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_max_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()

                    @dp.message_handler(state=states.fifty_fifty.random_number_two)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.fifty_fifty.random_number_two.set()
                            data['random_number_two'] = random.randint(1, 2)
                        try:
                            betting = data['bet_two']
                            if int(message.text) >= 1 and int(message.text) <= 2:
                                anim_num_f = random.randint(1, 2)
                                anim_num_s = random.randint(1, 2)
                                anim_num_t = random.randint(1, 2)
                                await asyncio.sleep(0.5)
                                await message.answer(locales.for_all_games[f'for_all_games_rand_num_{BotDB.user_language(message.from_user.id)}'] + '<b>' + str(anim_num_f) + '</b> ❓', parse_mode='html')
                                await asyncio.sleep(0.5)
                                await message.answer(locales.for_all_games[f'for_all_games_rand_num_{BotDB.user_language(message.from_user.id)}'] + '<b>' + str(anim_num_s) + '</b> ❓', parse_mode='html')
                                await asyncio.sleep(0.5)
                                await message.answer(locales.for_all_games[f'for_all_games_rand_num_{BotDB.user_language(message.from_user.id)}'] + '<b>' + str(anim_num_t) + '</b> ❓', parse_mode='html')
                                if int(message.text) == data['random_number_two']:
                                    cur.execute(f"UPDATE achivement SET game_fifty = game_fifty + 1 WHERE user_id = {message.chat.id}")
                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 0.95 WHERE user_id = {message.chat.id}")
                                    base.commit()
                                    for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_win_game_{BotDB.user_language(message.chat.id)}'].format(betting * 1.95), reply_markup=markup_games)
                                        markup_again_fifty_two = await kb.markup_again_fifty_two(message)
                                        await message.answer(locales.fifty_game[f'fifty_two_result_{BotDB.user_language(message.chat.id)}'].format(values[0], data['random_number_two']), reply_markup=markup_again_fifty_two, parse_mode='html')
                                        await state.finish()
                                else:
                                    cur.execute(f"UPDATE achivement SET game_fifty = game_fifty + 1 WHERE user_id = {message.chat.id}")
                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} WHERE user_id = {message.chat.id}")
                                    base.commit()
                                    for valuess in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_lose_game_{BotDB.user_language(message.chat.id)}'].format(betting), parse_mode='html', reply_markup=markup_games)
                                        markup_again_fifty_two = await kb.markup_again_fifty_two(message)
                                        await message.answer(locales.fifty_game[f'fifty_two_result_{BotDB.user_language(message.chat.id)}'].format(valuess[0], data['random_number_two']), reply_markup=markup_again_fifty_two, parse_mode='html')
                                        await state.finish()
                            else:
                                await bot.send_message(message.chat.id, locales.fifty_game[f'fifty_two_range_game_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await message.answer(locales.fifty_game[f'fifty_two_error_range_game_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_fifty_two, parse_mode='html')

                if call.data == 'four_num_fifty_game':
                    await states.fifty_fifty.bet_four.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_intro_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')
                    @dp.message_handler(state=states.fifty_fifty.bet_four)
                    async def random_number_four(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['bet_four'] = float(message.text)
                            betting = data['bet_four']
                            if betting <= 1000:
                                if betting > 0:
                                    user_id_mod = message.from_user.id
                                    for value_bet_four in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = ?", (user_id_mod,)):
                                        if betting <= value_bet_four[0]:
                                            await states.fifty_fifty.next()
                                            await bot.send_message(message.chat.id, locales.fifty_game[f'fifty_four_game_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_fifty_four)
                                        else:
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                else:
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_min_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_max_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()

                    @dp.message_handler(state=states.fifty_fifty.random_number_four)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.fifty_fifty.random_number_four.set()
                            data['random_number_four_first'] = random.randint(1, 4)
                            data['random_number_four_second'] = random.randint(1, 4)
                            if data['random_number_four_first'] == data['random_number_four_second']:
                                data['random_number_four_second'] = random.randint(1, 4)
                            if data['random_number_four_first'] == data['random_number_four_second']:
                                data['random_number_four_second'] = random.randint(1, 4)
                            if data['random_number_four_first'] == data['random_number_four_second']:
                                data['random_number_four_second'] = random.randint(1, 4)
                            try:
                                betting = data['bet_four']
                                if int(message.text) >= 1 and int(message.text) <= 4:
                                    anim_num = random.sample(range(1, 5), 3)
                                    for rand_anim in anim_num:
                                        await asyncio.sleep(0.5)
                                        await message.answer(locales.for_all_games[f'for_all_games_rand_num_{BotDB.user_language(message.chat.id)}'] + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
                                    if int(message.text) == data['random_number_four_first'] or int(message.text) == data['random_number_four_second']:
                                        if int(message.text) == data['random_number_four_first'] and int(message.text) == data['random_number_four_second']:
                                            cur.execute(f"UPDATE achivement SET game_fifty = game_fifty + 1 WHERE user_id = {message.chat.id}")
                                            cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 2.9 WHERE user_id = {message.chat.id}")
                                            base.commit()
                                            markup_games = await kb.markup_games(message)
                                            await message.answer(locales.fifty_game[f'fifty_four_twice_win_game_{BotDB.user_language(message.chat.id)}'].format(betting * 3.9), reply_markup=markup_games)
                                        else:
                                            cur.execute(f"UPDATE achivement SET game_fifty = game_fifty + 1 WHERE user_id = {message.chat.id}")
                                            cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 0.95 WHERE user_id = {message.chat.id}")
                                            base.commit()
                                            markup_games = await kb.markup_games(message)
                                            await message.answer(locales.for_all_games[f'for_all_games_win_game_{BotDB.user_language(message.chat.id)}'].format(betting * 1.95), reply_markup=markup_games)
                                        for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                            markup_again_fifty_four = await kb.markup_again_fifty_four(message)
                                            await message.answer(locales.fifty_game[f'fifty_four_result_{BotDB.user_language(message.chat.id)}'].format(values[0], data['random_number_four_first'], data['random_number_four_second']), reply_markup=markup_again_fifty_four, parse_mode='html')
                                            await state.finish()
                                    else:
                                        cur.execute(f"UPDATE achivement SET game_fifty = game_fifty + 1 WHERE user_id = {message.chat.id}")
                                        cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} WHERE user_id = {message.chat.id}")
                                        base.commit()
                                        for valuess in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                            markup_games = await kb.markup_games(message)
                                            await message.answer(locales.for_all_games[f'for_all_games_lose_game_{BotDB.user_language(message.chat.id)}'].format(betting), parse_mode='html', reply_markup=markup_games)
                                            markup_again_fifty_four = await kb.markup_again_fifty_four(message)
                                            await message.answer(locales.fifty_game[f'fifty_four_result_{BotDB.user_language(message.chat.id)}'].format(valuess[0], data['random_number_four_first'], data['random_number_four_second']), reply_markup=markup_again_fifty_four, parse_mode='html')
                                            await state.finish()
                                else:
                                    await bot.send_message(message.chat.id, locales.fifty_game[f'fifty_four_range_game_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            except:
                                await message.answer(locales.fifty_game[f'fifty_four_error_range_game_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_fifty_four, parse_mode='html')

                if call.data == 'classic_dice_game':
                    await states.dice.bet_classic.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_intro_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                    @dp.message_handler(state=states.dice.bet_classic)
                    async def random_number_classic(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['bet_classic'] = float(message.text)
                            betting = data['bet_classic']
                            if betting <= 1000:
                                if betting > 0:
                                    user_id_mod = message.from_user.id
                                    for value_bet_classic in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = ?", (user_id_mod,)):
                                        if betting <= value_bet_classic[0]:
                                            await states.dice.next()
                                            await bot.send_message(message.chat.id, locales.dice[f'dice_game_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_dice_classic)
                                        else:
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                else:
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_min_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_max_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()

                    @dp.message_handler(state=states.dice.random_number_classic)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.dice.random_number_classic.set()
                            data['random_number_classic'] = await bot.send_dice(message.chat.id)
                            data['random_number_classic'] = data['random_number_classic']['dice'] ['value']
                        try:
                            betting = data['bet_classic']
                            await asyncio.sleep(4)
                            if int(message.text) >= 1 and int(message.text) <= 6:
                                if int(message.text) == data['random_number_classic']:
                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 4.8 WHERE user_id = {message.chat.id}")
                                    cur.execute(f"UPDATE achivement SET game_cub = game_cub + 1 WHERE user_id = {message.chat.id}")
                                    base.commit()
                                    for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_win_game_{BotDB.user_language(message.chat.id)}'].format(betting * 5.8), reply_markup=markup_games)
                                        markup_again_dice_classic = await kb.markup_again_dice_classic(message)
                                        await message.answer(locales.dice[f'dice_result_{BotDB.user_language(message.chat.id)}'].format(values[0], data['random_number_classic']), reply_markup=markup_again_dice_classic, parse_mode='html')
                                        await state.finish()
                                else:
                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} WHERE user_id = {message.chat.id}")
                                    cur.execute(f"UPDATE achivement SET game_cub = game_cub + 1 WHERE user_id = {message.chat.id}")
                                    base.commit()
                                    for valuess in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_lose_game_{BotDB.user_language(message.chat.id)}'].format(betting), parse_mode='html', reply_markup=markup_games)
                                        markup_again_dice_classic = await kb.markup_again_dice_classic(message)
                                        await message.answer(locales.dice[f'dice_result_{BotDB.user_language(message.chat.id)}'].format(valuess[0], data['random_number_classic']), reply_markup=markup_again_dice_classic, parse_mode='html')
                                        await state.finish()
                            else:
                                await bot.send_message(message.chat.id, locales.dice[f'dice_classic_range_game_{BotDB.user_language(message.chat.id)}'], parse_mode='html', reply_markup=kb.markup_select_dice_classic)
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await message.answer(locales.dice[f'dice_classic_error_range_game_{BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_select_dice_classic, parse_mode='html')

                if call.data == 'under_s_game':
                    await states.dice.bet_under.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_intro_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                    @dp.message_handler(state=states.dice.bet_under)
                    async def random_number_under(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['bet_under'] = float(message.text)
                            betting = data['bet_under']
                            if betting <= 1000:
                                if betting > 0:
                                    user_id_mod = message.from_user.id
                                    for value_bet_under in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = ?", (user_id_mod,)):
                                        if betting <= value_bet_under[0]:
                                            await states.dice.next()
                                            markup_select_dice_under = await kb.markup_select_dice_under(message)
                                            await bot.send_message(message.chat.id, locales.dice[f'dice_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_select_dice_under)
                                        else:
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                else:
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_min_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_max_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()

                    @dp.message_handler(state=states.dice.random_number_under)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.dice.random_number_under.set()
                            data['random_number_under_first'] = await bot.send_dice(message.chat.id)
                            data['random_number_under_second'] = await bot.send_dice(message.chat.id)
                            if data['random_number_under_first']['dice']['value'] + data['random_number_under_second']['dice']['value'] < 7:
                                data['random_number_under'] = '(x2) 🎲 Менше 7'
                            elif data['random_number_under_first']['dice']['value'] + data['random_number_under_second']['dice']['value'] == 7:
                                data['random_number_under'] = '(x5.8) 🎲 7'
                            elif data['random_number_under_first']['dice']['value'] + data['random_number_under_second']['dice']['value'] > 7:
                                data['random_number_under'] = '(x2) 🎲 Більше 7'
                            else:
                                markup_games = await kb.markup_games(message)
                                await message.answer(f'Error', reply_markup=markup_games)
                        try:
                            betting = data['bet_under']
                            await asyncio.sleep(4)
                            if message.text == '(x2) 🎲 Менше 7' or message.text == '(x2) 🎲 Less than 7' or message.text == '(x2) 🎲 Меньше 7' or message.text == '(x5.8) 🎲 7' or message.text == '(x2) 🎲 Більше 7' or message.text == '(x2) 🎲 More than 7' or message.text == '(x2) 🎲 Больше 7':
                                if message.text == data['random_number_under']:
                                    if data['random_number_under_first']['dice']['value'] + data['random_number_under_second']['dice']['value'] == 7:
                                        cur.execute(f"UPDATE achivement SET game_cub = game_cub + 1 WHERE user_id = {message.chat.id}")
                                        cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 4.8 WHERE user_id = {message.chat.id}")
                                        base.commit()
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_win_game_{BotDB.user_language(message.chat.id)}'].format(betting * 5.8), reply_markup=markup_games)
                                    else:
                                        cur.execute(f"UPDATE achivement SET game_cub = game_cub + 1 WHERE user_id = {message.chat.id}")
                                        cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} WHERE user_id = {message.chat.id}")
                                        base.commit()
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_win_game_{BotDB.user_language(message.chat.id)}'].format(betting * 2), reply_markup=markup_games)
                                    for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_again_dice_under = await kb.markup_again_dice_under(message)
                                        await message.answer(locales.dice[f'dice_result_{BotDB.user_language(message.chat.id)}'].format(values[0], data['random_number_under']), reply_markup=markup_again_dice_under, parse_mode='html')
                                    await state.finish()
                                else:
                                    cur.execute(f"UPDATE achivement SET game_cub = game_cub + 1 WHERE user_id = {message.chat.id}")
                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} WHERE user_id = {message.chat.id}")
                                    base.commit()
                                    for valuess in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.chat.id}"):
                                        markup_games = await kb.markup_games(message)
                                        await message.answer(locales.for_all_games[f'for_all_games_lose_game_{BotDB.user_language(message.chat.id)}'].format(betting), parse_mode='html', reply_markup=markup_games)
                                        markup_again_dice_under = await kb.markup_again_dice_under(message)
                                        await message.answer(locales.dice[f'dice_result_{BotDB.user_language(message.chat.id)}'].format(valuess[0], data['random_number_under']), reply_markup=markup_again_dice_under, parse_mode='html')
                                        await state.finish()
                            else:
                                markup_select_dice_under = await kb.markup_select_dice_under(message)
                                await bot.send_message(message.chat.id, locales.dice[f'dice_under_range_game_{BotDB.user_language(message.chat.id)}'], parse_mode='html', reply_markup=markup_select_dice_under)
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            markup_select_dice_under = await kb.markup_select_dice_under(message)
                            await message.answer(locales.dice[f'dice_under_error_range_game_{BotDB.user_language(message.chat.id)}'], parse_mode='html', reply_markup=markup_select_dice_under)

                if call.data == 'br_case_game':
                    await states.cases.case_br_buy.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.cases_game[f'cases_game_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), parse_mode='html')
                    markup_accept_cases = await kb.markup_accept_cases(call.message)
                    await bot.send_message(call.message.chat.id, locales.cases_game[f'cases_ask_buy_br_case_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_accept_cases, parse_mode='html')

                    @dp.callback_query_handler(state=states.cases.case_br_buy, text_contains='accept_case_game')
                    async def answer(message: types.Message, state: FSMContext):
                        for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.from_user.id}"):
                            if values[0] >= 10:
                                markup_games = await kb.markup_games(message)
                                await bot.send_message(message.from_user.id, locales.cases_game[f'cases_buy_br_case_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_games, parse_mode='html')
                                anim_num = random.sample(range(5, 15), 3)
                                for rand_anim in anim_num:
                                    await asyncio.sleep(0.5)
                                    await bot.send_message(message.from_user.id, locales.cases_game[f'cases_anim_{BotDB.user_language(message.from_user.id)}'] + '<b>' + str(rand_anim) + ' TRX</b> ❓', parse_mode='html')
                                cash = random.randint(5, 15)
                                if cash >=13:
                                    cash = random.randint(5, 15)
                                cur.execute(f"UPDATE achivement SET game_case = game_case + 1 WHERE user_id = {message.from_user.id}")
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx + {cash} - 10 WHERE user_id = {message.from_user.id}")
                                base.commit()
                                markup_games = await kb.markup_games(message)
                                await bot.send_message(message.from_user.id, locales.cases_game[f'cases_win_{BotDB.user_language(message.from_user.id)}'].format(cash), reply_markup=markup_games)
                                for valuess in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.from_user.id}"):
                                    markup_again_br_case = await kb.markup_again_br_case(message)
                                    await bot.send_message(message.from_user.id, locales.cases_game[f'cases_result_{BotDB.user_language(message.from_user.id)}'].format(valuess[0]), reply_markup=markup_again_br_case, parse_mode='html')
                                await state.finish()
                            else:
                                await bot.send_message(message.from_user.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                                await state.finish()

                if call.data == 'si_case_game':
                    await states.cases.case_si_buy.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.cases_game[f'cases_game_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), parse_mode='html')
                    markup_accept_cases = await kb.markup_accept_cases(call.message)
                    await bot.send_message(call.message.chat.id, locales.cases_game[f'cases_ask_buy_si_case_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_accept_cases, parse_mode='html')

                    @dp.callback_query_handler(state=states.cases.case_si_buy, text_contains='accept_case_game')
                    async def answer(message: types.Message, state: FSMContext):
                        for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.from_user.id}"):
                            if values[0] >= 100:
                                markup_games = await kb.markup_games(message)
                                await bot.send_message(message.from_user.id, locales.cases_game[f'cases_buy_si_case_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_games, parse_mode='html')
                                anim_num = random.sample(range(50, 150), 3)
                                for rand_anim in anim_num:
                                    await asyncio.sleep(0.5)
                                    await bot.send_message(message.from_user.id, locales.cases_game[f'cases_anim_{BotDB.user_language(message.from_user.id)}'] + '<b>' + str(rand_anim) + ' TRX</b> ❓', parse_mode='html')
                                cash = random.randint(50, 150)
                                if cash >=135:
                                    cash = random.randint(50, 150)
                                cur.execute(f"UPDATE achivement SET game_case = game_case + 1 WHERE user_id = {message.from_user.id}")
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx + {cash} - 100 WHERE user_id = {message.from_user.id}")
                                base.commit()
                                markup_games = await kb.markup_games(message)
                                await bot.send_message(message.from_user.id, locales.cases_game[f'cases_win_{BotDB.user_language(message.from_user.id)}'].format(cash), reply_markup=markup_games)
                                for valuess in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.from_user.id}"):
                                    markup_again_si_case = await kb.markup_again_si_case(message)
                                    await bot.send_message(message.from_user.id, locales.cases_game[f'cases_result_{BotDB.user_language(message.from_user.id)}'].format(valuess[0]), reply_markup=markup_again_si_case, parse_mode='html')
                                await state.finish()
                            else:
                                await bot.send_message(message.from_user.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                                await state.finish()

                if call.data == 'go_case_game':
                    await states.cases.case_go_buy.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.cases_game[f'cases_game_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), parse_mode='html')
                    markup_accept_cases = await kb.markup_accept_cases(call.message)
                    await bot.send_message(call.message.chat.id, locales.cases_game[f'cases_ask_buy_go_case_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_accept_cases, parse_mode='html')

                    @dp.callback_query_handler(state=states.cases.case_go_buy, text_contains='accept_case_game')
                    async def answer(message: types.Message, state: FSMContext):
                        for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.from_user.id}"):
                            if values[0] >= 1000:
                                markup_games = await kb.markup_games(message)
                                await bot.send_message(message.from_user.id, locales.cases_game[f'cases_buy_go_case_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_games, parse_mode='html')
                                anim_num = random.sample(range(0, 1500), 3)
                                for rand_anim in anim_num:
                                    await asyncio.sleep(0.5)
                                    await bot.send_message(message.from_user.id, locales.cases_game[f'cases_anim_{BotDB.user_language(message.from_user.id)}'] + '<b>' + str(rand_anim) + ' TRX</b> ❓', parse_mode='html')
                                cash = random.randint(0, 1500)
                                if cash >=1350:
                                    cash = random.randint(0, 1500)
                                cur.execute(f"UPDATE achivement SET game_case = game_case + 1 WHERE user_id = {message.from_user.id}")
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx + {cash} - 1000 WHERE user_id = {message.from_user.id}")
                                base.commit()
                                markup_games = await kb.markup_games(message)
                                await bot.send_message(message.from_user.id, locales.cases_game[f'cases_win_{BotDB.user_language(message.from_user.id)}'].format(cash), reply_markup=markup_games)
                                for valuess in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.from_user.id}"):
                                    markup_again_go_case = await kb.markup_again_go_case(message)
                                    await bot.send_message(message.from_user.id, locales.cases_game[f'cases_result_{BotDB.user_language(message.from_user.id)}'].format(valuess[0]), reply_markup=markup_again_go_case, parse_mode='html')
                                await state.finish()
                            else:
                                await bot.send_message(message.from_user.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                                await state.finish()

                if call.data == 'lot_buy_game':
                    if not BotDB.lot_exists(call.message.chat.id):
                        for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                            if value[0] >= 15:
                                BotDB.add_lot(call.message.chat.id)
                                await call.answer(locales.lot_game[f'lot_game_acc_{BotDB.user_language(call.message.chat.id)}'])
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx - 15 WHERE user_id = {call.message.chat.id}")
                                await call.message.answer(locales.lot_game[f'lot_game_cong_{BotDB.user_language(call.message.chat.id)}'])
                                await call.message.answer(locales.lot_game[f'lot_game_luck_{BotDB.user_language(call.message.chat.id)}'])
                                return base.commit()
                            else:
                                await call.message.answer(locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(call.message.chat.id)}'])
                    else:
                        await call.message.answer(locales.lot_game[f'lot_game_alert_{BotDB.user_language(call.message.chat.id)}'])

                if call.data == 'miner_three_game':
                    await states.miner.bet_three.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_intro_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')
                    @dp.message_handler(state=states.miner.bet_three)
                    async def random_number_three(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['bet_three'] = float(message.text)
                            betting = data['bet_three']
                            if betting <= 1000:
                                if betting > 0:
                                    user_id_mod = message.from_user.id
                                    for value_bet_three in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = ?", (user_id_mod,)):
                                        if betting <= value_bet_three[0]:
                                            await states.miner.next()
                                            random.shuffle(kb.list_buts)
                                            markup = types.InlineKeyboardMarkup()
                                            for text, data in kb.list_buts:
                                                markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
                                            await bot.send_message(message.chat.id, locales.miner_game[f'miner_game_ask_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup)
                                        else:
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                else:
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_min_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_max_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()
                    @dp.callback_query_handler(state=states.miner.random_number_three)
                    async def answer(call: types.CallbackQuery, state: FSMContext):
                        async with state.proxy() as data:
                            betting = data['bet_three']
                        try:
                            await call.message.answer("_🟡_", parse_mode='html')
                            await asyncio.sleep(0.7)
                            await call.message.answer("_💣_", parse_mode='html')
                            await asyncio.sleep(0.7)
                            if call.data == 'field_1' or call.data == 'field_2' or call.data == 'field_3' or call.data == 'field_4' or call.data == 'field_5' or call.data == 'field_6':
                                await call.message.answer("👍", parse_mode='html')
                                await asyncio.sleep(0.7)
                                cur.execute(f"UPDATE achivement SET game_mine = game_mine + 1 WHERE user_id = {call.message.chat.id}")
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 0.7 WHERE user_id = {call.message.chat.id}")
                                base.commit()
                                markup_games = await kb.markup_games_(call.message)
                                await call.message.answer(locales.miner_game[f'miner_game_win_{BotDB.user_language(call.message.chat.id)}'].format(betting * 1.7), reply_markup=markup_games)
                                for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                                    markup_again_miner_three = await kb.markup_again_miner_three(call.message)
                                    await call.message.answer(locales.miner_game[f'miner_game_result_{BotDB.user_language(call.message.chat.id)}'].format(values[0]), reply_markup=markup_again_miner_three, parse_mode='html')
                                await call.answer()
                                await state.finish()
                            else:
                                await call.message.answer("💥", parse_mode='html')
                                await asyncio.sleep(0.7)
                                cur.execute(f"UPDATE achivement SET game_mine = game_mine + 1 WHERE user_id = {call.message.chat.id}")
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} WHERE user_id = {call.message.chat.id}")
                                base.commit()
                                markup_games = await kb.markup_games_(call.message)
                                await call.message.answer(locales.miner_game[f'miner_game_lose_{BotDB.user_language(call.message.chat.id)}'].format(betting), parse_mode='html', reply_markup=markup_games)
                                for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                                    markup_again_miner_three = await kb.markup_again_miner_three(call.message)
                                    await call.message.answer(locales.miner_game[f'miner_game_result_{BotDB.user_language(call.message.chat.id)}'].format(values[0]), reply_markup=markup_again_miner_three, parse_mode='html')
                                await call.answer()
                                await state.finish()
                        except:
                            await call.message.answer(locales.miner_game[f'miner_game_error_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')

                if call.data == 'miner_five_game':
                    await states.miner.bet_five.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_intro_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')
                    @dp.message_handler(state=states.miner.bet_five)
                    async def random_number_five(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['bet_five'] = float(message.text)
                            betting = data['bet_five']
                            if betting <= 1000:
                                if betting > 0:
                                    user_id_mod = message.from_user.id
                                    for value_bet_five in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = ?", (user_id_mod,)):
                                        if betting <= value_bet_five[0]:
                                            await states.miner.next()
                                            random.shuffle(kb.list_buts)
                                            markup = types.InlineKeyboardMarkup()
                                            for text, data in kb.list_buts:
                                                markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
                                            await bot.send_message(message.chat.id, locales.miner_game[f'miner_game_ask_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup)
                                        else:
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                else:
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_min_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_max_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()
                    @dp.callback_query_handler(state=states.miner.random_number_five)
                    async def answer(call: types.CallbackQuery, state: FSMContext):
                        async with state.proxy() as data:
                            betting = data['bet_five']
                        try:
                            await call.message.answer("_🟡_", parse_mode='html')
                            await asyncio.sleep(0.7)
                            await call.message.answer("_💣_", parse_mode='html')
                            await asyncio.sleep(0.7)
                            if call.data == 'field_1' or call.data == 'field_2' or call.data == 'field_3' or call.data == 'field_4':
                                await call.message.answer("👍", parse_mode='html')
                                await asyncio.sleep(0.7)
                                cur.execute(f"UPDATE achivement SET game_mine = game_mine + 1 WHERE user_id = {call.message.chat.id}")
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 1 WHERE user_id = {call.message.chat.id}")
                                base.commit()
                                markup_games = await kb.markup_games_(call.message)
                                await call.message.answer(locales.miner_game[f'miner_game_win_{BotDB.user_language(call.message.chat.id)}'].format(betting * 2), reply_markup=markup_games)
                                for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                                    markup_again_miner_five = await kb.markup_again_miner_five(call.message)
                                    await call.message.answer(locales.miner_game[f'miner_game_result_{BotDB.user_language(call.message.chat.id)}'].format(values[0]), reply_markup=markup_again_miner_five, parse_mode='html')
                                await call.answer()
                                await state.finish()
                            else:
                                await call.message.answer("💥", parse_mode='html')
                                await asyncio.sleep(0.7)
                                cur.execute(f"UPDATE achivement SET game_mine = game_mine + 1 WHERE user_id = {call.message.chat.id}")
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} WHERE user_id = {call.message.chat.id}")
                                base.commit()
                                markup_games = await kb.markup_games_(call.message)
                                await call.message.answer(locales.miner_game[f'miner_game_lose_{BotDB.user_language(call.message.chat.id)}'].format(betting), parse_mode='html', reply_markup=markup_games)
                                for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                                    markup_again_miner_five = await kb.markup_again_miner_five(call.message)
                                    await call.message.answer(locales.miner_game[f'miner_game_result_{BotDB.user_language(call.message.chat.id)}'].format(values[0]), reply_markup=markup_again_miner_five, parse_mode='html')
                                await call.answer()
                                await state.finish()
                        except:
                            await call.message.answer(locales.miner_game[f'miner_game_error_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')

                if call.data == 'miner_seven_game':
                    await states.miner.bet_seven.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_intro_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')
                    @dp.message_handler(state=states.miner.bet_seven)
                    async def random_number_seven(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['bet_seven'] = float(message.text)
                            betting = data['bet_seven']
                            if betting <= 1000:
                                if betting > 0:
                                    user_id_mod = message.from_user.id
                                    for value_bet_seven in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = ?", (user_id_mod,)):
                                        if betting <= value_bet_seven[0]:
                                            await states.miner.next()
                                            random.shuffle(kb.list_buts)
                                            markup = types.InlineKeyboardMarkup()
                                            for text, data in kb.list_buts:
                                                markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
                                            await bot.send_message(message.chat.id, locales.miner_game[f'miner_game_ask_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup)
                                        else:
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                else:
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_min_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_max_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()
                    @dp.callback_query_handler(state=states.miner.random_number_seven)
                    async def answer(call: types.CallbackQuery, state: FSMContext):
                        async with state.proxy() as data:
                            betting = data['bet_seven']
                        try:
                            await call.message.answer("_🟡_", parse_mode='html')
                            await asyncio.sleep(0.7)
                            await call.message.answer("_💣_", parse_mode='html')
                            await asyncio.sleep(0.7)
                            if call.data == 'field_1' or call.data == 'field_2':
                                await call.message.answer("👍", parse_mode='html')
                                await asyncio.sleep(0.7)
                                cur.execute(f"UPDATE achivement SET game_mine = game_mine + 1 WHERE user_id = {call.message.chat.id}")
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 3.5 WHERE user_id = {call.message.chat.id}")
                                base.commit()
                                markup_games = await kb.markup_games_(call.message)
                                await call.message.answer(locales.miner_game[f'miner_game_win_{BotDB.user_language(call.message.chat.id)}'].format(betting * 4.5), reply_markup=markup_games)
                                for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                                    markup_again_miner_seven = await kb.markup_again_miner_seven(call.message)
                                    await call.message.answer(locales.miner_game[f'miner_game_result_{BotDB.user_language(call.message.chat.id)}'].format(values[0]), reply_markup=markup_again_miner_seven, parse_mode='html')
                                await call.answer()
                                await state.finish()
                            else:
                                await call.message.answer("💥", parse_mode='html')
                                await asyncio.sleep(0.7)
                                cur.execute(f"UPDATE achivement SET game_mine = game_mine + 1 WHERE user_id = {call.message.chat.id}")
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} WHERE user_id = {call.message.chat.id}")
                                base.commit()
                                markup_games = await kb.markup_games_(call.message)
                                await call.message.answer(locales.miner_game[f'miner_game_lose_{BotDB.user_language(call.message.chat.id)}'].format(betting), parse_mode='html', reply_markup=markup_games)
                                for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                                    markup_again_miner_seven = await kb.markup_again_miner_seven(call.message)
                                    await call.message.answer(locales.miner_game[f'miner_game_result_{BotDB.user_language(call.message.chat.id)}'].format(values[0]), reply_markup=markup_again_miner_seven, parse_mode='html')
                                await call.answer()
                                await state.finish()
                        except:
                            await call.message.answer(locales.miner_game[f'miner_game_error_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')

                if call.data == 'accept_spin':
                    await states.spin.bet_spin.set()
                    for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {call.message.chat.id}"):
                        await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_intro_{BotDB.user_language(call.message.chat.id)}'].format(value[0]), reply_markup=kb.markup_select_bet, parse_mode='html')

                    @dp.message_handler(state=states.spin.bet_spin)
                    async def random_number_spin(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['bet_spin'] = float(message.text)
                            betting = data['bet_spin']
                            if betting <= 1000:
                                if betting > 0:
                                    user_id_mod = message.from_user.id
                                    for value_bet_spin in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = ?", (user_id_mod,)):
                                        if betting <= value_bet_spin[0]:
                                            await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_ready_{BotDB.user_language(message.chat.id)}'])
                                            async with state.proxy() as data:
                                                await states.spin.random_number_spin.set()
                                                markup_games = await kb.markup_games(message)
                                                data['random_number_spin'] = await message.answer_dice(emoji="🎰", reply_markup=markup_games)
                                                data['random_number_spin'] = data['random_number_spin']['dice']['value']
                                            try:
                                                betting = data['bet_spin']
                                                await asyncio.sleep(2)
                                                cur.execute(f"UPDATE achivement SET game_slot = game_slot + 1 WHERE user_id = {user_id_mod}")
                                                base.commit()
                                                """
                                                 0     1       2    3
                                                BAR виноград лимон сім
        
                                                1 ['BAR', 'BAR', 'BAR']
        
                                                2 ['виноград', 'BAR', 'BAR']
        
                                                3 ['лимон', 'BAR', 'BAR']
        
                                                4 ['семь', 'BAR', 'BAR']
        
                                                5 ['BAR', 'виноград', 'BAR']
        
                                                6 ['виноград', 'виноград', 'BAR']
        
                                                7 ['лимон', 'виноград', 'BAR']
        
                                                8 ['семь', 'виноград', 'BAR']
        
                                                9 ['BAR', 'лимон', 'BAR']
        
                                                10 ['виноград', 'лимон', 'BAR']
        
                                                11 ['лимон', 'лимон', 'BAR']
        
                                                12 ['семь', 'лимон', 'BAR']
        
                                                13 ['BAR', 'семь', 'BAR']
        
                                                14 ['виноград', 'семь', 'BAR']
        
                                                15 ['лимон', 'семь', 'BAR']
        
                                                16 ['семь', 'семь', 'BAR']
        
                                                17 ['BAR', 'BAR', 'виноград']
        
                                                18 ['виноград', 'BAR', 'виноград']
        
                                                19 ['лимон', 'BAR', 'виноград']
        
                                                20 ['семь', 'BAR', 'виноград']
        
                                                21 ['BAR', 'виноград', 'виноград']
        
                                                22 ['виноград', 'виноград', 'виноград']
        
                                                23 ['лимон', 'виноград', 'виноград']
        
                                                24 ['семь', 'виноград', 'виноград']
        
                                                25 ['BAR', 'лимон', 'виноград']
        
                                                26 ['виноград', 'лимон', 'виноград']
        
                                                27 ['лимон', 'лимон', 'виноград']
        
                                                28 ['семь', 'лимон', 'виноград']
        
                                                29 ['BAR', 'семь', 'виноград']
        
                                                30 ['виноград', 'семь', 'виноград']
        
                                                31 ['лимон', 'семь', 'виноград']
        
                                                32 ['семь', 'семь', 'виноград']
        
                                                33 ['BAR', 'BAR', 'лимон']
        
                                                34 ['виноград', 'BAR', 'лимон']
        
                                                35 ['лимон', 'BAR', 'лимон']
        
                                                36 ['семь', 'BAR', 'лимон']
        
                                                37 ['BAR', 'виноград', 'лимон']
        
                                                38 ['виноград', 'виноград', 'лимон']
        
                                                39 ['лимон', 'виноград', 'лимон']
        
                                                40 ['семь', 'виноград', 'лимон']
        
                                                41 ['BAR', 'лимон', 'лимон']
        
                                                42 ['виноград', 'лимон', 'лимон']
        
                                                43 ['лимон', 'лимон', 'лимон']
        
                                                44 ['семь', 'лимон', 'лимон']
        
                                                45 ['BAR', 'семь', 'лимон']
        
                                                46 ['виноград', 'семь', 'лимон']
        
                                                47 ['лимон', 'семь', 'лимон']
        
                                                48 ['семь', 'семь', 'лимон']
        
                                                49 ['BAR', 'BAR', 'семь']
        
                                                50 ['виноград', 'BAR', 'семь']
        
                                                51 ['лимон', 'BAR', 'семь']
        
                                                52 ['семь', 'BAR', 'семь']
        
                                                53 ['BAR', 'виноград', 'семь']
        
                                                54 ['виноград', 'виноград', 'семь']
        
                                                55 ['лимон', 'виноград', 'семь']
        
                                                56 ['семь', 'виноград', 'семь']
        
                                                57 ['BAR', 'лимон', 'семь']
        
                                                58 ['виноград', 'лимон', 'семь']
        
                                                59 ['лимон', 'лимон', 'семь']
        
                                                60 ['семь', 'лимон', 'семь']
        
                                                61 ['BAR', 'семь', 'семь']
        
                                                62 ['виноград', 'семь', 'семь']
        
                                                63 ['лимон', 'семь', 'семь']
        
                                                64 ['семь', 'семь', 'семь']
        
                                                """
                                                if data['random_number_spin'] in (1, 22, 43):# три в ряд без сімок
                                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 2 WHERE user_id = {user_id_mod}")
                                                    base.commit()
                                                    markup_games = await kb.markup_games(message)
                                                    await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_win_{BotDB.user_language(message.chat.id)}'].format(betting * 3), reply_markup=markup_games)
                                                    for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {user_id_mod}"):
                                                        markup_again_slot = await kb.markup_again_slot(message)
                                                        await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_result_{BotDB.user_language(message.chat.id)}'].format(values[0]), reply_markup=markup_again_slot, parse_mode='html')
                                                    await state.finish()
                                                elif data['random_number_spin'] in (16, 32, 48):# дві сімки на початку
                                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 4 WHERE user_id = {user_id_mod}")
                                                    base.commit()
                                                    markup_games = await kb.markup_games(message)
                                                    await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_win_{BotDB.user_language(message.chat.id)}'].format(betting * 5), reply_markup=markup_games)
                                                    for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {user_id_mod}"):
                                                        markup_again_slot = await kb.markup_again_slot(message)
                                                        await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_result_{BotDB.user_language(message.chat.id)}'].format(values[0]), reply_markup=markup_again_slot, parse_mode='html')
                                                    await state.finish()
                                                # два співпадіння
                                                elif data['random_number_spin'] in (2, 3, 4, 5, 6, 9, 13, 17, 33, 49, 18, 21, 23, 24, 26, 30, 38, 54, 11, 27, 35, 39, 41, 42, 44, 47, 59, 52, 56, 60, 61, 62, 63):
                                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} * 0.7 WHERE user_id = {user_id_mod}")
                                                    base.commit()
                                                    markup_games = await kb.markup_games(message)
                                                    await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_win_{BotDB.user_language(message.chat.id)}'].format(betting * 0.3), reply_markup=markup_games)
                                                    for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {user_id_mod}"):
                                                        markup_again_slot = await kb.markup_again_slot(message)
                                                        await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_result_{BotDB.user_language(message.chat.id)}'].format(values[0]), reply_markup=markup_again_slot, parse_mode='html')
                                                    await state.finish()
                                                elif data['random_number_spin'] == 64:# три сімки
                                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx + {betting} * 14 WHERE user_id = {user_id_mod}")
                                                    base.commit()
                                                    await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_win_jackpot_{BotDB.user_language(message.chat.id)}'].format(betting * 15))
                                                    await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_win_jackpot_text_{BotDB.user_language(message.chat.id)}'])
                                                    for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {user_id_mod}"):
                                                        markup_again_slot = await kb.markup_again_slot(message)
                                                        await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_result_{BotDB.user_language(message.chat.id)}'].format(values[0]), reply_markup=markup_again_slot, parse_mode='html')
                                                    await state.finish()
                                                else:
                                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx - {betting} WHERE user_id = {user_id_mod}")
                                                    base.commit()
                                                    markup_games = await kb.markup_games(message)
                                                    await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_lose_{BotDB.user_language(message.chat.id)}'].format(betting), parse_mode='html', reply_markup=markup_games)
                                                    for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {user_id_mod}"):
                                                        markup_again_slot = await kb.markup_again_slot(message)
                                                        await bot.send_message(message.chat.id, locales.spin_game[f'spin_game_result_{BotDB.user_language(message.chat.id)}'].format(values[0]), reply_markup=markup_again_slot, parse_mode='html')
                                                    await state.finish()
                                            except:
                                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                        else:
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_no_money_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                else:
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_min_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                    await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_max_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                                await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_another_sum_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()

                if call.data == 'promo_bon_cab':
                    if await check_sub_channels(CHANNELS, call.message.chat.id):
                        await states.promo_code.type_promo.set()
                        markup_cancel_promo = await kb.markup_cancel_promo(call.message)
                        await bot.send_message(call.message.chat.id, locales.promo_code[f'promo_type_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_cancel_promo)

                        @dp.message_handler(state=states.promo_code.type_promo)
                        async def promo_text(message: types.Message, state: FSMContext):
                            try:
                                first_promo = 'Ocgt3Ic21'
                                second_promo = 'msv7D2s4'
                                if not BotDB.promo_exists(message.from_user.id):
                                    cur.execute("INSERT INTO `promo_codes` (`user_id`, `promo_code`) VALUES (?, ?)", (message.from_user.id, first_promo,))
                                    cur.execute("INSERT INTO `promo_codes` (`user_id`, `promo_code`) VALUES (?, ?)", (message.from_user.id, second_promo,))
                                    base.commit()
                                async with state.proxy() as data:
                                    data['type_promo'] = message.text
                                if data['type_promo'] == first_promo:
                                    for value_check_promo in cur.execute(f"SELECT c_promo_code FROM promo_codes WHERE user_id = {message.from_user.id} AND promo_code = '{data['type_promo']}'"):
                                        if value_check_promo[0] != 1:
                                            for value_count_promo in cur.execute(f"SELECT count_promo_code FROM count_promo_codes WHERE promo_code = '{data['type_promo']}'"):
                                                if value_count_promo[0] < 250:
                                                    markup_start = await kb.markup_start(message)
                                                    await bot.send_message(message.from_user.id, locales.promo_code[f'promo_use_{BotDB.user_language(message.chat.id)}'].format(first_promo), reply_markup=markup_start)
                                                    await bot.send_message(message.from_user.id, locales.promo_code[f'promo_earn_{BotDB.user_language(message.chat.id)}'])
                                                    cur.execute(f"UPDATE promo_codes SET `c_promo_code` = 1 WHERE user_id = {message.from_user.id} AND promo_code = '{data['type_promo']}'")
                                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx + 0.5 WHERE user_id = {message.from_user.id}")
                                                    cur.execute(f"UPDATE count_promo_codes SET count_promo_code = count_promo_code + 1 WHERE promo_code = '{data['type_promo']}'")
                                                    base.commit()
                                                    await state.finish()
                                                else:
                                                    markup_cancel_promo = await kb.markup_cancel_promo(message)
                                                    await bot.send_message(message.from_user.id, locales.promo_code[f'promo_not_exists_{BotDB.user_language(message.from_user.id)}'].format(message.text), parse_mode='html', reply_markup=markup_cancel_promo)
                                        else:
                                            markup_start = await kb.markup_start(message)
                                            await bot.send_message(message.from_user.id, locales.promo_code[f'promo_use_once_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_start)
                                            await state.finish()
                                elif data['type_promo'] == second_promo:
                                    for value_check_promo in cur.execute(f"SELECT c_promo_code FROM promo_codes WHERE user_id = {message.from_user.id} AND promo_code = '{data['type_promo']}'"):
                                        if value_check_promo[0] != 1:
                                            for value_count_promo in cur.execute(f"SELECT count_promo_code FROM count_promo_codes WHERE promo_code = '{data['type_promo']}'"):
                                                if value_count_promo[0] < 250:
                                                    markup_start = await kb.markup_start(message)
                                                    await bot.send_message(message.from_user.id, locales.promo_code[f'promo_use_{BotDB.user_language(message.chat.id)}'].format(second_promo), reply_markup=markup_start)
                                                    await bot.send_message(message.from_user.id, locales.promo_code[f'promo_earn_{BotDB.user_language(message.chat.id)}'])
                                                    cur.execute(f"UPDATE promo_codes SET `c_promo_code` = 1 WHERE user_id = {message.from_user.id} AND promo_code = '{data['type_promo']}'")
                                                    cur.execute(f"UPDATE users SET bal_trx = bal_trx + 0.5 WHERE user_id = {message.from_user.id}")
                                                    cur.execute(f"UPDATE count_promo_codes SET count_promo_code = count_promo_code + 1 WHERE promo_code = '{data['type_promo']}'")
                                                    base.commit()
                                                    await state.finish()
                                                else:
                                                    markup_cancel_promo = await kb.markup_cancel_promo(message)
                                                    await bot.send_message(message.from_user.id, locales.promo_code[f'promo_not_exists_{BotDB.user_language(message.from_user.id)}'].format(message.text).format(message.text), parse_mode='html', reply_markup=markup_cancel_promo)
                                        else:
                                            markup_start = await kb.markup_start(message)
                                            await bot.send_message(message.from_user.id, locales.promo_code[f'promo_use_once_{BotDB.user_language(message.from_user.id)}'], reply_markup=markup_start)
                                            await state.finish()
                                elif message.text == '🚫 Повернутись назад 🚫' or message.text == '🚫 Вернуться назад 🚫' or message.text == '🚫 Go back 🚫':
                                    await state.finish()
                                    markup_start = await kb.markup_start(message)
                                    await message.answer(locales.promo_code[f'promo_main_menu_{BotDB.user_language(message.from_user.id)}'], parse_mode='HTML', reply_markup=markup_start)
                                else:
                                    markup_cancel_promo = await kb.markup_cancel_promo(message)
                                    await bot.send_message(message.from_user.id, locales.promo_code[f'promo_not_exists_{BotDB.user_language(message.from_user.id)}'].format(message.text), parse_mode='html', reply_markup=markup_cancel_promo)
                            except:
                                markup_start = await kb.markup_start(message)
                                await bot.send_message(message.chat.id, locales.promo_code[f'promo_error_{BotDB.user_language(message.from_user.id)}'], parse_mode='html', reply_markup=markup_start)
                                await bot.send_message(message.chat.id, locales.promo_code[f'promo_back_main_menu_{BotDB.user_language(message.from_user.id)}'], parse_mode='html')
                                await state.finish()
                    else:
                        markup_channels = await kb.markup_channels(call.message)
                        await bot.send_message(call.message.chat.id, NOT_SUB_MESSAGE[f'NOT_SUB_MESSAGE_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_channels)

                if call.data == 'mailing_admin':
                    await bot.send_message(call.message.chat.id, locales.mailing_admin[f'mailing_{BotDB.user_language(call.message.chat.id)}'], reply_markup=types.ReplyKeyboardRemove())
                    await mailing.text.set()

                if call.data == 'pay_history_all_admin':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'all'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[4] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➖ ") + "</b>")
                                        if r[4] != 0:
                                            answer += f"<b><u><i>{r[4]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin)
                    except:
                        pass

                if call.data == 'del_trx_admin' or call.data == 'pay_history_day_admin':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'day'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[4] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➖ ") + "</b>")
                                        if r[4] != 0:
                                            answer += f"<b><u><i>{r[4]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin)
                    except:
                        pass

                if call.data == 'pay_history_month_admin':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'month'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[4] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➖ ") + "</b>")
                                        if r[4] != 0:
                                            answer += f"<b><u><i>{r[4]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin)
                    except:
                        pass

                if call.data == 'pay_history_year_admin':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'year'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[4] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➖ ") + "</b>")
                                        if r[4] != 0:
                                            answer += f"<b><u><i>{r[4]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin)
                    except:
                        pass

                if call.data == 'pay_history_all_not_acces_admin_del_trx':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'year'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[7] == 0:
                                        if r[4] != 0:
                                            answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                            answer += ("<b>" + ("➖ ") + "</b>")
                                            if r[4] != 0:
                                                answer += f"<b><u><i>{r[4]} TRX</i></u></b>"
                                            answer += f"\n🕐 {r[5]}  "
                                            answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                            answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                            if r[7] == 0:
                                                answer += f"<b>❌ Не виконано</b>\n\n"
                                            elif r[7] == 1:
                                                answer += f"<b>✅ Виконано</b>\n\n"
                                            else:
                                                answer += f"<b>💢 Помилка виконання</b>\n\n"
                                        else:
                                            pass
                                    else:
                                        pass
                                if answer != (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n"):
                                    await sleep(0.33)
                                    await call.message.answer(answer, parse_mode='html')
                                else:
                                    pass
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin)
                    except:
                        pass

                if call.data == 'pay_history_all_admin_add_trx':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'all'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[3] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➕ ") + "</b>")
                                        if r[3] != 0:
                                            answer += f"<b><u><i>{r[3]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_trx)
                    except:
                        pass

                if call.data == 'add_trx_admin' or call.data == 'pay_history_day_admin_add_trx':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'day'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[3] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➕ ") + "</b>")
                                        if r[3] != 0:
                                            answer += f"<b><u><i>{r[3]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_trx)
                    except:
                        pass

                if call.data == 'pay_history_month_admin_add_trx':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'month'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[3] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➕ ") + "</b>")
                                        if r[3] != 0:
                                            answer += f"<b><u><i>{r[3]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_trx)
                    except:
                        pass

                if call.data == 'pay_history_year_admin_add_trx':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'year'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[3] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➕ ") + "</b>")
                                        if r[3] != 0:
                                            answer += f"<b><u><i>{r[3]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_trx)
                    except:
                        pass

                if call.data == 'pay_history_all_not_acces_admin_add_trx':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'year'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[7] == 0:
                                        if r[3] != 0:
                                            answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                            answer += ("<b>" + ("➕ ") + "</b>")
                                            if r[3] != 0:
                                                answer += f"<b><u><i>{r[3]} TRX</i></u></b>"
                                            answer += f"\n🕐 {r[5]}  "
                                            answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                            answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                            if r[7] == 0:
                                                answer += f"<b>❌ Не виконано</b>\n\n"
                                            elif r[7] == 1:
                                                answer += f"<b>✅ Виконано</b>\n\n"
                                            else:
                                                answer += f"<b>💢 Помилка виконання</b>\n\n"
                                        else:
                                            pass
                                    else:
                                        pass
                                if answer != (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n"):
                                    await sleep(0.33)
                                    await call.message.answer(answer, parse_mode='html')
                                else:
                                    pass
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_trx)
                    except:
                        pass

                if call.data == 'pay_history_all_admin_add_usd':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'all'

                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[2] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➕ ") + "</b>")
                                        if r[2] != 0:
                                            answer += f"<b><u><i>{r[2]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass

                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_usd)
                    except:
                        pass

                if call.data == 'add_usd_admin' or call.data == 'pay_history_day_admin_add_usd':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'day'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[2] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➕ ") + "</b>")
                                        if r[2] != 0:
                                            answer += f"<b><u><i>{r[2]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_usd)
                    except:
                        pass

                if call.data == 'pay_history_month_admin_add_usd':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'month'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[2] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➕ ") + "</b>")
                                        if r[2] != 0:
                                            answer += f"<b><u><i>{r[2]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_usd)
                    except:
                        pass

                if call.data == 'pay_history_year_admin_add_usd':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'year'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[2] != 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("<b>" + ("➕ ") + "</b>")
                                        if r[2] != 0:
                                            answer += f"<b><u><i>{r[2]} TRX</i></u></b>"
                                        answer += f"\n🕐 {r[5]}  "
                                        answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                        answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                        if r[7] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[7] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_usd)
                    except:
                        pass

                if call.data == 'pay_history_all_not_acces_admin_add_usd':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'year'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_records(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[7] == 0:
                                        if r[2] != 0:
                                            answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                            answer += ("<b>" + ("➕ ") + "</b>")
                                            if r[2] != 0:
                                                answer += f"<b><u><i>{r[2]} TRX</i></u></b>"
                                            answer += f"\n🕐 {r[5]}  "
                                            answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                            answer += (f"📬 Адреса: <code>{r[6]}</code>\n")
                                            if r[7] == 0:
                                                answer += f"<b>❌ Не виконано</b>\n\n"
                                            elif r[7] == 1:
                                                answer += f"<b>✅ Виконано</b>\n\n"
                                            else:
                                                answer += f"<b>💢 Помилка виконання</b>\n\n"
                                        else:
                                            pass
                                    else:
                                        pass
                                if answer != (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n"):
                                    await sleep(0.33)
                                    await call.message.answer(answer, parse_mode='html')
                                else:
                                    pass
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_usd)
                    except:
                        pass

                if call.data == 'pay_admin':
                    markup_admin = types.InlineKeyboardMarkup(row_width=1)
                    del_trx_admin = types.InlineKeyboardButton(f'⬆ Заявки на вивід ({db.BotDB.count_del_trx_admin(0)})', callback_data='del_trx_admin')
                    add_trx_admin = types.InlineKeyboardButton(f'💶 Заявки на поповнення TRX ({db.BotDB.count_add_trx_admin(0)})', callback_data='add_trx_admin')
                    add_usd_admin = types.InlineKeyboardButton(f'💲 Заявки на поповнення USDT ({db.BotDB.count_add_usd_admin(0)})', callback_data='add_usd_admin')
                    say_hi_admin_kb = types.InlineKeyboardButton(f'🗣 Поділитись історією/музикою ({db.BotDB.count_say_hi_admin(0)})', callback_data='say_hi_admin_kb')
                    work_user_admin = types.InlineKeyboardButton(f'🤖 Робота з користувачем', callback_data='work_user_admin')
                    mailing_admin = types.InlineKeyboardButton(f'✍ Розсилка', callback_data='mailing_admin')
                    markup_admin.add(del_trx_admin, add_trx_admin, add_usd_admin, say_hi_admin_kb, mailing_admin, work_user_admin)
                    await bot.send_message(call.message.chat.id, f'👤 Адмін панель:                                                                        ㅤ', reply_markup=markup_admin)

                if call.data == 'work_user_admin':
                    await call.message.edit_text('👷 Який вид робіт буде проходити: ', parse_mode='html', reply_markup=kb.markup_work_admin)

                if call.data == 'work_admin_trx':
                    await call.message.edit_text('🛠 Оберіть операцію: ', parse_mode='html', reply_markup=kb.markup_work_admin_select_trx)

                if call.data == 'work_admin_patreon':
                    await call.message.edit_text('🛠 Оберіть операцію: ', parse_mode='html', reply_markup=kb.markup_work_admin_select_patreon)

                if call.data == 'work_admin_trx_select_trx':
                    await states.work_trx_admin.sum_trx.set()
                    await bot.send_message(call.message.chat.id, f'↘ Оберіть суму що хочете додати із клавіатури або введіть її самі', reply_markup=kb.markup_select_add_trx, parse_mode='html')

                    @dp.message_handler(state=states.work_trx_admin.sum_trx)
                    async def random_number_hun(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['sum_trx'] = float(message.text)
                            betting = data['sum_trx']
                            if betting <= 1000:
                                if betting > 0:
                                    await states.work_trx_admin.next()
                                    await bot.send_message(message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)
                                else:
                                    await bot.send_message(message.chat.id, f'❌ Мінімальна сума поповнення <b><i>1</i></b> TRX ‼', parse_mode='html')
                                    await bot.send_message(message.chat.id, f'❌ Введіть іншу суму поповнення (або можете вийти з гри /cancel):', parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, f'❌ Максимальна сума поповнення <b><i>1000</i></b> TRX ‼', parse_mode='html')
                                await bot.send_message(message.chat.id, f'❌ Введіть іншу суму поповнення (або можете вийти з гри /cancel):', parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_start = await kb.markup_start(message)
                            await bot.send_message(message.chat.id, f'❌ Ви вийшли з режиму поповнення ‼', reply_markup=markup_start, parse_mode='html')
                            await state.finish()

                    @dp.message_handler(state=states.work_trx_admin.user_id)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.work_trx_admin.user_id.set()
                            data['user_id'] = message.text
                            for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.text}"):
                                await message.answer(f'Kористувач <b><i>{data["user_id"]}</i></b>. Його баланс становить - <b><i>{values[0]}</i></b> TRX\n\nПоповнити на {data["sum_trx"]} TRX', parse_mode='html', reply_markup=kb.markup_work_add_trx_admin)
                            await states.work_trx_admin.next()

                    @dp.callback_query_handler(text='work_add_trx_admin', state=states.work_trx_admin.accept)
                    async def start(call: types.callback_query, state: FSMContext):
                        async with state.proxy() as data:
                            try:
                                user_id_text = data['user_id']
                                sum_trx = data['sum_trx']
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx + {sum_trx} WHERE user_id = {user_id_text}")
                                base.commit()
                                for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {user_id_text}"):
                                    await call.message.answer(f'----------------------------------------------\n\n\nБаланс користувача <b><i>{data["user_id"]}</i></b> поповнено на <b><u>{sum_trx}</u></b> TRX\n\n\n\n💳 Його баланс становить - {values[0]} TRX\n\n\n----------------------------------------------', reply_markup=kb.markup_admin, parse_mode='html')
                                    await state.finish()
                            except:
                                await call.message.answer(locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')

                    @dp.callback_query_handler(text='work_add_trx_admin_cancel', state=states.work_trx_admin.accept)
                    async def start(call: types.callback_query, state: FSMContext):
                        await call.message.answer(f"❌ Ви відмінили поповнення ❗", parse_mode='html', reply_markup=kb.markup_admin)
                        await state.finish()

                if call.data == 'work_admin_trx_del_select_trx':
                    await states.work_trx_admin.sum_trx_del.set()
                    await bot.send_message(call.message.chat.id, f'↘ Оберіть суму що хочете зняти з балансу із клавіатури або введіть її самі', reply_markup=kb.markup_select_add_trx, parse_mode='html')

                    @dp.message_handler(state=states.work_trx_admin.sum_trx_del)
                    async def random_number_hun(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['sum_trx_del'] = float(message.text)
                            betting = data['sum_trx_del']
                            if betting <= 1000:
                                if betting > 0:
                                    await states.work_trx_admin.next()
                                    await bot.send_message(message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)
                                else:
                                    await bot.send_message(message.chat.id, f'❌ Мінімальна сума зняття з балансу <b><i>1</i></b> TRX ‼', parse_mode='html')
                                    await bot.send_message(message.chat.id, f'❌ Введіть іншу суму зняття з балансу (або можете вийти з гри /cancel):', parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, f'❌ Максимальна сума зняття з балансу <b><i>1000</i></b> TRX ‼', parse_mode='html')
                                await bot.send_message(message.chat.id, f'❌ Введіть іншу суму зняття з балансу (або можете вийти з гри /cancel):', parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_start = await kb.markup_start(message)
                            await bot.send_message(message.chat.id, f'❌ Ви вийшли з режиму зняття з балансу ‼', reply_markup=markup_start, parse_mode='html')
                            await state.finish()

                    @dp.message_handler(state=states.work_trx_admin.user_id_del)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.work_trx_admin.user_id_del.set()
                            data['user_id_del'] = message.text
                            for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.text}"):
                                await message.answer(f'Kористувач <b><i>{data["user_id_del"]}</i></b>. Його баланс становить - <b><i>{values[0]}</i></b> TRX\n\nЗняти з балансу на {data["sum_trx_del"]} TRX', parse_mode='html', reply_markup=kb.markup_work_add_trx_admin)
                            await states.work_trx_admin.next()

                    @dp.callback_query_handler(text='work_add_trx_admin', state=states.work_trx_admin.accept_del)
                    async def start(call: types.callback_query, state: FSMContext):
                        async with state.proxy() as data:
                            try:
                                user_id_text = data['user_id_del']
                                sum_trx_del = data['sum_trx_del']
                                cur.execute(f"UPDATE users SET bal_trx = bal_trx - {sum_trx_del} WHERE user_id = {user_id_text}")
                                base.commit()
                                for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {user_id_text}"):
                                    await call.message.answer(f'----------------------------------------------\n\n\nБаланс користувача <b><i>{data["user_id_del"]}</i></b> знято з балансу на <b><u>{sum_trx_del}</u></b> TRX\n\n\n\n💳 Його баланс становить - {values[0]} TRX\n\n\n----------------------------------------------', reply_markup=kb.markup_admin, parse_mode='html')
                                    await state.finish()
                            except:
                                await call.message.answer(locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')

                    @dp.callback_query_handler(text='work_add_trx_admin_cancel', state=states.work_trx_admin.accept_del)
                    async def start(call: types.callback_query, state: FSMContext):
                        await call.message.answer(f"❌ Ви відмінили зняття з балансу ❗", parse_mode='html', reply_markup=kb.markup_admin)
                        await state.finish()

                if call.data == 'work_admin_usd':
                    await call.message.edit_text('🛠 Оберіть операцію: ', parse_mode='html', reply_markup=kb.markup_work_admin_select_usd)

                if call.data == 'work_admin_trx_select_usd':
                    await states.work_usd_admin.sum_trx.set()
                    await bot.send_message(call.message.chat.id, f'↘ Оберіть суму що хочете додати із клавіатури або введіть її самі', reply_markup=kb.markup_select_add_usdt, parse_mode='html')

                    @dp.message_handler(state=states.work_usd_admin.sum_trx)
                    async def random_number_hun(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['sum_trx'] = float(message.text)
                            betting = data['sum_trx']
                            if betting <= 100000:
                                if betting > 0:
                                    await states.work_usd_admin.next()
                                    await bot.send_message(message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)
                                else:
                                    await bot.send_message(message.chat.id, f'❌ Мінімальна сума поповнення <b><i>1</i></b> USDT ‼', parse_mode='html')
                                    await bot.send_message(message.chat.id, f'❌ Введіть іншу суму поповнення (або можете вийти з гри /cancel):', parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, f'❌ Максимальна сума поповнення <b><i>100000</i></b> USDT ‼', parse_mode='html')
                                await bot.send_message(message.chat.id, f'❌ Введіть іншу суму поповнення (або можете вийти з гри /cancel):', parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_start = await kb.markup_start(message)
                            await bot.send_message(message.chat.id, f'❌ Ви вийшли з режиму поповнення ‼', reply_markup=markup_start, parse_mode='html')
                            await state.finish()

                    @dp.message_handler(state=states.work_usd_admin.user_id)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.work_usd_admin.user_id.set()
                            data['user_id'] = message.text
                            for values in cur.execute(f"SELECT bal_dol FROM users WHERE user_id = {message.text}"):
                                await message.answer(f'Kористувач <b><i>{data["user_id"]}</i></b>. Його баланс становить - <b><i>{values[0]}</i></b> USDT\n\nПоповнити на {data["sum_trx"]} USDT', parse_mode='html', reply_markup=kb.markup_work_add_trx_admin)
                            await states.work_usd_admin.next()

                    @dp.callback_query_handler(text='work_add_trx_admin', state=states.work_usd_admin.accept)
                    async def start(call: types.callback_query, state: FSMContext):
                        async with state.proxy() as data:
                            try:
                                user_id_text = data['user_id']
                                sum_trx = data['sum_trx']
                                cur.execute(f"UPDATE users SET bal_dol = bal_dol + {sum_trx} WHERE user_id = {user_id_text}")
                                base.commit()
                                for values in cur.execute(f"SELECT bal_dol FROM users WHERE user_id = {user_id_text}"):
                                    await call.message.answer(f'----------------------------------------------\n\n\nБаланс користувача <b><i>{data["user_id"]}</i></b> поповнено на <b><u>{sum_trx}</u></b> USDT\n\n\n\n💳 Його баланс становить - {values[0]} USDT\n\n\n----------------------------------------------', reply_markup=kb.markup_admin, parse_mode='html')
                                    await state.finish()
                            except:
                                await call.message.answer(locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')

                    @dp.callback_query_handler(text='work_add_trx_admin_cancel', state=states.work_usd_admin.accept)
                    async def start(call: types.callback_query, state: FSMContext):
                        await call.message.answer(f"❌ Ви відмінили поповнення ❗", parse_mode='html', reply_markup=kb.markup_admin)
                        await state.finish()

                if call.data == 'work_admin_usd_del_select_usd':
                    await states.work_usd_admin.sum_trx_del.set()
                    await bot.send_message(call.message.chat.id, f'↘ Оберіть суму що хочете зняти з балансу із клавіатури або введіть її самі', reply_markup=kb.markup_select_add_usdt, parse_mode='html')

                    @dp.message_handler(state=states.work_usd_admin.sum_trx_del)
                    async def random_number_hun(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['sum_trx_del'] = float(message.text)
                            betting = data['sum_trx_del']
                            if betting <= 10000:
                                if betting > 0:
                                    await states.work_usd_admin.next()
                                    await bot.send_message(message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)
                                else:
                                    await bot.send_message(message.chat.id, f'❌ Мінімальна сума зняття з балансу <b><i>1</i></b> USDT ‼', parse_mode='html')
                                    await bot.send_message(message.chat.id, f'❌ Введіть іншу суму зняття з балансу (або можете вийти з гри /cancel):', parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, f'❌ Максимальна сума зняття з балансу <b><i>10000</i></b> USDT ‼', parse_mode='html')
                                await bot.send_message(message.chat.id, f'❌ Введіть іншу суму зняття з балансу (або можете вийти з гри /cancel):', parse_mode='html')
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_start = await kb.markup_start(message)
                            await bot.send_message(message.chat.id, f'❌ Ви вийшли з режиму зняття з балансу ‼', reply_markup=markup_start, parse_mode='html')
                            await state.finish()

                    @dp.message_handler(state=states.work_usd_admin.user_id_del)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.work_usd_admin.user_id_del.set()
                            data['user_id_del'] = message.text
                            for values in cur.execute(f"SELECT bal_dol FROM users WHERE user_id = {message.text}"):
                                await message.answer(f'Kористувач <b><i>{data["user_id_del"]}</i></b>. Його баланс становить - <b><i>{values[0]}</i></b> USDT\n\nЗняти з балансу на {data["sum_trx_del"]} USDT', parse_mode='html', reply_markup=kb.markup_work_add_trx_admin)
                            await states.work_usd_admin.next()

                    @dp.callback_query_handler(text='work_add_trx_admin', state=states.work_usd_admin.accept_del)
                    async def start(call: types.callback_query, state: FSMContext):
                        async with state.proxy() as data:
                            try:
                                user_id_text = data['user_id_del']
                                sum_trx_del = data['sum_trx_del']
                                cur.execute(f"UPDATE users SET bal_dol = bal_dol - {sum_trx_del} WHERE user_id = {user_id_text}")
                                base.commit()
                                for values in cur.execute(f"SELECT bal_dol FROM users WHERE user_id = {user_id_text}"):
                                    await call.message.answer(f'----------------------------------------------\n\n\nБаланс користувача <b><i>{data["user_id_del"]}</i></b> знято з балансу <b><u>{sum_trx_del}</u></b> USDT\n\n\n\n💳 Його баланс становить - {values[0]} USDT\n\n\n----------------------------------------------', reply_markup=kb.markup_admin, parse_mode='html')
                                    await state.finish()
                            except:
                                await call.message.answer(locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')

                    @dp.callback_query_handler(text='work_add_trx_admin_cancel', state=states.work_usd_admin.accept_del)
                    async def start(call: types.callback_query, state: FSMContext):
                        await call.message.answer(f"❌ Ви відмінили зняття з балансу ❗", parse_mode='html', reply_markup=kb.markup_admin)
                        await state.finish()

                if call.data == 'work_admin_ban':
                    await call.message.edit_text('🛠 Оберіть операцію: ', parse_mode='html', reply_markup=kb.markup_work_admin_select_ban)

                if call.data == 'work_admin_ban_select_ban':
                    await states.work_ban.ban.set()
                    await bot.send_message(call.message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)

                    @dp.message_handler(state=states.work_ban.ban)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.work_ban.ban.set()
                            data['user_id'] = message.text
                            for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.text}"):
                                await message.answer(f'ℹ Kористувач <b><i>{data["user_id"]}</i></b>. Його баланс становить - <b><i>{values[0]}</i></b> TRX\n\n<b>👎 Тепер в БАНІ !</b>', parse_mode='html', reply_markup=kb.markup_admin)
                            cur.execute(f"UPDATE users SET ban = 1 WHERE user_id = {message.text}")
                            base.commit()
                            await state.finish()

                if call.data == 'work_admin_unban_select_ban':
                    await states.work_ban.unban.set()
                    await bot.send_message(call.message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)

                    @dp.message_handler(state=states.work_ban.unban)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.work_ban.unban.set()
                            data['user_id'] = message.text
                            for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.text}"):
                                await message.answer(f'ℹ Kористувач <b><i>{data["user_id"]}</i></b>. Його баланс становить - <b><i>{values[0]}</i></b> TRX\n\n<b>👍Тепер РОЗБАНЕНИЙ !</b>', parse_mode='html', reply_markup=kb.markup_admin)
                            cur.execute(f"UPDATE users SET ban = 0 WHERE user_id = {message.text}")
                            base.commit()
                            await state.finish()

                if call.data == 'work_admin_ban_list':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'all'
                        users = await db.get_users_ban()
                        answer = (f"📖 Забанені за <b>{within_als[within][-1]}</b>.\n\n")
                        for user in users:
                            records = BotDB.get_ban_list(user[0], within)
                            if (len(records)):
                                for r in records:
                                    answer += (f"➖ <b><i>USER_ID</i> = <code>{user[0]}</code></b>. Баланс = {r[5]} TRX, {r[4]} USDT\n")
                                    answer += f"🕐 Дата реєстрації аккаунта: {r[6]}\n\n\n"
                                await sleep(0.33)
                            else:
                                pass
                        await call.message.answer(answer, parse_mode='html')
                        await call.message.answer('Адмін панель:', parse_mode='html', reply_markup=kb.markup_admin)
                    except:
                        pass

                if call.data == 'work_admin_select_patreon':
                    await states.work_patreon.patron.set()
                    await bot.send_message(call.message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)

                    @dp.message_handler(state=states.work_patreon.patron)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.work_patreon.patron.set()
                            data['user_id'] = message.text
                            for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.text}"):
                                await message.answer(f'ℹ Kористувач <b><i>{data["user_id"]}</i></b>. Його баланс становить - <b><i>{values[0]}</i></b> TRX\n\n<b>👎 Тепер наш ПАТРОН !</b>', parse_mode='html', reply_markup=kb.markup_admin)
                            cur.execute(f"UPDATE users SET patron = 1 WHERE user_id = {message.text}")
                            base.commit()
                            await state.finish()

                if call.data == 'work_admin_del_select_patreon':
                    await states.work_patreon.unpatron.set()
                    await bot.send_message(call.message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)

                    @dp.message_handler(state=states.work_patreon.unpatron)
                    async def answer(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            await states.work_patreon.unpatron.set()
                            data['user_id'] = message.text
                            for values in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.text}"):
                                await message.answer(f'ℹ Kористувач <b><i>{data["user_id"]}</i></b>. Його баланс становить - <b><i>{values[0]}</i></b> TRX\n\n<b>👎 Тепер НЕ Патрон !</b>', parse_mode='html', reply_markup=kb.markup_admin)
                            cur.execute(f"UPDATE users SET patron = 0 WHERE user_id = {message.text}")
                            base.commit()
                            await state.finish()

                if call.data == 'work_admin_patreon_list':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'all'
                        users = await db.get_users_patron()
                        answer = (f"📖 Патрони за <b>{within_als[within][-1]}</b>.\n\n")
                        for user in users:
                            records = BotDB.get_patron_list(user[0], within)
                            if (len(records)):
                                for r in records:
                                    answer += (f"➖ <b><i>USER_ID</i> = <code>{user[0]}</code></b>. Баланс = {r[5]} TRX, {r[4]} USDT\n")
                                    answer += f"🕐 Дата реєстрації аккаунта: {r[6]}\n\n\n"
                                await sleep(0.33)
                            else:
                                pass
                        await call.message.answer(answer, parse_mode='html')
                        await call.message.answer('Адмін панель:', parse_mode='html', reply_markup=kb.markup_admin)
                    except:
                        pass

                if call.data == 'say_hi_admin_kb_all_admin':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'all'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_say_hi(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория розсилок користувачів за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[3] == 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("➕ " if r[3] != 0 else "➖ TEXT\n\n")
                                        answer += f"<b><u><i>{r[2]}\n\n</i></u></b>"
                                        answer += f"\n🕐 {r[4]}  "
                                        if r[3] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[3] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_say_hi_admin_kb)
                    except:
                        pass

                if call.data == 'say_hi_admin_kb_year_admin':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'year'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_say_hi(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория розсилок користувачів за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[3] == 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("➕ " if r[3] != 0 else "➖ TEXT\n\n")
                                        answer += f"<b><u><i>{r[2]}\n\n</i></u></b>"
                                        answer += f"\n🕐 {r[4]}  "
                                        if r[3] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[3] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_say_hi_admin_kb)
                    except:
                        pass

                if call.data == 'say_hi_admin_kb_month_admin':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'month'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_say_hi(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория розсилок користувачів за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[3] == 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("➕ " if r[3] != 0 else "➖ TEXT\n\n")
                                        answer += f"<b><u><i>{r[2]}\n\n</i></u></b>"
                                        answer += f"\n🕐 {r[4]}  "
                                        if r[3] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[3] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_say_hi_admin_kb)
                    except:
                        pass

                if call.data == 'say_hi_admin_kb' or call.data == 'say_hi_admin_kb_day_admin':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'day'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_say_hi(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория розсилок користувачів за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[3] == 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("➕ " if r[3] != 0 else "➖ TEXT\n\n")
                                        answer += f"<b><u><i>{r[2]}\n\n</i></u></b>"
                                        answer += f"\n🕐 {r[4]}  "
                                        if r[3] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[3] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                await sleep(0.33)
                                await call.message.answer(answer, parse_mode='html')
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_say_hi_admin_kb)
                    except:
                        pass

                if call.data == 'say_hi_all_not_acces_admin':
                    try:
                        within_als = {
                            "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                            "month": ('month', 'МІСЯЦЬ'),
                            "year": ('year', 'РІК'),
                            "all": ('all', 'ВЕСЬ ЧАС'),
                        }
                        within = 'all'
                        users = await db.get_users()
                        for user in users:
                            records = BotDB.get_say_hi(user[0], within)
                            if (len(records)):
                                answer = (f"📖 Істория розсилок користувачів за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n")
                                for r in records:
                                    if r[3] == 0:
                                        answer += (f"<b><i>ID</i> = <code>{r[0]}</code></b>\n\n")
                                        answer += ("➕ " if r[3] != 0 else "➖ TEXT\n\n")
                                        answer += f"<b><u><i>{r[2]}\n\n</i></u></b>"
                                        answer += f"\n🕐 {r[4]}  "
                                        if r[3] == 0:
                                            answer += f"<b>❌ Не виконано</b>\n\n"
                                        elif r[3] == 1:
                                            answer += f"<b>✅ Виконано</b>\n\n"
                                        else:
                                            answer += f"<b>💢 Помилка виконання</b>\n\n"
                                    else:
                                        pass
                                if answer != (f"📖 Істория розсилок користувачів за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user[0]}</code></b>\n"):
                                    await sleep(0.33)
                                    await call.message.answer(answer, parse_mode='html')
                                else:
                                    pass
                            else:
                                pass
                        await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_say_hi_admin_kb)
                    except:
                        pass

                if call.data == 'say_hi_admin_kb_do_acces':
                    await states.say_hi_admin_kb_do_acces.user_id.set()
                    await bot.send_message(call.message.chat.id, f'🔑 Введіть ID запису (id)', reply_markup=kb.cancel_num, parse_mode='html')

                    @dp.message_handler(state=states.say_hi_admin_kb_do_acces.user_id)
                    async def acces_say_hi_admin(message: types.Message, state: FSMContext):
                        try:
                            async with state.proxy() as data:
                                data['user_id'] = int(message.text)
                            record_id = data['user_id']
                            cur.execute(f"UPDATE say_hi SET acces = 1 WHERE id = {record_id}")
                            base.commit()
                            for values in cur.execute(f"SELECT text_message, user_id FROM say_hi WHERE id = {record_id} AND acces = 1"):
                                await bot.send_message(message.chat.id, f'✅ Повідомлення: \n{values[0]}\n\n👤 Користувача: \n{values[1]}\n\n🔑 Запис: {record_id}\n\n ВИКОНАНО', parse_mode='html', reply_markup=kb.markup_admin)
                            await state.finish()
                        except:
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(message.chat.id)}'], parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await bot.send_message(message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                            await state.finish()

                if call.data == 'pay_admin_kb_do_acces_add_usd':
                    await states.pay_history_admin_add_usd.user_id.set()
                    await bot.send_message(call.message.chat.id, f'🔑 Введіть ID користувача (user_id)', reply_markup=kb.cancel_num, parse_mode='html')

                    @dp.message_handler(state=states.pay_history_admin_add_usd.user_id)
                    async def acces_say_hi_admin(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            data['user_id'] = int(message.text)
                            await bot.send_message(call.message.chat.id, f'Оберіть операцію', parse_mode='html', reply_markup=kb.markup_cancel)
                        await bot.send_message(call.message.chat.id, f'Оберіть операцію', parse_mode='html', reply_markup=kb.markup_pay_admin_kb_do_acces_add_usd)
                        await states.pay_history_admin_add_usd.next()

                    @dp.callback_query_handler(state=states.pay_history_admin_add_usd.select)
                    async def answer(call: types.CallbackQuery, state: FSMContext):
                        if call.data == 'pay_admin_kb_do_acces_add_usd_set_null':
                            try:
                                async with state.proxy() as data:
                                    record_id = data['user_id']
                                cur.execute(f"UPDATE paymants SET acces = 0 WHERE id = {record_id}")
                                base.commit()
                                for value in cur.execute(f"SELECT user_id FROM paymants WHERE id = {record_id}"):
                                    for values in cur.execute(f"SELECT bal_dol, user_id FROM users WHERE user_id = {value[0]}"):
                                        await bot.send_message(call.message.chat.id, f'❌ Баланс USDT: \n{values[0]} USDT\n\n👤 Користувача: \n{values[1]}\n\n🔑 Запис: {record_id}\n\n ВІДМІНЕНО', parse_mode='html', reply_markup=kb.markup_admin)
                                await state.finish()
                            except:
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                markup_games = await kb.markup_games(call.message)
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                                await state.finish()
                        elif call.data == 'pay_admin_kb_do_acces_add_usd_set_one':
                            try:
                                async with state.proxy() as data:
                                    record_id = data['user_id']
                                cur.execute(f"UPDATE paymants SET acces = 1 WHERE id = {record_id}")
                                base.commit()
                                for value in cur.execute(f"SELECT user_id FROM paymants WHERE id = {record_id}"):
                                    for values in cur.execute(f"SELECT bal_dol, user_id FROM users WHERE user_id = {value[0]}"):
                                        await bot.send_message(call.message.chat.id, f'✅ Баланс USDT: \n{values[0]} USDT\n\n👤 Користувача: \n{values[1]}\n\n🔑 Запис: {record_id}\n\n ВИКОНАНО', parse_mode='html', reply_markup=kb.markup_admin)
                                await state.finish()
                            except:
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                markup_games = await kb.markup_games(call.message)
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                                await state.finish()
                        elif call.data == 'pay_admin_kb_do_acces_add_usd_set_two':
                            try:
                                async with state.proxy() as data:
                                    record_id = data['user_id']
                                cur.execute(f"UPDATE paymants SET acces = 2 WHERE id = {record_id}")
                                base.commit()
                                for value in cur.execute(f"SELECT user_id FROM paymants WHERE id = {record_id}"):
                                   for values in cur.execute(f"SELECT bal_dol, user_id FROM users WHERE user_id = {value[0]}"):
                                        await bot.send_message(call.message.chat.id, f'💢 Баланс USDT: \n{values[0]} USDT\n\n👤 Користувача: \n{values[1]}\n\n🔑 Запис: {record_id}\n\n ПОСТАВЛЕНА ПОМИЛКА', parse_mode='html', reply_markup=kb.markup_admin)
                                await state.finish()
                            except:
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                markup_games = await kb.markup_games(call.message)
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                                await state.finish()

                if call.data == 'pay_admin_kb_do_acces':
                    await states.pay_admin_kb_do_acces.user_id.set()
                    await bot.send_message(call.message.chat.id, f'🔑 Введіть ID запису (id)', reply_markup=kb.cancel_num, parse_mode='html')

                    @dp.message_handler(state=states.pay_admin_kb_do_acces.user_id)
                    async def acces_say_hi_admin(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            data['user_id'] = int(message.text)
                            await bot.send_message(call.message.chat.id, f'Оберіть операцію', parse_mode='html', reply_markup=kb.markup_cancel)
                        await bot.send_message(call.message.chat.id, f'Оберіть операцію', parse_mode='html', reply_markup=kb.markup_pay_admin_kb_do_acces_del_trx)
                        await states.pay_admin_kb_do_acces.next()

                    @dp.callback_query_handler(state=states.pay_admin_kb_do_acces.select)
                    async def answer(call: types.CallbackQuery, state: FSMContext):
                        if call.data == 'pay_admin_kb_do_acces_del_trx_set_null':
                            try:
                                async with state.proxy() as data:
                                    record_id = data['user_id']
                                cur.execute(f"UPDATE paymants SET acces = 0 WHERE id = {record_id}")
                                base.commit()
                                for value in cur.execute(f"SELECT user_id FROM paymants WHERE id = {record_id}"):
                                    for values in cur.execute(f"SELECT bal_trx, user_id FROM users WHERE user_id = {value[0]}"):
                                        await bot.send_message(call.message.chat.id, f'❌ Баланс TRX: \n{values[0]} TRX\n\n👤 Користувача: \n{values[1]}\n\n🔑 Запис: {record_id}\n\n ВІДМІНЕНО', parse_mode='html', reply_markup=kb.markup_admin)
                                await state.finish()
                            except:
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                markup_games = await kb.markup_games(call.message)
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                                await state.finish()
                        elif call.data == 'pay_admin_kb_do_acces_del_trx_set_one':
                            try:
                                async with state.proxy() as data:
                                    record_id = data['user_id']
                                cur.execute(f"UPDATE paymants SET acces = 1 WHERE id = {record_id}")
                                base.commit()
                                for value in cur.execute(f"SELECT user_id FROM paymants WHERE id = {record_id}"):
                                    for values in cur.execute(f"SELECT bal_trx, user_id FROM users WHERE user_id = {value[0]}"):
                                        await bot.send_message(call.message.chat.id, f'✅ Баланс TRX: \n{values[0]} TRX\n\n👤 Користувача: \n{values[1]}\n\n🔑 Запис: {record_id}\n\n ВИКОНАНО', parse_mode='html', reply_markup=kb.markup_admin)
                                await state.finish()
                            except:
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                markup_games = await kb.markup_games(call.message)
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                                await state.finish()
                        elif call.data == 'pay_admin_kb_do_acces_del_trx_set_two':
                            try:
                                async with state.proxy() as data:
                                    record_id = data['user_id']
                                cur.execute(f"UPDATE paymants SET acces = 2 WHERE id = {record_id}")
                                base.commit()
                                for value in cur.execute(f"SELECT user_id FROM paymants WHERE id = {record_id}"):
                                    for values in cur.execute(f"SELECT bal_trx, user_id FROM users WHERE user_id = {value[0]}"):
                                        await bot.send_message(call.message.chat.id, f'💢 Баланс TRX: \n{values[0]} TRX\n\n👤 Користувача: \n{values[1]}\n\n🔑 Запис: {record_id}\n\n ПОСТАВЛЕНА ПОМИЛКА', parse_mode='html', reply_markup=kb.markup_admin)
                                await state.finish()
                            except:
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                markup_games = await kb.markup_games(call.message)
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                                await state.finish()

                if call.data == 'pay_admin_kb_do_acces_add_trx':
                    await states.pay_admin_kb_do_acces_add_trx.user_id.set()
                    await bot.send_message(call.message.chat.id, f'🔑 Введіть ID запису (id)', reply_markup=kb.cancel_num, parse_mode='html')

                    @dp.message_handler(state=states.pay_admin_kb_do_acces_add_trx.user_id)
                    async def acces_say_hi_admin(message: types.Message, state: FSMContext):
                        async with state.proxy() as data:
                            data['user_id'] = int(message.text)
                            await bot.send_message(call.message.chat.id, f'Оберіть операцію', parse_mode='html', reply_markup=kb.markup_cancel)
                        await bot.send_message(call.message.chat.id, f'Оберіть операцію', parse_mode='html', reply_markup=kb.markup_pay_admin_kb_do_acces_add_trx)
                        await states.pay_admin_kb_do_acces_add_trx.next()

                    @dp.callback_query_handler(state=states.pay_admin_kb_do_acces_add_trx.select)
                    async def answer(call: types.CallbackQuery, state: FSMContext):
                        if call.data == 'pay_admin_kb_do_acces_add_trx_set_null':
                            try:
                                async with state.proxy() as data:
                                    record_id = data['user_id']
                                cur.execute(f"UPDATE paymants SET acces = 0 WHERE id = {record_id}")
                                base.commit()
                                for value in cur.execute(f"SELECT user_id FROM paymants WHERE id = {record_id}"):
                                    for values in cur.execute(f"SELECT bal_trx, user_id FROM users WHERE user_id = {value[0]}"):
                                        await bot.send_message(call.message.chat.id, f'❌ Баланс TRX: \n{values[0]} TRX\n\n👤 Користувача: \n{values[1]}\n\n🔑 Запис: {record_id}\n\n ВІДМІНЕНО', parse_mode='html', reply_markup=kb.markup_admin)
                                await state.finish()
                            except:
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                markup_games = await kb.markup_games(call.message)
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                                await state.finish()
                        elif call.data == 'pay_admin_kb_do_acces_add_trx_set_one':
                            try:
                                async with state.proxy() as data:
                                    record_id = data['user_id']
                                cur.execute(f"UPDATE paymants SET acces = 1 WHERE id = {record_id}")
                                base.commit()
                                for value in cur.execute(f"SELECT user_id FROM paymants WHERE id = {record_id}"):
                                    for values in cur.execute(f"SELECT bal_trx, user_id FROM users WHERE user_id = {value[0]}"):
                                        await bot.send_message(call.message.chat.id, f'✅ Баланс TRX: \n{values[0]} TRX\n\n👤 Користувача: \n{values[1]}\n\n🔑 Запис: {record_id}\n\n ВИКОНАНО', parse_mode='html', reply_markup=kb.markup_admin)
                                await state.finish()
                            except:
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                markup_games = await kb.markup_games(call.message)
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                                await state.finish()
                        elif call.data == 'pay_admin_kb_do_acces_add_trx_set_two':
                            try:
                                async with state.proxy() as data:
                                    record_id = data['user_id']
                                cur.execute(f"UPDATE paymants SET acces = 2 WHERE id = {record_id}")
                                base.commit()
                                for value in cur.execute(f"SELECT user_id FROM paymants WHERE id = {record_id}"):
                                    for values in cur.execute(f"SELECT bal_trx, user_id FROM users WHERE user_id = {value[0]}"):
                                        await bot.send_message(call.message.chat.id, f'💢 Баланс TRX: \n{values[0]} TRX\n\n👤 Користувача: \n{values[1]}\n\n🔑 Запис: {record_id}\n\n ПОСТАВЛЕНА ПОМИЛКА', parse_mode='html', reply_markup=kb.markup_admin)
                                await state.finish()
                            except:
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_error_num_{BotDB.user_language(call.message.chat.id)}'], parse_mode='html')
                                markup_games = await kb.markup_games(call.message)
                                await bot.send_message(call.message.chat.id, locales.for_all_games[f'for_all_games_exit_game_{BotDB.user_language(call.message.chat.id)}'], reply_markup=markup_games, parse_mode='html')
                                await state.finish()
        else:
            await call.message.answer(locales.ban[f'ban_{BotDB.user_language(call.message.chat.id)}'], parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

    await call.answer()