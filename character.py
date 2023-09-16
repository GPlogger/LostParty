from enum import Enum


class CharacterType(Enum):
    SUPPORTER = 1
    DEALER = 2


class Character:
    support_jobs = ["바드", "도화가", "홀리나이트"]

    def __init__(self, user_name, char_name, char_class, item_level):
        self.user_name = user_name
        self.char_name = char_name
        self.char_class = char_class
        self.item_level = int(float(item_level.replace(",", "")))
        self.type = CharacterType.SUPPORTER if char_class in self.support_jobs else CharacterType.DEALER

    def __str__(self) -> str:
        to_print = [value.name if isinstance(value, Enum) else value for key, value in self.__dict__.items()]
        return f"{list(to_print)}"

    def is_supporter(self):
        return self.type == CharacterType.SUPPORTER

    @classmethod
    def load(cls, character_data):
        return cls(
            character_data["Name"],
            character_data["CharacterName"],
            character_data["CharacterClassName"],
            character_data["ItemMaxLevel"],
        )
