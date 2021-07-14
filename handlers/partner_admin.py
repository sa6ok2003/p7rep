from aiogram import types
from misc import dp, bot
import sqlite3
import asyncio

from .sqlit import cheach_channel_par,info

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

ADMIN_ID_1 = 494588959 #Cаня

PARTNERS1 = 430142587 #ДЕНИС
PARTNERS2 = 984418306 #Игорь
#ФАИН PARTNERS3 = 519072406
PARTNERS4 = 921818240 #Юля
PARTNERS5 = 1013231983 # АЛЕКС

class st_person_den(StatesGroup):
    st_1 = State()
    st_2 = State()


@dp.message_handler(commands=['info'],state='*')
async def cheak_traaf(message: types.Message):
    q  = cheach_channel_par(message.chat.id)
    if q != []: #Если зарегистрирован в базе для просмотра
        for i in q:
            s = (info(i[0]))
            await bot.send_message(message.chat.id, f'Счетчик @{i[0]}: {s}')