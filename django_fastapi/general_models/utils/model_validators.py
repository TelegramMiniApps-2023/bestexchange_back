from django.core.exceptions import ValidationError


def is_positive_validate(value: int):
    if value < 0:
        raise ValidationError(f'Частота должна быть положительной, передано: {value}')