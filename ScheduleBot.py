# coding=UTF-8

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import time
import config
from commands import run_msg




def main():

    vk_session = vk_api.VkApi(config.login, config.password)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
     
    vk = vk_session.get_api()
    print("Ready!")

    while True:
        try:
            longpoll = VkLongPoll(vk_session)

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if(event.from_chat):
                        run_msg(vk, event.chat_id, event.text, True)
                    else:
                        run_msg(vk, event.user_id, event.text, False)
        except Exception as error:
                text = "Произошла ошибка: " + str(error)
                vk.messages.send(user_id=96494615, message=text)
                print(error)

    #while (True):
    #    try:
    #        poll = gbot.messages.getLongPollServer()
    #        r = requests.request("GET", "http://" + poll['server'] + "?act=a_check&key=" + poll['key'] + "&ts=" + str(
    #            poll['ts']) + "&wait=10&mode=2", timeout=50)
    #        mesg_poll = r.json()
    #        for mesg in mesg_poll['updates']:
    #            run_msg(mesg, gbot)
    #    except Exception as e:
    #        print("Error: {0}".format(e))
    #        time.sleep(4)



if __name__ == '__main__':
    main()
