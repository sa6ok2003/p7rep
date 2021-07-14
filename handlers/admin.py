from aiogram import types
from misc import dp, bot
import sqlite3
from .callbak_data import obnovlenie
from .sqlit import info_members, reg_one_channel, reg_channels,del_one_channel,user_partners,info_partners,delit_partners,obnovatrafika,cheak_traf,reg_partners_schet,cheach_all_par,info
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 1489359560 #Менеджер
ADMIN_ID_4 = 941730379 #Джейсон

ADMIN_ID =[ADMIN_ID_1,ADMIN_ID_2,ADMIN_ID_3,ADMIN_ID_4]

PARTNERS1 = 430142587 #ДЕНИС
PARTNERS2 = 984418306 #Игорь
PARTNERS3 = 519072406 #ФАИН
PARTNERS4 = 921818240 #Юля

class reg(StatesGroup):
    name = State()
    fname = State()

class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()
    step_q = State()
    step_regbutton = State()


class del_user(StatesGroup):
    del_name = State()
    del_fname = State()

class partners12(StatesGroup):
    step1 = State()
    step2 = State()

class reg_partners(StatesGroup):
    name_partners = State()
    fname_partners = State()
    dname_partners = State ()

class reg_trafik(StatesGroup):
    traf1 = State()
    traf2 = State()

@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик | Количество пользователей', callback_data='list_members')
        bat_b = types.InlineKeyboardButton(text='NEW канал | Разрешенный канал', callback_data='new_channel')# Добавляет 1 канал
        bat_c = types.InlineKeyboardButton(text='NEW Список | Добавить много каналов', callback_data='new_channels') # Добавляет список каналов через пробел
        bat_d = types.InlineKeyboardButton(text='Удалить канал ', callback_data='delite_channel')# Удаляет канал из списка
        bat_e = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
        bat_j = types.InlineKeyboardButton(text='Скачать базу', callback_data='baza')
        bat_f = types.InlineKeyboardButton(text='Партнеры', callback_data='partners')
        bat_setin = types.InlineKeyboardButton(text='Настройка трафика', callback_data='settings')

        reg_new_partners = types.InlineKeyboardButton(text='РЕГИСТРАЦИЯ НОВОГО ПАРТНЕРА',callback_data='reg_new_partners')
        vienw_partners = types.InlineKeyboardButton(text='СТАТИСТИКА ВСЕХ ПАРТНЕРОВ', callback_data='vienw_partners')


        markup.add(bat_a)
        markup.add(bat_b)
        markup.add(bat_c)
        markup.add(bat_d)
        markup.add(bat_e)
        markup.add(bat_j)
        markup.add(bat_f)
        markup.add(bat_setin)
        markup.add(reg_new_partners)
        markup.add(vienw_partners)

        await bot.send_message(message.chat.id,'Выполнен вход в админ панель',reply_markup=markup)



#ПРОСМОТР ВСЕХ ПАРТНЕРОВ
@dp.callback_query_handler(text='vienw_partners')  #ПРОСМОТР ВСЕХ ПАРТНЕРОВ
async def vienw_partners(call: types.callback_query):
    q = cheach_all_par()
    if q != []:  # Если зарегистрирован в базе для просмотра
        for i in q:
            s = (info(i[0]))
            await bot.send_message(call.message.chat.id, f'Счетчик @{i[0]}: {s}')

#МЕНЮ НОВЫХ ПАРТНЕРОВ
@dp.callback_query_handler(text='reg_new_partners')  #МЕНЮ
async def check_all_partners(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(chat_id=call.message.chat.id,text = 'Перешлите сообщение от партнера',reply_markup=markup)
    await partners12.step1.set()


@dp.message_handler(state=partners12.step1, content_types='text')
async def get_id_partners(message: types.Message, state: FSMContext):
    try:
        id = message.forward_from.id
        await state.update_data(id_partners = id)
        await bot.send_message(chat_id=message.chat.id, text='ID получен! \n'
                                                             'Введите имя канала слитно без пробелов, через @')
        await partners12.step2.set()

    except:
        await bot.send_message(chat_id=message.chat.id, text='У партнера скрытый аккаунт!\n'
                                                             'Повторите попытку')


@dp.message_handler(state=partners12.step2, content_types='text')
async def get_channel_partners(message: types.Message, state: FSMContext):
    chennel = message.text
    if chennel[0] == '@':
        await bot.send_message(chat_id=message.chat.id, text='Канал зарегистрирован')
        text_id = (await state.get_data())['id_partners']
        reg_partners_schet(channel=chennel[1:],id = text_id)
        await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id, text='Повторите попытку')



