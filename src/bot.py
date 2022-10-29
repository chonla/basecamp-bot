"""Bot

A main bot application.
"""

from bc3bot import config, bc3bot
import sys

from bc3bot import bc3bot, hook


def new_messages_event_callback(bot_instance: bc3bot.Bot, params: any):
    print(params)


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
    bot.enter_campfire('playground')
    
    # bot.send_message_to_campfire('ทดสอบโพสต์ด้วย bot', 'playground')
