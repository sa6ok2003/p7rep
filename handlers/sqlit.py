import sqlite3
def reg_user(id,ref):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(""" CREATE TABLE IF NOT EXISTS channel_list (
            name,
            number
            ) """)
    db.commit()#Таблица разрешенных каналов



    sql.execute(""" CREATE TABLE IF NOT EXISTS user_time (
        id BIGINT,
        status_ref
        ) """)
    db.commit()# Таблица юзеров



    sql.execute(""" CREATE TABLE IF NOT EXISTS user_partners (
            channel_teacher,
            channel_people
            ) """)
    db.commit()  # Таблица партнеров

    sql.execute(f"SELECT id FROM user_time WHERE id ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?)", (id, ref))
        db.commit()

    sql.execute(""" CREATE TABLE IF NOT EXISTS trafik (
                chanel,
                parametr,
                person
                ) """)
    db.commit()
    sql.execute(f"SELECT chanel FROM trafik WHERE chanel = 'channel1'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel1', 'nikolacinema', 100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel2', 'filmsmarket', 100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel3', 'Alitopprodaj', 100))
        db.commit()

# Cоздание отслеживания подписчиков
    sql.execute(""" CREATE TABLE IF NOT EXISTS stata_parthers ( 
            id BIGINT,
            channel_ref
            ) """)
    db.commit()
    sql.execute(f"SELECT id FROM stata_parthers WHERE id ='{0}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO stata_parthers VALUES (?,?)", (0,0))
        db.commit()


# ИНФО О ПАРТНЕРАХ ЧТО БЫ ПРИКРУТИТЬ ИМ СЧЕТЧИК
    sql.execute(""" CREATE TABLE IF NOT EXISTS parthers( 
                id_partn,
                name_channel,
                schet
                ) """)
    db.commit()


## НОВОЕ
def cheach_channel_par(id): #Возвращает 0 - если человек не работает с нами. имя его канала - если все хорошо
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    r = sql.execute(f"SELECT name_channel FROM parthers WHERE id_partn ={id}").fetchall()
    return r

def cheach_all_par(): #Возвращает 0 - если человек не работает с нами. имя его канала - если все хорошо
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    r = sql.execute(f"SELECT name_channel FROM parthers").fetchall()
    return r

def info(channel): #Возвращает количество подписок на канал
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = '{channel}'").fetchone()[0]
    return a


def reg_partners_schet(id,channel): #Регистрация партнера и его канала и отслеживание счетчика
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT id_partn FROM parthers WHERE name_channel ='{channel}' and id_partn ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO parthers VALUES (?,?,?)", (id, channel, 0))
        db.commit()

## КОНЕЦ НОВОГО


###### Количество подписок на каналы партнеров
def reg_pod(id,channel):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT id FROM stata_parthers WHERE id ='{id}' and channel_ref ='{channel}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO stata_parthers VALUES (?,?)", (id, channel))
        db.commit()


#Просмотр трафика
def info_chyornaya_vdova(): # Трафик Дена
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'chyornaya_vdova'").fetchone()[0]
    return a

def info_filmyshd(): # Трафик Фаина
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'filmyshd'").fetchone()[0]
    return a

def info_films_online_everyday(): # Трафик ЮЛИ
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'films_online_everyday'").fetchone()[0]
    return a



def info_members():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f'SELECT COUNT(*) FROM user_time').fetchone()[0]
    return a


def reg_one_channel(name): #Регистрация одного канала
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    name = name[1:]
    sql.execute(f"SELECT name FROM channel_list WHERE name ='{name}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO channel_list VALUES (?,?)", (name, 1))
        db.commit()
    db.commit()

def reg_channels(text): #Регистрация списка каналов
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    text = text.split()
    for i in text:
        i = i[1:]
        sql.execute(f"SELECT name FROM channel_list WHERE name ='{i}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO channel_list VALUES (?,?)", (i, 1))
            db.commit()
        db.commit()

def proverka_channel(channel_name):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT name FROM channel_list WHERE name ='{channel_name}'").fetchone()
    if a is None:
        return 0
    else:
        return 1

def del_one_channel(name): #Удаление одного канала
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    name = name[1:]
    sql.execute(f"SELECT name FROM channel_list WHERE name ='{name}'")
    if sql.fetchone() is None:
        pass
    else:
        sql.execute(f'DELETE FROM channel_list WHERE name ="{name}"')
        db.commit()


####################  Партнерские sqlit  #####################
def user_partners(channel_teacher,channel_people):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"INSERT INTO user_partners VALUES (?,?)", (channel_teacher,channel_people))
    db.commit()


def cheak_partner_channels(channels): #проверка есть ли у данного канала учитель
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT channel_teacher FROM user_partners WHERE channel_people ='{channels}'").fetchone()
    if a == None:
        return 0
    else:
        return a[0]

def info_partners():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f'SELECT * FROM user_partners').fetchall()
    return a

def delit_partners(name_channel):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT channel_people FROM user_partners WHERE channel_people ='{name_channel}'").fetchone()
    if a == None:
        return 0
    else:
        sql.execute(f'DELETE FROM user_partners WHERE channel_people ="{name_channel}"')
        db.commit()
        return 1

def obnovatrafika(channel1,channel2,channel3):
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sql.execute(f"UPDATE trafik SET parametr= '{channel1}' WHERE chanel = 'channel1'")
    sql.execute(f"UPDATE trafik SET parametr= '{channel2}' WHERE chanel = 'channel2'")
    sql.execute(f"UPDATE trafik SET parametr= '{channel3}' WHERE chanel = 'channel3'")
    db.commit()

def cheak_traf():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    c1 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel1'").fetchone()[0]
    c2 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel2'").fetchone()[0]
    c3 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel3'").fetchone()[0]
    list = [c1,c2,c3]
    return list