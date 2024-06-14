from enum import Enum


class LoginChooseResponseType(str, Enum):
    SUPER_ADMIN_CHOOSE = "SUPER_ADMIN_CHOOSE"

    def __str__(self) -> str:
        return str(self.value)
