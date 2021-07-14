from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp, bot


class reg(StatesGroup):
    name = State()
    fname = State()
    age = State()


@dp.message_handler(commands="reg", state="*")
async def name_step(message: types.Message, state: FSMContext):
    await message.answer(text='Напиши имя')
    await reg.name.set()




@dp.message_handler(state=reg.fname, content_types='text')
async def fname_step(message: types.Message, state: FSMContext):
    print(message.text)
    await bot.send_message(message.chat.id, 'Cколько тебе лет?')
    await reg.age.set()

@dp.message_handler(state=reg.age, content_types='text')
async def fname_step(message: types.Message, state: FSMContext):
    print(message.text)
    await bot.send_message(message.chat.id, 'Приятно Познакомится!')
    await state.finish()