from aiogram import types
from misc import dp,bot
import sqlite3
from .sqlit import reg_user

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    channel_name = message.text[7:]
    reg_user(message.chat.id,channel_name)

    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🥤НАЧАТЬ СМОТРЕТЬ🥤', callback_data= f'start_watch_{channel_name}')
    markup.add(bat_a)
    await bot.send_message(message.chat.id, f'🥤Все новинки фильмов 2021 доступны на нашем <b>приватном канале.</b> \n'
                                            '\n'
                                            '📲Приятного просмотра 👇👇👇',parse_mode='html',reply_markup=markup)