import db
from aiogram.dispatcher import FSMContext

import locales
from dispatcher import dp, bot
from aiogram import types
import keyboards as kb
from .states import pay_operation
import sqlite3


base = sqlite3.connect('bot_db.sqlite3')
cur = base.cursor()

@dp.message_handler(state=pay_operation.del_trx)
async def get_sum(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['del_trx'] = float(message.text)
            for value in cur.execute(f"SELECT bal_trx FROM users WHERE user_id = {message.from_user.id}"):
                if (data['del_trx'] <= value[0]):
                    if(data['del_trx'] >= 100):
                        await pay_operation.next()
                        for value_wallet in cur.execute(f"SELECT wallet_trx FROM users WHERE user_id = {message.from_user.id}"):
                            if value_wallet[0] == '0':
                                await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_type_adress_trx_{db.BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_cancel, parse_mode='html')
                            else:
                                markup_save_wallet_trx = types.ReplyKeyboardMarkup(resize_keyboard=True ,row_width=1)
                                save_wallet_trx = types.KeyboardButton(f'{value_wallet[0]}')
                                save_wallet_trx_cancel = types.KeyboardButton(f'/cancel')
                                markup_save_wallet_trx.add(save_wallet_trx, save_wallet_trx_cancel)
                                await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_type_adress_trx_save_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_save_wallet_trx, parse_mode='html')
                    else:
                        markup_start = await kb.markup_start(message)
                        await bot.send_message(message.chat.id, locales.pay_operation[f'pay_operation_min_del_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_start, parse_mode='html')
                        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_cancel_{db.BotDB.user_language(message.chat.id)}'], parse_mode='html')
                        await state.finish()
                else:
                    markup_start = await kb.markup_start(message)
                    await bot.send_message(message.chat.id, locales.pay_operation[f'pay_operation_no_money_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_start, parse_mode='html')
                    await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_cancel_{db.BotDB.user_language(message.chat.id)}'], parse_mode='html')
                    await state.finish()
    except:
        markup_start = await kb.markup_start(message)
        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_num_error_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_start, parse_mode='html')
        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_cancel_{db.BotDB.user_language(message.chat.id)}'], parse_mode='html')
        await state.finish()

@dp.message_handler(state=pay_operation.add_trx)
async def get_sum_trx(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['add_trx'] = float(message.text)
            if (data['add_trx'] >= 100):
                await pay_operation.next()
                for value_wallet in cur.execute(f"SELECT wallet_trx FROM users WHERE user_id = {message.from_user.id}"):
                    if value_wallet[0] == '0':
                        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_type_adress_trx_{db.BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_cancel, parse_mode='html')
                    else:
                        markup_save_wallet_trx = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                        save_wallet_trx = types.KeyboardButton(f'{value_wallet[0]}')
                        save_wallet_trx_cancel = types.KeyboardButton(f'/cancel')
                        markup_save_wallet_trx.add(save_wallet_trx, save_wallet_trx_cancel)
                        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_type_adress_trx_save_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_save_wallet_trx, parse_mode='html')
            else:
                markup_start = await kb.markup_start(message)
                await bot.send_message(message.chat.id, locales.pay_operation[f'pay_operation_min_add_trx_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_start, parse_mode='html')
                await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_cancel_{db.BotDB.user_language(message.chat.id)}'], parse_mode='html')
                await state.finish()
    except:
        markup_start = await kb.markup_start(message)
        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_num_error_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_start, parse_mode='html')
        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_cancel_{db.BotDB.user_language(message.chat.id)}'], parse_mode='html')
        await state.finish()


@dp.message_handler(state=pay_operation.add_usd)
async def get_sum_trx(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['add_usd'] = float(message.text)
            if (data['add_usd'] >= 10):
                await pay_operation.next()
                for value_wallet in cur.execute(f"SELECT wallet_trx, wallet_usdt FROM users WHERE user_id = {message.from_user.id}"):
                    if value_wallet[1] == '0':
                        await bot.send_message(message.chat.id, locales.pay_operation[f'pay_operation_wallet_usd_{db.BotDB.user_language(message.chat.id)}'], reply_markup=kb.markup_cancel, parse_mode='html')
                    else:
                        markup_save_wallet_usdt = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                        save_wallet_usdt = types.KeyboardButton(f'{value_wallet[1]}')
                        save_wallet_trx_cancel = types.KeyboardButton(f'/cancel')
                        markup_save_wallet_usdt.add(save_wallet_usdt, save_wallet_trx_cancel)
                        await bot.send_message(message.chat.id, locales.pay_operation[f'pay_operation_wallet_usd_save_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_save_wallet_usdt, parse_mode='html')
            else:
                markup_start = await kb.markup_start(message)
                await bot.send_message(message.chat.id, locales.pay_operation[f'pay_operation_min_add_usd_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_start, parse_mode='html')
                await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_cancel_{db.BotDB.user_language(message.chat.id)}'], parse_mode='html')
                await state.finish()
    except:
        markup_start = await kb.markup_start(message)
        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_num_error_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_start, parse_mode='html')
        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_cancel_{db.BotDB.user_language(message.chat.id)}'], parse_mode='html')
        await state.finish()


@dp.message_handler(state=pay_operation.del_trx_get_adress)
async def get_adress_sum(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            ID = message.from_user.id
            data['id_del_trx'] = ID
            data['del_trx_get_adress'] = message.text
            a = data['del_trx_get_adress']
            b = data['del_trx']

        await db.add_del_trx(state)
        if message.text != '/cancel':
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, locales.pay_operation[f'pay_operation_acc_del_trx_{db.BotDB.user_language(message.chat.id)}'].format(b, a), reply_markup=markup_start, parse_mode='html')
            markup_succes = await kb.markup_succes(message)
            await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_acc_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_succes, parse_mode='html')
            cur.execute(f"UPDATE users SET bal_trx = bal_trx - {b} WHERE `user_id` = ?", (message.from_user.id,))
            cur.execute(f"UPDATE users SET wallet_trx = '{a}' WHERE `user_id` = ?", (message.from_user.id,))
            base.commit()
            await state.finish()
        else:
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, locales.pay_operation[f'pay_operation_cancel_del_trx_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_start, parse_mode='html')
            await state.finish()
        cur.execute(f"DELETE FROM paymants WHERE adress = '/cancel'")
        base.commit()
    except:
        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_error_{db.BotDB.user_language(message.chat.id)}'], parse_mode='html')
        await state.finish()


@dp.message_handler(state=pay_operation.add_trx_get_adress)
async def get_adress_sum_(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            ID = message.from_user.id
            data['id_del_trx'] = ID
            data['add_trx_get_adress'] = message.text
            a = data['add_trx_get_adress']
            b = data['add_trx']

        await db.add_add_trx(state)
        if message.text != '/cancel':
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, locales.pay_operation[f'pay_operation_acc_add_trx_{db.BotDB.user_language(message.chat.id)}'].format(b, a), reply_markup=markup_start, parse_mode='html')
            markup_succes = await kb.markup_succes(message)
            await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_acc_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_succes, parse_mode='html')
            cur.execute(f"UPDATE users SET wallet_trx = '{a}' WHERE `user_id` = ?", (message.from_user.id,))
            base.commit()
            await state.finish()
        else:
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_cancel_add_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_start, parse_mode='html')
            await state.finish()
        cur.execute(f"DELETE FROM paymants WHERE adress = '/cancel'")
        base.commit()
    except:
        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_error_{db.BotDB.user_language(message.chat.id)}'], parse_mode='html')
        await state.finish()


@dp.message_handler(state=pay_operation.add_usd_get_adress)
async def get_adress_sum__(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            ID = message.from_user.id
            data['id_del_trx'] = ID
            data['add_usd_get_adress'] = message.text
            a = data['add_usd_get_adress']
            b = data['add_usd']

        await db.add_add_usd(state)
        if message.text != '/cancel':
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, locales.pay_operation[f'pay_operation_acc_add_usd_{db.BotDB.user_language(message.chat.id)}'].format(b, a), reply_markup=markup_start, parse_mode='html')
            markup_succes = await kb.markup_succes(message)
            await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_acc_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_succes, parse_mode='html')
            cur.execute(f"UPDATE users SET wallet_usdt = '{a}' WHERE `user_id` = ?", (message.from_user.id,))
            base.commit()
            await state.finish()
        else:
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_cancel_add_{db.BotDB.user_language(message.chat.id)}'], reply_markup=markup_start, parse_mode='html')
            await state.finish()
        cur.execute(f"DELETE FROM paymants WHERE adress = '/cancel'")
        base.commit()
    except:
        await bot.send_message(message.chat.id, locales.for_all_pay_operation[f'for_all_pay_operation_error_{db.BotDB.user_language(message.chat.id)}'], parse_mode='html')
        await state.finish()
