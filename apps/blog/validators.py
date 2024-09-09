from django.core.exceptions import ValidationError


def capitalize_words(value):
    if value:
        return value.title()
    return value