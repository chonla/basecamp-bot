from engine.intention.detector import Detector
from engine.intention.intention import Intention
from bc3bot import bc3bot
import logging


class Responder:
    def __init__(self, bot_instance: bc3bot.Bot):
        self._bot = bot_instance
        self._detector = Detector(bot_instance)
        logging.basicConfig(level=bot_instance.log_level())


    def respond(self, message: str, campfire_alias: str, sender: str):
        clean_message, intent = self._detector.detect(message)
        logging.debug(f"{clean_message} -> {intent}")
        response_message = ""
        if intent == Intention.GREETING:
            response_message = f"สวัสดีจ้า {sender}"
        elif intent == Intention.POKE:
            response_message = f"เรียก {self._bot.name()} ทำไมจ๊ะ"
        if response_message != "":
            self._bot.send_message_to_campfire(response_message, campfire_alias)
