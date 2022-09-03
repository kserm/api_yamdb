from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class UsernameSimbolsValidator(RegexValidator):
    regex = r"^[\w.@+-]+$"


def validate_name_me(value):
    if value.lower() == "me":
        raise ValidationError(
            "Имя 'me' недопустимо.",
            params={"value": value},
        )
