from django.db import models
from itertools import cycle
import re

from company import validators


def _check_validator_number(*args):
    rut = ''
    for value in args:
        rut = value
        continue

    if not re.match('[0-9]{7,9}[-][\dKk]$', str(rut)):
        return False

    number, validator = rut.split('-')
    reversed_digits = map(int, reversed(str(number)))
    factors = cycle(range(2, 8))
    val = -sum(d * f for d, f in zip(reversed_digits, factors)) % 11

    if val == 10 and validator == 'k':
        return True
    if str(val) == validator:
        return True
    return False


class RutField(models.Field):
    default_validators = [validators.validate_rut]
    description = "An integer number and a validator number separated by (-)"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 11)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # We do not exclude max_length if it matches default as we want to change
        # the default in future.
        return name, path, args, kwargs
