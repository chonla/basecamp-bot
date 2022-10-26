"""Bot

A main bot application.
"""

from .bc3bot import config


if __name__ == '__main__':
    conf = config.Config('bot.yaml')
    print('ok')
