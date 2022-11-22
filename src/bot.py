"""Bot

A main bot application.
"""

from bc3bot import config, bc3bot
import sys

from bc3bot import bc3bot, hook
from engine.responder.responder import Responder


def enter_campfire_event_callback(bot_instance: bc3bot.Bot, params: any):
    bot_instance.send_message_to_campfire(f'สวัสดีจ้า {bot_instance.name()} มาแล้วจ้า', params["campfire_alias"])

def exit_campfire_event_callback(bot_instance: bc3bot.Bot, params: any):
    bot_instance.send_message_to_campfire(f'{bot_instance.name()} ไปก่อนน้า..', params["campfire_alias"])

def new_messages_event_callback(bot_instance: bc3bot.Bot, params: any):
    responder = Responder(bot_instance)
    message = params["messages"][0]["message"]
    room = params["campfire_alias"]
    sender = params["messages"][0]["sender"]["name"]
    responder.respond(message, room, sender)

if __name__ == '__main__':
    try:
        conf = config.Config('bot.yaml')
    except FileNotFoundError as err:
        print(err)
        sys.exit()

    try:
        auth = config.Config('.botrc')
    except FileNotFoundError as err:
        print(err)
        print('You may need to run "bot auth" to authorize the bot.')
        sys.exit()

    bot = bc3bot.Bot(auth, conf)

    bot.add_hook(hook.Hook.NEW_MESSAGE, new_messages_event_callback)
    bot.add_hook(hook.Hook.ENTER_CAMPFIRE, enter_campfire_event_callback)
    bot.add_hook(hook.Hook.EXIT_CAMPFIRE, exit_campfire_event_callback)
    bot.enter_campfire('playground')
    
    # bot.send_message_to_campfire('ทดสอบโพสต์ด้วย bot', 'playground')
