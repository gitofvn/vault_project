import re
from django.core.exceptions import ValidationError

def validate_phone_number(value):
    pattern = r'^\+?[0-9\s\-]+$'
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid phone number (digits, spaces, dashes, optional +).")
