import db
from asyncio import sleep
from aiogram.dispatcher import FSMContext
from dispatcher import dp, admins, bot
from aiogram import types
from handlers.states import mailing
import keyboards as kb

#######################################################################################################################################

@dp.message_handler(commands=['ad', 'admin', 'mod', 'moder', 'фв', 'фвьшт', 'адмін', 'ад'], chat_id=admins)
async def start_mailing(message: types.Message):
    markup_admin = types.InlineKeyboardMarkup(row_width=1)
    del_trx_admin = types.InlineKeyboardButton(f'⬆ Заявки на вивід ({db.BotDB.count_del_trx_admin(0)})', callback_data='del_trx_admin')
    add_trx_admin = types.InlineKeyboardButton(f'💶 Заявки на поповнення TRX ({db.BotDB.count_add_trx_admin(0)})', callback_data='add_trx_admin')
    add_usd_admin = types.InlineKeyboardButton(f'💲 Заявки на поповнення USDT ({db.BotDB.count_add_usd_admin(0)})', callback_data='add_usd_admin')
    say_hi_admin_kb = types.InlineKeyboardButton(f'🗣 Поділитись історією/музикою ({db.BotDB.count_say_hi_admin(0)})', callback_data='say_hi_admin_kb')
    work_user_admin = types.InlineKeyboardButton(f'🤖 Робота з користувачем', callback_data='work_user_admin')
    mailing_admin = types.InlineKeyboardButton(f'✍ Розсилка', callback_data='mailing_admin')
    markup_admin.add(del_trx_admin, add_trx_admin, add_usd_admin, say_hi_admin_kb, mailing_admin, work_user_admin)
    await message.answer(f'👤 Адмін панель:                                                                        ㅤ', reply_markup=markup_admin)

#######################################################################################################################################


@dp.message_handler(state=mailing.text)
async def mailing_text(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(text=answer)
    markup_say_hi_add_photo, markup_say_hi_add_audio, markup_say_hi_add_audio_mod = await kb.markup_say(message)
    await message.answer(text=answer, reply_markup=markup_say_hi_add_photo)
    await mailing.state.set()

@dp.callback_query_handler(text= 'next', state=mailing.state)
async def mailing_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    markup_say_hi_add_photo, markup_say_hi_add_audio, markup_say_hi_add_audio_mod = await kb.markup_say(message)
    await bot.send_message(message.from_user.id, text=text, reply_markup=markup_say_hi_add_audio_mod)

@dp.callback_query_handler(text= 'send_text_msg', state=mailing.state)
async def language(call: types.callback_query, state: FSMContext):
    markup_language = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=3)
    ukrainian = types.InlineKeyboardButton('🇺🇦 Українська', callback_data="ua_mailing")
    russian = types.InlineKeyboardButton('🇷🇺 Русский', callback_data="ru_mailing")
    english = types.InlineKeyboardButton('🇬🇧 English', callback_data="en_mailing")
    all = types.InlineKeyboardButton('Всі користувачі', callback_data="all_mailing")
    exit = types.InlineKeyboardButton(text='❌ Відмінити', callback_data='quit')
    markup_language.add(ukrainian, russian, english).add(all).add(exit)
    await call.message.answer('🌬 Оберіть мову розсилки', reply_markup=markup_language)

@dp.callback_query_handler(text= 'ua_mailing', state=mailing.state)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_ua()
    data = await state.get_data()
    text = data.get('text')
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user[0], text=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для україномовних користувачів')

@dp.callback_query_handler(text= 'ru_mailing', state=mailing.state)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_ru()
    data = await state.get_data()
    text = data.get('text')
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user[0], text=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для російськомовних користувачів')

@dp.callback_query_handler(text= 'en_mailing', state=mailing.state)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_en()
    data = await state.get_data()
    text = data.get('text')
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user[0], text=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для англомовних користувачів')

@dp.callback_query_handler(text= 'all_mailing', state=mailing.state)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users()
    data = await state.get_data()
    text = data.get('text')
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user[0], text=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для всіх користувачів')

@dp.callback_query_handler(text='add_photo', state=mailing.state)
async def add_photo(call: types.callback_query):
    await call.message.answer('📸 Надішліть фото')
    await mailing.photo.set()

