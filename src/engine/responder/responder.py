from engine.intention.detector import Detector
from engine.intention.intention import Intention
from bc3bot import bc3bot


class Responder:
    def __init__(self, bot_instance: bc3bot.Bot):
        self._bot = bot_instance
        self._detector = Detector(bot_instance)


    def respond(self, message: str, campfire_alias: str, sender: str):
        intent = self._detector.detect(message)
        response_message = ""
        if intent == Intention.GREETING:
            response_message = f"สวัสดีจ้า {sender}"
        elif intent == Intention.POKE:
            response_message = f"เรียก {self._bot.name()} ทำไมจ๊ะ"
        if response_message != "":
            self._bot.send_message_to_campfire(response_message, campfire_alias)
