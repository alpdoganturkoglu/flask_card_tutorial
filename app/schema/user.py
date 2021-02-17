import typing
import re
from dataclasses import dataclass

email_regex: str = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
password_regex: str = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"


@dataclass
class LoginSchema:

    email: str
    password: str

    def validate_login(self) -> bool:
        if self.validate_email() and self.password:
            return True
        return False

    def validate_password(self) -> bool:
        if re.search(password_regex, self.password):
            return True
        return False

    def validate_email(self) -> bool:
        if re.search(email_regex, self.email):
            return True
        else:
            return False


@dataclass
class RegisterSchema:

    email: str
    password: str
    password2: str

    def validate_password(self) -> bool:
        if re.search(password_regex, self.password) and self.password == self.password2:
            return True
        return False

    def validate_register(self) -> bool:
        if self.validate_password() and self.validate_email():
            print(self.validate_password())
            return True
        return False

    def validate_email(self) -> bool:
        if re.search(email_regex, self.email):
            return True
        else:
            return False


