import re
from django.core.exceptions import ValidationError


def validate_username(username):
    username = username.lower()
    
    if len(username) < 3 or len(username) > 30:
        raise ValidationError("Username must be between 3 and 30 characters long.")
    
    if not re.match(r'^\w+$', username):
        raise ValidationError("Username can only contain letters, numbers, and underscores.")
    
    if not username[0].isalpha():
        raise ValidationError("Username must start with a letter.")
    
    return username


def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r'[0-9]', password):
        raise ValidationError("Password must contain at least one digit.")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")

    return password


def capitalize_name(name):
    return name.capitalize() if name else name