@dp.message_handler(state=mailing.photo, content_types=types.ContentType.PHOTO)
async def mailing_text(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup_say_hi_add_photo, markup_say_hi_add_audio, markup_say_hi_add_audio_mod = await kb.markup_say(message)
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup_say_hi_add_audio)


@dp.callback_query_handler(text='next', state=mailing.photo)
async def language(call: types.callback_query, state: FSMContext):
    markup_language = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=3)
    ukrainian = types.InlineKeyboardButton('🇺🇦 Українська', callback_data="ua_mailing")
    russian = types.InlineKeyboardButton('🇷🇺 Русский', callback_data="ru_mailing")
    english = types.InlineKeyboardButton('🇬🇧 English', callback_data="en_mailing")
    all = types.InlineKeyboardButton('Всі користувачі', callback_data="all_mailing")
    exit = types.InlineKeyboardButton(text='❌ Відмінити', callback_data='quit')
    markup_language.add(ukrainian, russian, english).add(all).add(exit)
    await call.message.answer('🌬 Оберіть мову розсилки', reply_markup=markup_language)

@dp.callback_query_handler(text= 'ua_mailing', state=mailing.photo)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_ua()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user[0], photo=photo, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для україномовних користувачів')

@dp.callback_query_handler(text= 'ru_mailing', state=mailing.photo)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_ru()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user[0], photo=photo, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для російськомовних користувачів')

@dp.callback_query_handler(text= 'en_mailing', state=mailing.photo)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_en()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user[0], photo=photo, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для англомовних користувачів')

@dp.callback_query_handler(text= 'all_mailing', state=mailing.photo)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user[0], photo=photo, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для всіх користувачів')

@dp.callback_query_handler(text='add_song', state=mailing.state)
async def add_song(call: types.callback_query):
    await call.message.answer('🎤 Надішліть пісню')
    await mailing.song.set()

@dp.message_handler(state=mailing.song, content_types=types.ContentType.AUDIO)
async def mailing_text(message: types.Message, state: FSMContext):
    audio_file_id = message.audio.file_id
    await state.update_data(audio=audio_file_id)
    data = await state.get_data()
    text = data.get('text')
    audio = data.get('audio')
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[[types.InlineKeyboardButton(text='✅ Виконати розсилку', callback_data='next'), types.InlineKeyboardButton(text='❌ Відмінити', callback_data='quit')]])
    await message.answer_audio(audio=audio, caption=text, reply_markup=markup)


@dp.callback_query_handler(text='next', state=mailing.song)
async def language(call: types.callback_query, state: FSMContext):
    markup_language = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=3)
    ukrainian = types.InlineKeyboardButton('🇺🇦 Українська', callback_data="ua_mailing")
    russian = types.InlineKeyboardButton('🇷🇺 Русский', callback_data="ru_mailing")
    english = types.InlineKeyboardButton('🇬🇧 English', callback_data="en_mailing")
    all = types.InlineKeyboardButton('Всі користувачі', callback_data="all_mailing")
    exit = types.InlineKeyboardButton(text='❌ Відмінити', callback_data='quit')
    markup_language.add(ukrainian, russian, english).add(all).add(exit)
    await call.message.answer('🌬 Оберіть мову розсилки', reply_markup=markup_language)

