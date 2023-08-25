from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.validators import validate_email
import re

def c_validate_email(value):
    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError("Invalid email address.")

def validate_username(value):
    # Custom validation for the username
    if not re.match(r'^\w+$', value):
        raise ValidationError("Username can only contain alphanumeric characters and underscores.")

    # Check if the username is already taken
    if User.objects.filter(username=value).exists():
        raise ValidationError("Username already exists.")

def validate_phone_number(value):
    # Custom validation for the phone number
    phone_regex = r'^\+?1?\d{9,15}$'
    phone_validator = RegexValidator(regex=phone_regex, message="Enter a valid phone number.")
    phone_validator(value)
