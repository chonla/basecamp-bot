from enum import Enum


class Intention(Enum):
    UNKNOWN = "unknown"
    POKE = "poke" # When someone call bot
    GREETING = "greeting" # When someone greet
    INQUIRY = "inquiry" # When someone ask for something