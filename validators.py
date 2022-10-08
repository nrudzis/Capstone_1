"""Custom validators."""

from wtforms.validators import ValidationError

class Unique(object):
    """Validator to verify that field is unique."""
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = 'Error: Unique constraint violation.'
        self.message = message

    def __call__(self, form, field):
        is_duplicate = self.model.query.filter(self.field == field.data).first()
        if is_duplicate:
            raise ValidationError(self.message)
