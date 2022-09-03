from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class UsernameSimbolsValidator(RegexValidator):
    regex = r"^[\w.@+-]+$"


def username_me_valdator(value):
    if value.lower() == "me":
        raise ValidationError(
            "Имя 'me' недопустимо.",
            params={"value": value},
        )
