from aiogram.dispatcher.filters.state import State, StatesGroup


class pay_operation(StatesGroup):
    del_trx = State()
    del_trx_get_adress = State()
    add_trx = State()
    add_trx_get_adress = State()
    add_usd = State()
    add_usd_get_adress = State()

class mailing(StatesGroup):
    text = State()
    state = State()
    photo = State()
    state_second = State()
    song = State()
    song_plus_photo = State()
    lang = State()

class say_hi(StatesGroup):
    text = State()
    state = State()
    photo = State()
    state_second = State()
    song = State()
    song_plus_photo = State()

class guess_number(StatesGroup):
    bet_five = State()
    random_number_five = State()
    bet_ten = State()
    random_number_ten = State()
    bet_hun = State()
    random_number_hun = State()

class fifty_fifty(StatesGroup):
    bet_two = State()
    random_number_two = State()
    bet_four = State()
    random_number_four = State()
    bet_ten = State()
    random_number_ten = State()

class dice(StatesGroup):
    bet_classic = State()
    random_number_classic = State()
    bet_under = State()
    random_number_under = State()

class miner(StatesGroup):
    bet_three = State()
    random_number_three = State()
    bet_five = State()
    random_number_five = State()
    bet_seven = State()
    random_number_seven = State()

class cases(StatesGroup):
    accept_buy = State()
    case_br_buy = State()
    case_si_buy = State()
    case_go_buy = State()

class spin(StatesGroup):
    bet_spin = State()
    random_number_spin = State()

class promo_code(StatesGroup):
    type_promo = State()

class captcha(StatesGroup):
    select_language = State()
    type_mail = State()
    type_captcha = State()
    type_phone = State()
    start = State()

class work_trx_admin(StatesGroup):
    sum_trx = State()
    user_id = State()
    accept = State()
    sum_trx_del = State()
    user_id_del = State()
    accept_del = State()

class work_usd_admin(StatesGroup):
    sum_trx = State()
    user_id = State()
    accept = State()
    sum_trx_del = State()
    user_id_del = State()
    accept_del = State()

class work_ban(StatesGroup):
    ban = State()
    unban = State()

class work_patreon(StatesGroup):
    patron = State()
    unpatron = State()

class say_hi_admin_kb_do_acces(StatesGroup):
    user_id = State()

class pay_admin_kb_do_acces(StatesGroup):
    user_id = State()
    select = State()

class pay_admin_kb_do_acces_add_trx(StatesGroup):
    user_id = State()
    select = State()

class pay_history_admin_add_usd(StatesGroup):
    user_id = State()
    select = State()

