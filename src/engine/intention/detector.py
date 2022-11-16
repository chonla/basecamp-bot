from engine.intention.intention import Intention
from bc3bot import bc3bot


class Detector:
    def __init__(self, bot_instance: bc3bot.Bot):
        self._bot = bot_instance
        self._trigger = bot_instance.trigger()

    def detect(self, message: str) -> Intention:
        if message == self._trigger:
            return Intention.POKE
        if  message == "สวัสดี" or \
            message == "สวัสดีจ้า" or \
            message == "สวัสดีจ้ะ" or \
            message == "สวัสดีครับ" or \
            message == "สวัสดีค่ะ" or \
            message == "สวัสดีค่า":
            return Intention.GREETING
        return Intention.UNKNOWN