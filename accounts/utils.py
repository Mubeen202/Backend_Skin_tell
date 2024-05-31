from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email
from typing import Tuple

def validate_email(value: str) -> Tuple[bool, str]:
    """Validate a single email."""
    message_invalid = 'Enter a valid email address.'

    if not value:
        return False, message_invalid
    # Check the regex, using the validate_email from django.
    try:
        django_validate_email(value)
    except ValidationError:
        return False, message_invalid

    return True, ''
