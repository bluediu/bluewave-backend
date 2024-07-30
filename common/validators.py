from django.core.validators import RegexValidator


class NumericStringValidator(RegexValidator):
    """Numeric string validator."""

    code = "numeric_string"
    message = "Value must be numeric."

    def __init__(self, message: str = None):
        """Convert numeric string validator."""
        super().__init__(regex="[^0-9]+", inverse_match=True, message=message)
