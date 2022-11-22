from engine.intention.intention import Intention
from bc3bot import bc3bot
import re
from functools import reduce


class Detector:
    def __init__(self, bot_instance: bc3bot.Bot):
        self._bot = bot_instance
        self._trigger = bot_instance.trigger()

    def detect(self, message: str) -> tuple[str, Intention]:
        clean_message = self._clean(message)
        if clean_message == self._trigger:
            return clean_message, Intention.POKE
        if  clean_message == "สวัสดี" or \
            clean_message == "หวัดดี":
            return clean_message, Intention.GREETING
        if  clean_message.endswith("คืออะไร") or \
            clean_message.startswith("ขอ") or \
            clean_message.startswith("อยากได้"):
            return clean_message, Intention.INQUIRY
        return clean_message, Intention.UNKNOWN

    def _clean(self, message: str) -> str:
        message = message.strip()

        to_be_removed = [
            r"หน่อยจ้า$",
            r"หน่อยครับ$",
            r"หน่อยค่ะ$",
            r"หน่อยค้าบ$",
            r"นะจ๊ะ$",
            r"นะคะ$",
            r"นะครับ$",
            r"นะค้าบ$",
            r"ครับ$",
            r"ค้าบ$",
            r"ค่ะ$",
            r"จ้ะ$",
            r"จ้า$",
            r"จ๋า$"
        ]
        cleaned_message = reduce(lambda acc, pat: re.sub(pat, "", acc, flags=re.U), to_be_removed, message)
        return cleaned_message