########################### Партнеры ####################################
@dp.callback_query_handler(text='partners')
async def partners_info(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='Список учителей, и их учеников', callback_data='list_partners') # Список партнеров
    bat_b = types.InlineKeyboardButton(text='Новый партнер',callback_data='new_partners')  # Добавляет нового партнера
    bat_c = types.InlineKeyboardButton(text='Удалить партнера',callback_data='del_partners')  # Удаляет партнера
    bat_d = types.InlineKeyboardButton(text='Назад', callback_data='exit_partners')  # УНазад

    markup.add(bat_a)
    markup.add(bat_b)
    markup.add(bat_c)
    markup.add(bat_d)

    await bot.edit_message_text(message_id=call.message.message_id,chat_id=call.message.chat.id,text='Панель партнеров',reply_markup=markup)



#ОБНОВА ТРАФИКА
# НАСТРОЙКА ТРАФИКА
@dp.callback_query_handler(text='settings')
async def baza12(call: types.callback_query):
    markup_traf = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ИЗМЕНИТЬ КАНАЛЫ⚙️', callback_data='change_trafik')
    markup_traf.add(bat_a)
    list = cheak_traf()
    await bot.send_message(call.message.chat.id, text=f'Список активный каналов на данный момент:\n\n'
                                                      f'1. @{list[0]}\n'
                                                      f'2. @{list[1]}\n'
                                                      f'3. @{list[2]}\n\n'
                                                      f'<b>Внимание! Первый по счету канал , должен быть обязательно с кино-тематикой</b> А третий канал по счету будет получать меньше трафика, так как он будет заменяться каналом учителя, если тот имеется\n'
                                                      f'Для изменения жми кнопку',parse_mode='html',reply_markup=markup_traf)


@dp.callback_query_handler(text='change_trafik') # Изменение каналов, на которые нужно подписаться
async def baza12342(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Введите новый список каналов\n<b>ПЕРВЫЙ КАНАЛ ДОЛЖЕН БЫТЬ ОБЯЗАТЕЛЬНО С КИНО-ТЕМАТИКОЙ!</b>\n\n'
                                                      'Список каналов вводи в строчку, пример:\n'
                                                      '@channel1 @channel2 @channel3',parse_mode='html',reply_markup=markup)
    await reg_trafik.traf1.set()


@dp.message_handler(state=reg_trafik.traf1, content_types='text')
async def traf_obnovlenie(message: types.Message, state: FSMContext):
    mas = message.text.split()
    if (len(mas) == 3 and mas[0][0] == '@' and mas[1][0] == '@' and mas[2][0] == '@'):
        # Список новых каналов
        channel1 = mas[0][1:]
        channel2 = mas[1][1:]
        channel3 = mas[2][1:]

        obnovatrafika(channel1,channel2,channel3) # Внесение новых каналов в базу данных
        obnovlenie()
        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. ТЕбе необходимо снова зайти в админ панель и выбрать нужный пункт.'
                                                            'Сообщение со списком каналом мне отсылать сейчас бессмыслено - я тебя буду игнорить, поэтому делай по новой все')
        await state.finish()




@dp.callback_query_handler(text='exit_partners') ### Выход из панели партнеров
async def partners_exit(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='Трафик | Количество пользователей', callback_data='list_members')
    bat_b = types.InlineKeyboardButton(text='NEW канал | Разрешенный канал', callback_data='new_channel')  # Добавляет 1 канал
    bat_c = types.InlineKeyboardButton(text='NEW Список | Добавить много каналов', callback_data='new_channels')  # Добавляет список каналов через пробел
    bat_d = types.InlineKeyboardButton(text='Удалить канал ', callback_data='delite_channel')  # Удаляет канал из списка
    bat_e = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
    bat_j = types.InlineKeyboardButton(text='Скачать базу', callback_data='baza')
    bat_f = types.InlineKeyboardButton(text='Партнеры', callback_data='partners')

    markup.add(bat_a)
    markup.add(bat_b)
    markup.add(bat_c)
    markup.add(bat_d)
    markup.add(bat_e)
    markup.add(bat_j)
    markup.add(bat_f)

    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text='Выполнен вход в админ панель', reply_markup=markup)