@dp.callback_query_handler(text= 'ua_mailing', state=mailing.song)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_ua()
    data = await state.get_data()
    text = data.get('text')
    audio = data.get('audio')
    for user in users:
        try:
            await dp.bot.send_audio(chat_id=user[0], audio=audio, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для україномовних користувачів')

@dp.callback_query_handler(text= 'ru_mailing', state=mailing.song)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_ru()
    data = await state.get_data()
    text = data.get('text')
    audio = data.get('audio')
    for user in users:
        try:
            await dp.bot.send_audio(chat_id=user[0], audio=audio, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для російськомовних користувачів')

@dp.callback_query_handler(text= 'en_mailing', state=mailing.song)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_en()
    data = await state.get_data()
    text = data.get('text')
    audio = data.get('audio')
    for user in users:
        try:
            await dp.bot.send_audio(chat_id=user[0], audio=audio, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для англомовних користувачів')

@dp.callback_query_handler(text= 'all_mailing', state=mailing.song)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users()
    data = await state.get_data()
    text = data.get('text')
    audio = data.get('audio')
    for user in users:
        try:
            await dp.bot.send_audio(chat_id=user[0], audio=audio, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для всіх користувачів')

@dp.callback_query_handler(text='add_song', state=mailing.photo)
async def add_song(call: types.callback_query):
    await call.message.answer('🎤 Надішліть пісню')
    await mailing.song_plus_photo.set()

@dp.message_handler(state=mailing.song_plus_photo, content_types=types.ContentType.AUDIO)
async def mailing_photo(message: types.Message, state: FSMContext):
    audio_file_id = message.audio.file_id
    await state.update_data(audio=audio_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    audio = data.get('audio')
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[[types.InlineKeyboardButton(text='✅ Виконати розсилку', callback_data='next'), types.InlineKeyboardButton(text='❌ Відмінити', callback_data='quit')]])
    await message.answer_photo(photo=photo, caption=text)
    await message.answer_audio(audio=audio, reply_markup=markup)


@dp.callback_query_handler(text='next', state=mailing.song_plus_photo)
async def language(call: types.callback_query, state: FSMContext):
    markup_language = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=3)
    ukrainian = types.InlineKeyboardButton('🇺🇦 Українська', callback_data="ua_mailing")
    russian = types.InlineKeyboardButton('🇷🇺 Русский', callback_data="ru_mailing")
    english = types.InlineKeyboardButton('🇬🇧 English', callback_data="en_mailing")
    all = types.InlineKeyboardButton('Всі користувачі', callback_data="all_mailing")
    exit = types.InlineKeyboardButton(text='❌ Відмінити', callback_data='quit')
    markup_language.add(ukrainian, russian, english).add(all).add(exit)
    await call.message.answer('🌬 Оберіть мову розсилки', reply_markup=markup_language)

@dp.callback_query_handler(text= 'ua_mailing', state=mailing.song_plus_photo)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_ua()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    audio = data.get('audio')
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user[0], photo=photo, caption=text)
            await dp.bot.send_audio(chat_id=user[0], audio=audio)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для україномовних користувачів')

@dp.callback_query_handler(text= 'ru_mailing', state=mailing.song_plus_photo)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_ru()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    audio = data.get('audio')
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user[0], photo=photo, caption=text)
            await dp.bot.send_audio(chat_id=user[0], audio=audio)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для російськомовних користувачів')

@dp.callback_query_handler(text= 'en_mailing', state=mailing.song_plus_photo)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users_en()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    audio = data.get('audio')
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user[0], photo=photo, caption=text)
            await dp.bot.send_audio(chat_id=user[0], audio=audio)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для англомовних користувачів')

@dp.callback_query_handler(text= 'all_mailing', state=mailing.song_plus_photo)
async def start(call: types.callback_query, state: FSMContext):
    users = await db.get_users()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    audio = data.get('audio')
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user[0], photo=photo, caption=text)
            await dp.bot.send_audio(chat_id=user[0], audio=audio)
            await sleep(0.33)
        except Exception:
            pass
    await state.finish()
    await call.message.answer('✅ Розсилка виконана для всіх користувачів')

@dp.message_handler(state=mailing.photo)
async def no_photo(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[[types.InlineKeyboardButton(text='❌ Відмінити', callback_data='quit')]])
    await message.answer('📸 Надішліть фото', reply_markup=markup)

@dp.message_handler(state=mailing.song)
async def no_song(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[[types.InlineKeyboardButton(text='❌ Відмінити', callback_data='quit')]])
    await message.answer('🎤 Надішліть пісню', reply_markup=markup)

@dp.callback_query_handler(text='quit', state=[mailing.text, mailing.photo, mailing.state, mailing.song, mailing.state_second, mailing.song_plus_photo, mailing.lang])
async def quit(call: types.callback_query, state: FSMContext):
    await state.finish()
    markup_start = await kb.markup_start(call.message)
    await call.message.answer('❌ Розсилка відмінена', reply_markup=markup_start)


#######################################################################################################################################

