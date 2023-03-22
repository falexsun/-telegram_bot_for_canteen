import telebot
import sqlite3
import datetime
from telebot import types
from config import token


# db = sqlite3.connect("base.db",  check_same_thread=False)
# c = db.cursor()
# в каждой функции вызываю новый для оптимизации

bot = telebot.TeleBot(token)

##################
##==============##
##~Главное меню~##
##==============##
##################
@bot.message_handler(commands=['start', 'menu'])
def starts(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Сформировать информацию')
    item2 = types.KeyboardButton('Заполнить списки')

    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Выберете действие', reply_markup=markup)



################################################
##============================================##
##~Логика после главного меню, основная хрень~##
##============================================##
################################################
@bot.message_handler(content_types='text')
def bot_message(message):
    if message.text == 'Заполнить списки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('9A')
        item2 = types.KeyboardButton('9B')
        item3 = types.KeyboardButton('10A')
        item4 = types.KeyboardButton('10B')
        item5 = types.KeyboardButton('11A')
        item6 = types.KeyboardButton('11B')
        item7 = types.KeyboardButton('/menu')

        markup.add(item1, item2, item3, item4, item5, item6, item7)

        mesg = bot.send_message(message.chat.id, 'Выберете класс', reply_markup=markup)
        bot.register_next_step_handler(mesg, main_menu)
    #######################################################################
    elif message.text == 1:
        pass


    #######################################################################
    elif message.text == 'Сформировать информацию':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        db = sqlite3.connect("base.db", check_same_thread=False)
        c = db.cursor()
        today = datetime.date.today()
        c.execute("""SELECT date FROM attendance_log order by date asc limit 1""")

        start = c.fetchone()[0]
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        start = start.date()

        c.execute("""SELECT date FROM attendance_log order by date desc limit 1""")
        finish = c.fetchone()[0]
        finish = datetime.datetime.strptime(finish, "%Y-%m-%d")
        finish = finish.date()

        db.close()
        if (int(str(today - start).split()[0]) <= 0):
            day1 = start
            day2 = start + datetime.timedelta(days=1)
        elif (int(str(today - start).split()[0]) > 0 and int(str(today - finish).split()[0]) < 2):
            day1 = today
            day2 = today + datetime.timedelta(days=1)
        else:
            day1 = finish
            day2 = finish - datetime.timedelta(days=1)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(str(day1))
        item2 = types.KeyboardButton(str(day2))
        markup.add(item1, item2)
        mesg = bot.send_message(message.chat.id, 'Выберете дату или поставьте свою в формате гггг-мм-дд ПРИМЕР: 2022-09-01', reply_markup=markup)
        bot.register_next_step_handler(mesg, formation_of_lists)



###################################################################
##===============================================================##
##~~##
##===============================================================##
###################################################################
def main_menu (message):
    klass = message.text
    if klass == "/menu":
        starts(message)

    else:
        db = sqlite3.connect("base.db", check_same_thread=False)
        c = db.cursor()
        today = datetime.date.today()
        c.execute("""SELECT date FROM attendance_log order by date asc limit 1""")

        start = c.fetchone()[0]
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        start = start.date()

        c.execute("""SELECT date FROM attendance_log order by date desc limit 1""")
        finish = c.fetchone()[0]
        finish = datetime.datetime.strptime(finish, "%Y-%m-%d")
        finish = finish.date()

        db.close()

        print(int(str(today - start).split()[0].split(":")[0]))

        # if (int(str(today - start).split()[0]) <= 0):
        #     day1 = start
        #     day2 = start + datetime.timedelta(days=1)
        # elif (int(str(today - start).split()[0]) < 0 and int(str(today - finish).split()[0]) > 2 ):
        #     day1 = today
        #     day2 = today + datetime.timedelta(days=1)
        # else:
        #     day1 = finish
        #     day2 = finish - datetime.timedelta(days=1)


        if (int(str(today - start).split()[0]) <= 0):
            day1 = start
            day2 = start + datetime.timedelta(days=1)
        elif (int(str(today - start).split()[0]) > 0 and int(str(today - finish).split()[0]) < 2):
            day1 = today
            day2 = today + datetime.timedelta(days=1)
        else:
            day1 = finish
            day2 = finish - datetime.timedelta(days=1)

        # if (int(str(today - start).split()[0].split(":")[0]) <= 0):
        #     day1 = start
        #     day2 = start + datetime.timedelta(days=1)
        # elif (int(str(today - start).split()[0].split(":")[0])< 0 and int(str(today - finish).split()[0].split(":")[0]) > 2 ):
        #     day1 = today
        #     day2 = today + datetime.timedelta(days=1)
        # else:
        #     day1 = finish
        #     day2 = finish - datetime.timedelta(days=1)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(str(day1))
        item2 = types.KeyboardButton(str(day2))
        markup.add(item1, item2)
        mesg = bot.send_message(message.chat.id, 'Выберете дату или поставьте свою в формате гггг-мм-дд ПРИМЕР: 2022-09-01', reply_markup=markup)
        bot.register_next_step_handler(mesg, chose_date, klass)


###################################################################
##===============================================================##
##~~##
##===============================================================##
###################################################################
def chose_date(message, klass):
    date = message.text
    print(klass)
    print(message.text)
    l = list()
    db = sqlite3.connect("base.db", check_same_thread=False)
    c = db.cursor()
    c.execute(f"SELECT name FROM pupils WHERE class = '{klass}'")
    li = c.fetchall()
    for i in range(len(li)):
        l.append(li[i][0])
    print(l)
    del li
    l_number = list()
    for i in l:
        c.execute(f"SELECT id FROM pupils WHERE name = '{i}'")
        l_number.append(c.fetchone()[0])
    print(l_number)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in l:
        i = types.KeyboardButton(i)
        markup.add(i)
    i = types.KeyboardButton('/menu')
    markup.add(i)
    bot.send_message(message.chat.id, "Выберете отсутствующих", reply_markup=markup)
    nety = list()
    c.execute(f"SELECT * FROM attendance_log WHERE date = '{date}'")
    k = c.fetchone()[2:]
    k = list(k)
    print(l)
    print(l_number)
    print(k)

    for i in l_number:
        if k[i - 1] == 0:
            nety.append(l[l_number.index(i)])
    print(nety)
    if len(nety) != 0:
        nety_str = str()
        for i in nety:
            nety_str += f"{i}, "
        nety_str = nety_str[:-2]
        bot.send_message(message.chat.id, f"В этот день отсутствуют")
        mesg = bot.send_message(message.chat.id, nety_str)
    else:
        mesg = bot.send_message(message.chat.id, "Отсутствующих нет")
    bot.register_next_step_handler(mesg, chose_men_next, klass, date, l, l_number, k)
    db.close()


###################################################################
##===============================================================##

##===============================================================##
###################################################################
def chose_men_next(message, klass, date, l, l_number, k):
    if message.text not in l and message.text != '/menu':
        bot.send_message(message.chat.id, "Нет такого человека O_o")
        mesg = bot.send_message(message.chat.id, "Выберете человека")
        bot.register_next_step_handler(mesg, chose_men_next, klass, date, l, l_number, k)
    elif message.text == "/menu":
        starts(message)
    else:
        db = sqlite3.connect("base.db", check_same_thread=False)
        c = db.cursor()

        name = message.text
        number = l_number[l.index(name)]

        b = k[number - 1]
        if b == 1 or b == None:
            c.execute(f"UPDATE attendance_log SET '{number}'=False WHERE date = '{date}'")
        else:
            c.execute(f"UPDATE attendance_log SET '{number}'=True WHERE date = '{date}'")

        db.commit()


        l = list()
        c.execute(f"SELECT name FROM pupils WHERE class = '{klass}'")
        li = c.fetchall()
        for i in range(len(li)):
            l.append(li[i][0])
        print(l)
        del li
        l_number = list()
        for i in l:
            c.execute(f"SELECT id FROM pupils WHERE name = '{i}'")
            l_number.append(c.fetchone()[0])
        print(l_number)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in l:
            i = types.KeyboardButton(i)
            markup.add(i)
        i = types.KeyboardButton('/menu')
        markup.add(i)
        bot.send_message(message.chat.id, "Выберете отсутствующих", reply_markup=markup)
        nety = list()
        c.execute(f"SELECT * FROM attendance_log WHERE date = '{date}'")
        k = c.fetchone()[2:]
        k = list(k)
        print(l)
        print(l_number)
        print(k)

        for i in l_number:
            if k[i - 1] == 0:
                nety.append(l[l_number.index(i)])
        print(nety)
        if len(nety) != 0:
            nety_str = str()
            for i in nety:
                nety_str += f"{i}, "
            nety_str = nety_str[:-2]
            bot.send_message(message.chat.id, f"В этот день отсутствуют")
            mesg = bot.send_message(message.chat.id, nety_str)
        else:
            mesg = bot.send_message(message.chat.id, "Отсутствующих нет")
        bot.register_next_step_handler(mesg, chose_men_next, klass, date, l, l_number, k)

        db.close()





###################################################################
##===============================================================##
##~Часть программы отвечающая за формирование готовой информации~##
##===============================================================##
###################################################################




# def generate_information(message):
#     db = sqlite3.connect("base.db", check_same_thread=False)
#     c = db.cursor()
#     date = message.text
#     c.execute("""select MAX(number_table) from pupils""")
#     tables = int(c.fetchone()[0])
#     c.execute("""select MAX(id) from pupils""")
#     maxs = int(c.fetchone()[0])
#     l = list()
#     for i in range (1, maxs + 1):
#         pass
#     db.close()

def formation_of_lists(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('/menu')
    markup.add(item1)
    bot.send_message(message.chat.id, "Информация о количестве человек за столом",  reply_markup=markup)
    db = sqlite3.connect("base.db", check_same_thread=False)
    c = db.cursor()
    date = message.text
    c.execute(f"SELECT * FROM attendance_log WHERE date = '{date}'")
    challenger = c.fetchone()[2:]
    choice = list()
    for i in range(len(challenger)):
        if challenger[i] == 1: #0 or challenger[i] == None:
            choice.append(i + 1)
    c.execute("""select MAX(number_table) from pupils""")
    tables = int(c.fetchone()[0])
    tb1 = [0] * tables  # заполнение столов 1 смены
    tb2 = [0] * tables  # заполнение столов 2 смены
    for i in choice:
        c.execute(f"SELECT number_table FROM pupils WHERE id = '{i}' and shift = 1")
        tb1[c.fetchone()[0] - 1] += 1
        c.execute(f"SELECT number_table FROM pupils WHERE id = '{i}' and shift = 2")
        tb2[c.fetchone()[0] - 1] += 1
    # вывод в меню не идеально, но хоть что-то#
    # UPD уже всё классно#
    for i in range(len(tb1)):
        bot.send_message(message.chat.id, f"стол {i + 1}: {tb1[i]} человек(а)")
    for i in range(len(tb2)):
        bot.send_message(message.chat.id, f"стол {i + 1}: {tb2[i]} человек(а)")


bot.polling(none_stop=True)