@dp.callback_query_handler(state=reg_partners.name_partners,text='partners_otmena')
async def partners_otmena(call: types.callback_query,state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await state.finish()

@dp.callback_query_handler(text='exitpartners')
async def partners_otmena(call: types.callback_query,state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='del_partners')
async def del_partners(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_d = types.InlineKeyboardButton(text='Назад', callback_data='exitpartners')  # Назад
    markup.add(bat_d)
    await bot.send_message(call.message.chat.id,text='Удаление партнера происходит по каналу ученика\n'
                                                'Что бы учитель был полностью анулирован, нужно что бы у него не было учеников\n'
                                                'Напиши мне @name_channel Ученика, что бы я его удалил.\n\n'
                                                'Так же не забудь удалить канал ученика из списка разрешенных, что бы он не смог гнать трафик на свой канал\n\n'
                                                '<b>Кидай мне @name_channel ученика</b>',parse_mode='html',reply_markup=markup)
    await reg_partners.dname_partners.set()





@dp.message_handler(state=reg_partners.dname_partners, content_types='text')
async def delpartners(message: types.Message, state: FSMContext):
    if message.text[:1] != '@':
        await bot.send_message(message.chat.id,text='Отправь @name_channel Ученика, которого нужно удалить')
    else:
        a = delit_partners(message.text[1:])
        if a == 0:
            await bot.send_message(message.chat.id,'Не нашел такой канал у ученика. Завершаю процесс удаления')
            await state.finish()
        else:
            await bot.send_message(chat_id=message.chat.id,text=f'Ученик {message.text} успешно удален')
            await state.finish()



@dp.callback_query_handler(text='list_partners')
async def partners_otmena(call: types.callback_query,state: FSMContext):
    a = info_partners()
    mas = []
    for i in a:
        mas.append('@'+i[0] + ' ' + '@'+i[1])
    g = '\n\n'.join([i for i in mas])
    await bot.send_message(call.message.chat.id, f'<b>Количество учеников: {len(a)}</b>\n\n'
                                                 'Пары <b>учитель - ученик:</b>\n'
                                                 f'{g}',parse_mode='html')

@dp.callback_query_handler(text='new_partners') ### Добавление нового партнера
async def partners_new(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='partners_otmena')
    markup.add(bat_a)
    await bot.send_message(call.message.chat.id, '<b>Будь внимателен при регистрации нового партнера!\n\n</b>'
                                                 'Процесс регистрации будет проходить следующим образом:\n\n'
                                                 'Перед регистрацией подготовь имена каналов ученика и учителя ! \n\n'
                                                 '1. Отправляешь мне @name_channel <b>Учителя</b>\n\n'
                                                 '2. Отправляешь мне @name_channel ученика\n\n'
                                                 'Сейчас сникнь мне канал учителя<b></b>\n\n'
                                                 'Для отмены жми кнопку \/',parse_mode='html',reply_markup=markup)
    await reg_partners.name_partners.set()


@dp.message_handler(state=reg_partners.name_partners, content_types='text')
async def name_partners(message: types.Message, state: FSMContext):
    if message.text[0] != '@':
        await bot.send_message(message.chat.id,text='Отправь мне канал учителя!\n\n'
                                                    'В формате @name_channels')
    else:
        await bot.send_message(message.chat.id, text='Канал учителя зарегистрирован!\n\n'
                                                     'Теперь тебе нужно скинуть мне канал Ученика')
        await state.update_data(channel_teacher=message.text[1:])
        await reg_partners.fname_partners.set()


@dp.message_handler(state=reg_partners.fname_partners, content_types='text')
async def jname_partners(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text[0] != '@':
        await bot.send_message(message.chat.id,text='Отправь мне канал ученика!\n\n'
                                                    'В формате @name_channels')
    else:
        await bot.send_message(message.chat.id, text='Канал ученика зарегистрирован!\n\n'
                                                     'Теперь тебе нужно добавить канал ученика в список разрешенных каналов через админ панель (Как это делалось со всеми каналами участников квеста')
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(chat_id=message.chat.id,text='Успешно')
        channel_people= message.text[1:]
        channel_teacher = data['channel_teacher']
        user_partners(channel_teacher,channel_people)
##################################################

@dp.callback_query_handler(text='baza')
async def baza(call: types.callback_query):
    a = open('server.db','rb')
    await bot.send_document(chat_id=call.message.chat.id, document=a)


############################  DELITE CHANNEL  ###################################
@dp.callback_query_handler(text='delite_channel')
async def del_channel(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь название канала для удаления в формате\n'
                                                 '@name_channel')
    await del_user.del_name.set()


@dp.message_handler(state=del_user.del_name, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    check_dog = message.text[:1]
    if check_dog != '@':
        await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
    else:
        await state.finish()
        del_one_channel(message.text)
        await bot.send_message(message.chat.id, 'Удаление завершено')


############################  REG ONE CHANNEL  ###################################
@dp.callback_query_handler(text='new_channel')  # АДМИН КНОПКА Добавления нового трафика
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь название нового канала в формате\n'
                                                 '@name_channel')
    await reg.name.set()


@dp.message_handler(state=reg.name, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    check_dog = message.text[:1]
    if check_dog != '@':
        await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
    else:
        reg_one_channel(message.text)
        await bot.send_message(message.chat.id, 'Регистрация успешна')
        await state.finish()


################################    REG MANY CHANNELS    ###########################

@dp.callback_query_handler(text='new_channels')  # АДМИН КНОПКА Добавления новые телеграмм каналы
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь список каналов в формате\n'
                                                 '@name1 @name2 @name3 ')
    await reg.fname.set()


@dp.message_handler(state=reg.fname, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Каналы зарегистрированы')
    reg_channels(message.text)
    await state.finish()

#####################################################################################


@dp.callback_query_handler(text='list_members')  # АДМИН КНОПКА ТРАФИКА
async def check(call: types.callback_query):
    a = info_members() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Количество пользователей: {a}')


########################  Рассылка  ################################

@dp.callback_query_handler(text='write_message')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                           reply_markup=murkap)
    await st_reg.step_q.set()


@dp.callback_query_handler(text='otemena',state='*')
async def otmena_12(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()



@dp.message_handler(state=st_reg.step_q,content_types=['text','photo','video','video_note']) # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    await st_reg.st_name.set()
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
    bat2 = types.InlineKeyboardButton(text='Добавить кнопки', callback_data='add_but')
    murkap.add(bat1)
    murkap.add(bat2)
    murkap.add(bat0)

    await message.copy_to(chat_id=message.chat.id)
    q = message
    await state.update_data(q=q)

    await bot.send_message(chat_id=message.chat.id,text='Пост сейчас выглядит так 👆',reply_markup=murkap)



# НАСТРОЙКА КНОПОК
@dp.callback_query_handler(text='add_but',state=st_reg.st_name) # Добавление кнопок
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id,text='Отправляй мне кнопки по принципу Controller Bot\n\n'
                                                     'Пока можно добавить только одну кнопку')
    await st_reg.step_regbutton.set()


@dp.message_handler(state=st_reg.step_regbutton,content_types=['text']) # Текст кнопок в неформате
async def redarkt_button(message: types.Message, state: FSMContext):
    arr2 = message.text.split('-')

    k = -1  # Убираем пробелы из кнопок
    for i in arr2:
        k+=1
        if i[0] == ' ':
            if i[-1] == ' ':
                arr2[k] = (i[1:-1])
            else:
                arr2[k] = (i[1:])

        else:
            if i[-1] == ' ':

                arr2[0] = (i[:-1])
            else:
                pass

    # arr2 - Массив с данными


    try:
        murkap = types.InlineKeyboardMarkup() #Клавиатура с кнопками
        bat = types.InlineKeyboardButton(text= arr2[0], url=arr2[1])
        murkap.add(bat)

        data = await state.get_data()
        mess = data['q']  # ID сообщения для рассылки

        await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,message_id=mess.message_id,reply_markup=murkap)

        await state.update_data(text_but =arr2[0]) # Обновление Сета
        await state.update_data(url_but=arr2[1])  # Обновление Сета

        murkap2 = types.InlineKeyboardMarkup() # Клавиатура - меню
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
        murkap2.add(bat1)
        murkap2.add(bat0)

        await bot.send_message(chat_id=message.chat.id,text='Теперь твой пост выглядит так☝',reply_markup=murkap2)


    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()


# КОНЕЦ НАСТРОЙКИ КНОПОК


@dp.callback_query_handler(text='send_ras',state="*") # Рассылка
async def fname_step(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

    data = await state.get_data()
    mess = data['q'] # Сообщения для рассылки

    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками

    try: #Пытаемся добавить кнопки. Если их нету оставляем клаву пустой
        text_but = data['text_but']
        url_but = data['url_but']
        bat = types.InlineKeyboardButton(text=text_but, url=url_but)
        murkap.add(bat)
    except: pass


    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time").fetchall()
    bad = 0
    good = 0
    await bot.send_message(call.message.chat.id, f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        await asyncio.sleep(1)
        try:
            await mess.copy_to(i[0],reply_markup=murkap)
            good += 1
        except:
            bad += 1

    await bot.send_message(
        call.message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )
#########################################################