import sqlite3
import aioschedule
import asyncio
from aiogram import types
from dispatcher import bot
import random

class BotDB:
    global base, cur
    base = sqlite3.connect('bot_db.sqlite3')
    cur = base.cursor()

    def user_exists(user_id):
        """Проверяем, есть ли юзер в базе"""
        result = cur.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def user_ref_exists(user_id):
        """Проверяем, есть ли юзер в базе"""
        result = cur.execute("SELECT `id` FROM `users` WHERE `first_referrer_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def lot_exists(user_id):
        """Проверяем, есть ли юзер в базе"""
        result = cur.execute("SELECT `id` FROM `lottery` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def promo_exists(user_id):
        """Проверяем, есть ли юзер в базе"""
        result = cur.execute("SELECT `id` FROM `promo_codes` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def achivement_exists(user_id):
        """Проверяем, есть ли юзер в базе"""
        result = cur.execute("SELECT `id` FROM `achivement` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def daily_bonus_exists(user_id):
        """Проверяем, есть ли бонус в базе"""
        result = cur.execute("SELECT `id` FROM `daily_bonus` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_lvl(user_id):
        """Достаем id юзера в базе по его user_id"""
        result = cur.execute("SELECT `user_level` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def get_user_mail(user_id):
        """Достаем id юзера в базе по его user_id"""
        result = cur.execute("SELECT `mail` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def get_bonus_daily(user_id):
        """Добавляем юзера в базу"""
        cur.execute("INSERT INTO `daily_bonus` (`user_id`) VALUES (?)", (user_id,))
        return base.commit()

    def add_lot(user_id):
        """Добавляем юзера в базу"""
        cur.execute("INSERT INTO `lottery` (`user_id`) VALUES (?)", (user_id,))
        return base.commit()

    def week_bonus_exists(user_id):
        """Проверяем, есть ли бонус в базе"""
        result = cur.execute("SELECT `id` FROM `week_bonus` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_bonus_week(user_id):
        """Добавляем юзера в базу"""
        cur.execute("INSERT INTO `week_bonus` (`user_id`) VALUES (?)", (user_id,))
        return base.commit()

    def get_user_id(user_id):
        """Достаем id юзера в базе по его user_id"""
        result = cur.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def user_language(user_id):
        """Достаем id юзера в базе по его user_id"""
        user_language = cur.execute(f"SELECT user_language FROM users WHERE user_id = ?", (user_id,))
        return user_language.fetchone()[0]

    def get_records(user_id, within="all"):
        """Получаем историю о доходах/расходах"""
        if within == "day":
            result = cur.execute("SELECT * FROM `paymants` WHERE `user_id` = ? AND `date` BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY `date`", (user_id,))
        elif within == "week":
            result = cur.execute("SELECT * FROM `paymants` WHERE `user_id` = ? AND `date` BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY `date`", (user_id,))
        elif within == "month":
            result = cur.execute("SELECT * FROM `paymants` WHERE `user_id` = ? AND `date` BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY `date`", (user_id,))
        else:
            result = cur.execute("SELECT * FROM `paymants` WHERE `user_id` = ? ORDER BY `date`", (user_id,))
        return result.fetchall()

    def get_say_hi(user_id, within="all"):
        """Получаем историю о доходах/расходах"""
        if within == "day":
            result = cur.execute("SELECT * FROM `say_hi` WHERE `user_id` = ? AND `date` BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY `date`", (user_id,))
        elif within == "week":
            result = cur.execute("SELECT * FROM `say_hi` WHERE `user_id` = ? AND `date` BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY `date`", (user_id,))
        elif within == "month":
            result = cur.execute("SELECT * FROM `say_hi` WHERE `user_id` = ? AND `date` BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY `date`", (user_id,))
        else:
            result = cur.execute("SELECT * FROM `say_hi` WHERE `user_id` = ? ORDER BY `date`", (user_id,))
        return result.fetchall()

    def get_ban_list(user_id, within="all"):
        """Получаем историю о доходах/расходах"""
        result = cur.execute("SELECT * FROM `users` WHERE `user_id` = ? AND `ban` = 1 ORDER BY `join_date`", (user_id,))
        return result.fetchall()

    def get_patron_list(user_id, within="all"):
        """Получаем историю о доходах/расходах"""
        result = cur.execute("SELECT * FROM `users` WHERE `user_id` = ? AND `patron` = 1 ORDER BY `join_date`", (user_id,))
        return result.fetchall()

    def get_user_sec_ref(user_id):
        """Достаем id юзера в базе по его user_id"""
        result = cur.execute("SELECT `user_id` FROM `users` WHERE `first_referrer_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(user_id, first_referrer_id=None):
        """Добавляем юзера в базу"""
        if first_referrer_id != None:
            cur.execute("INSERT INTO `users` (`user_id`, `first_referrer_id`) VALUES (?, ?)",
                        (user_id, first_referrer_id,))
        else:
            cur.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return base.commit()

    def add_achivement(user_id):
        """Добавляем ачивки в базу"""
        cur.execute("INSERT INTO `achivement` (`user_id`) VALUES (?)", (user_id,))
        return base.commit()

    def count_ref(user_id):
        """Рахуємо рефералів"""
        result = cur.execute("SELECT COUNT (`id`) as count FROM `users` WHERE `first_referrer_id` = ?", (user_id,))
        return result.fetchone()[0]

    def count_sec_ref(user_id):
        """Рахуємо рефералів"""
        result = cur.execute("SELECT COUNT (`id`) as count FROM `users` WHERE `second_referrer_id` = ?", (user_id,))
        return result.fetchone()[0]

    def count_thi_ref(user_id):
        """Рахуємо рефералів"""
        result = cur.execute("SELECT COUNT (`id`) as count FROM `users` WHERE `third_referrer_id` = ?", (user_id,))
        return result.fetchone()[0]

    def count_del_trx_admin(user_id):
        """Рахуємо рефералів"""
        result = cur.execute("SELECT COUNT (`del_trx`) as count FROM `paymants` WHERE `del_trx` != ? AND `acces` = ?", (0, 0,))
        return result.fetchone()[0]

    def count_add_trx_admin(user_id):
        """Рахуємо рефералів"""
        result = cur.execute("SELECT COUNT (`add_trx`) as count FROM `paymants` WHERE `add_trx` != ? AND `acces` = ?", (0, 0,))
        return result.fetchone()[0]

    def count_add_usd_admin(user_id):
        """Рахуємо рефералів"""
        result = cur.execute("SELECT COUNT (`add_usd`) as count FROM `paymants` WHERE `add_usd` != ? AND `acces` = ?", (0, 0,))
        return result.fetchone()[0]

    def count_say_hi_admin(user_id):
        """Рахуємо рефералів"""
        result = cur.execute("SELECT COUNT (`text_message`) as count FROM `say_hi` WHERE `acces` = ?", (0,))
        return result.fetchone()[0]

    def close(base):
        """Закрываем соединение с БД"""
        base.close()


async def all_acc_stats():
    cur.execute('UPDATE stats SET all_acc = round(all_acc * 1.0025)')
    return base.commit()

async def pay_trx_stats():
    cur.execute('UPDATE stats SET pay_trx = pay_trx * 1.0085')
    return base.commit()

async def day_acc_stats():
    day_acs = random.randint(-25, 25)
    if day_acs <= 10:
        day_acs = random.randint(-25, 25)
    if day_acs == 0:
        day_acs = random.randint(-25, 25)
    cur.execute(f'UPDATE stats SET day_acc = round(day_acc + {day_acs})')
    return base.commit()

async def active_acc_stats():
    cur.execute('UPDATE stats SET active_acc = round(active_acc * 1.0105)')
    return base.commit()

async def del_lot_db():
    cur.execute('DELETE FROM lottery WHERE user_id > 0')
    return base.commit()


async def give_bonus_daily(user_id):
    """Даємо щоденний бонус"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_bonus_daily_lvl_2(user_id):
    """Даємо щоденний бонус"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 1.05 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_bonus_daily_lvl_3(user_id):
    """Даємо щоденний бонус"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 1.15 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def update_bonus_daily(user_id):
    """Оновлюємо дату"""
    cur.execute("UPDATE daily_bonus SET date = CURRENT_TIMESTAMP WHERE `user_id` = ?", (user_id,))
    cur.execute("UPDATE achivement SET daily_bonus = daily_bonus + 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_bonus_week(user_id):
    """Даємо тижневий бонус"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 2.5 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_bonus_week_lvl_3(user_id):
    """Даємо тижневий бонус"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 3 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_bonus_ref(user_id):
    """Даємо реферальний бонус"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_bonus_ref_sec_ref(user_id):
    """Даємо реферальний бонус"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 0.6 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_bonus_ref_thi_ref(user_id):
    """Даємо реферальний бонус"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 0.2 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_bonus_ref_start(user_id):
    """Даємо реферальний бонус"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def update_bonus_week(user_id):
    """Оновлюємо дату"""
    cur.execute("UPDATE week_bonus SET date = CURRENT_TIMESTAMP WHERE `user_id` = ?", (user_id,))
    cur.execute("UPDATE achivement SET week_bonus = week_bonus + 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def add_del_trx(state):
    """Добавляем платеж в базу"""
    async with state.proxy() as data:
        cur.execute("INSERT INTO `paymants` (`del_trx`, `user_id`, `adress`) VALUES (?, ?, ?)", tuple(data.values()))
        base.commit()


async def add_add_trx(state):
    """Добавляем платеж в базу"""
    async with state.proxy() as data:
        cur.execute("INSERT INTO `paymants` (`add_trx`, `user_id`, `adress`) VALUES (?, ?, ?)", tuple(data.values()))
        base.commit()


async def add_add_usd(state):
    """Добавляем платеж в базу"""
    async with state.proxy() as data:
        cur.execute("INSERT INTO `paymants` (`add_usd`, `user_id`, `adress`) VALUES (?, ?, ?)", tuple(data.values()))
        base.commit()


async def give_level_2(user_id):
    """Даємо реферальний бонус"""
    cur.execute("UPDATE users SET user_level = 2 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_level_3(user_id):
    """Даємо реферальний бонус"""
    cur.execute("UPDATE users SET user_level = 3 WHERE `user_id` = ?", (user_id,))
    return base.commit()

async def give_achivement_day(user_id):
    """Перевірка ачівки"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 2.5 WHERE `user_id` = ?", (user_id,))
    cur.execute("UPDATE achivement SET c_daily_bonus = 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_achivement_pay(user_id):
    """Перевірка ачівки"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 5 WHERE `user_id` = ?", (user_id,))
    cur.execute("UPDATE achivement SET c_pay_trx = 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_achivement_pay_th(user_id):
    """Перевірка ачівки"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 25 WHERE `user_id` = ?", (user_id,))
    cur.execute("UPDATE achivement SET c_pay_trx_th = 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_achivement_f(user_id):
    """Перевірка ачівки"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 6.5 WHERE `user_id` = ?", (user_id,))
    cur.execute("UPDATE achivement SET c_f_ref = 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def give_achivement_s(user_id):
    """Перевірка ачівки"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 3.5 WHERE `user_id` = ?", (user_id,))
    cur.execute("UPDATE achivement SET c_s_ref = 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()


async def get_users():
    result = cur.execute("SELECT `user_id` FROM `users`")
    return result.fetchall()

async def get_users_ua():
    result = cur.execute("SELECT `user_id` FROM `users` WHERE `user_language` = 'ua'")
    return result.fetchall()

async def get_users_ru():
    result = cur.execute("SELECT `user_id` FROM `users` WHERE `user_language` = 'ru'")
    return result.fetchall()

async def get_users_en():
    result = cur.execute("SELECT `user_id` FROM `users` WHERE `user_language` = 'en'")
    return result.fetchall()

async def get_users_ban():
    result = cur.execute("SELECT `user_id` FROM `users` WHERE `ban` = 1")
    return result.fetchall()

async def get_users_patron():
    result = cur.execute("SELECT `user_id` FROM `users` WHERE `patron` = 1")
    return result.fetchall()


async def give_achivement_a(user_id):
    """Перевірка ачівки"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 10 WHERE `user_id` = ?", (user_id,))
    cur.execute("UPDATE achivement SET c_a_ref = 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()

async def give_achivement_cub(user_id):
    """Перевірка ачівки"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 3.5 WHERE `user_id` = ?", (user_id,))
    cur.execute("UPDATE achivement SET c_game_cub = 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()

async def give_achivement_win_lot(user_id):
    """Перевірка ачівки"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 13.5 WHERE `user_id` = ?", (user_id,))
    cur.execute("UPDATE achivement SET c_win_lot = 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()

async def give_achivement_miner(user_id):
    """Перевірка ачівки"""
    cur.execute("UPDATE users SET bal_trx = bal_trx + 4 WHERE `user_id` = ?", (user_id,))
    cur.execute("UPDATE achivement SET c_game_mine = 1 WHERE `user_id` = ?", (user_id,))
    return base.commit()
