from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


def textfield_not_empty(textfield):
    """
    Validates that a text field is not empty after stripping whitespace and HTML tags.
    """
    cleaned_data = strip_tags(textfield).replace("&nbsp;", "").strip()
    if not cleaned_data:
        raise ValidationError("Please fill in this field")
