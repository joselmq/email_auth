from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from itertools import cycle
import re


@deconstructible
class RutValidator:

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, rut):
        if not re.match('[0-9]{7,9}[-][\dKk]$', str(rut)):
            raise ValidationError(self.message, code=self.code, params={'value': rut})

        number, validator = rut.split('-')
        reversed_digits = map(int, reversed(str(number)))
        factors = cycle(range(2, 8))
        val = -sum(d * f for d, f in zip(reversed_digits, factors)) % 11

        if val == 10 and not validator == 'k':
            raise ValidationError(self.message, code=self.code, params={'value': rut})
        if str(val) == validator:
            return
        raise ValidationError(self.message, code=self.code, params={'value': rut})


validate_rut = RutValidator()