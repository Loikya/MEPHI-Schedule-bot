from schedule_parser import get_schedule
from dateutil import parser
import datetime
from config import mmessage, OW_API_key
from pyowm import OWM

def send_mesg(vk, vk_id, chat_flag, text):
    if(chat_flag):
        vk.messages.send(chat_id=vk_id, message=text)
    else:
        vk.messages.send(user_id=vk_id, message=text)

def send_schedule(vk_id, vk, chat_flag, msg):
    send_mesg(vk, vk_id, chat_flag, "Расписание подготавливается...")
    config = msg.split()
    if(len(config)>1):
        date = config[0]
        group = config[1]
    else:
        date=config[0]
        group = "Б14-501"
    try:
        date=parser.parse(date, dayfirst=True)
        schedule = get_schedule(group, date.strftime("%Y-%m-%d"))
    except ValueError as error:
        text = "⚠ Произошла ошибка, вероятно вы ввели неправильную дату. Соблюдайте следующий формат: ДД.ММ.ГГ (ДД/ММ/ГГ)"
        send_mesg(vk, vk_id, chat_flag, text)
        return
    except Exception as error:
        text = "Произошла ошибка: " + str(error)
        send_mesg(vk, vk_id, chat_flag, text)
        return
    text = ""
    for subj in schedule:
        text=text+"[%s] [%s] %s {%s} |%s|\n"%(subj['time'], subj['type'], subj['name'], subj['room'], subj['lecturers'])
    send_mesg(vk, vk_id, chat_flag, text)

def send_today(vk_id, vk, chat_flag, msg):
    send_mesg(vk, vk_id, chat_flag, "Расписание подготавливается...")
    if msg is not None:
        group=msg
    else:
        group = "Б14-501"
    try:
        date=datetime.date.today()
        schedule = get_schedule(group, date.strftime("%Y-%m-%d"))
    except Exception as error:
        text = "Произошла ошибка: " + str(error)
        send_mesg(vk, vk_id, chat_flag, text)
        return
    text = ""
    for subj in schedule:
        text=text+"[%s] [%s] %s {%s} |%s|\n"%(subj['time'], subj['type'], subj['name'], subj['room'], subj['lecturers'])
    send_mesg(vk, vk_id, chat_flag, text)

def send_tomorrow(vk_id, vk, chat_flag, msg):
    send_mesg(vk, vk_id, chat_flag, "Расписание подготавливается...")
    if msg is not None:
        group=msg
    else:
        group = "Б14-501"
    try:
        date=datetime.date.today()+ datetime.timedelta(days=1)
        schedule = get_schedule(group, date.strftime("%Y-%m-%d"))
    except Exception as error:
        text = "Произошла ошибка: " + str(error)
        send_mesg(vk, vk_id, chat_flag, text)
        return
    text = ""
    for subj in schedule:
        text=text+"[%s] [%s] %s {%s} |%s|\n"%(subj['time'], subj['type'], subj['name'], subj['room'], subj['lecturers'])
    send_mesg(vk, vk_id, chat_flag, text)

def morning_messages(vk_id, vk, chat_flag, group):
    owm = OWM(OW_API_key, language='ru')
    obs = owm.weather_at_place('Moscow,RU') 
    weather = obs.get_weather()
    temp = weather.get_temperature(unit='celsius')['temp']
    status = weather.get_detailed_status() 
    schedule = get_schedule(group)
    sc_text = ""
    for subj in schedule:
        sc_text=sc_text+"[%s] [%s] %s {%s} |%s|\n"%(subj['time'], subj['type'], subj['name'], subj['room'], subj['lecturers'])
    text = mmessage%(sc_text, temp, status)
    send_mesg(vk, vk_id, chat_flag, text)

commands = ((u'!расписание',send_schedule),
            (u'!сегодня',send_today),
            (u'!завтра',send_tomorrow),
            (u'!пост',morning_messages),)

def parse_message(msg):
    #msg = msg.lower()
    if msg[0] == '!':
        return msg.split(" ", 1)
    else:
        return [u'***', '']

def run_msg(vk, vk_id, message, chat_flag):
    res = parse_message(message)
    for command in commands:
        if (res[0] == command[0]):
            try:
                command[1](vk_id, vk, chat_flag, res[1] if len(res)>1 else None)
                return

            except Exception as error:
                err_m = u'Что то пошло не так. Попробуйте повторить запрос или свяжитесь с администратором'
                send_mesg(vk, vk_id, chat_flag, err_m)
                print(error)