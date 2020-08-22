from django.db.models import Model as DefaultModel
from safedelete.models import SafeDeleteModel


class Model(DefaultModel):
    class Meta:
        abstract = True

    @staticmethod
    def choices_help_text(choices):
        return "<br>".join([f"`{item[0]}`: {item[1]}\n" for item in choices])


class SafeDeleteHistoryModel(SafeDeleteModel):
    pass
