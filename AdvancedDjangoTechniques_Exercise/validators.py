from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def check_spaces_letters_validator(value: str):
    for char in value:
        if not char.isalpha() or char != ' ':
            raise ValidationError('Name can only contain letters and spaces')

