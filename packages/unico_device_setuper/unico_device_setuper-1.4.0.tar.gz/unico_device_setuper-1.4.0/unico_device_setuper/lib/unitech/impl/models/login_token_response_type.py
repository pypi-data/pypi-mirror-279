from enum import Enum


class LoginTokenResponseType(str, Enum):
    USER_AUTH = "USER_AUTH"

    def __str__(self) -> str:
        return str(self.value)
