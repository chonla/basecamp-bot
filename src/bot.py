"""Bot

A main bot application.
"""

from bc3bot import config, bc3bot
import sys


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

    bot.enter_campfire('playground')
    
    # bot.send_message_to_campfire('ทดสอบโพสต์ด้วย bot', 'playground')
