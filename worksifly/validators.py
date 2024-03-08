from django.core.exceptions import ValidationError

def textfield_not_empty(value):
    """Validates that a TextField is not empty."""
    if value == '' or value is None:
        raise ValidationError('This field cannot be empty.')
