from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(
            gettext_lazy('значение должно быть >= 1'),
            params={'value': value},
        )
