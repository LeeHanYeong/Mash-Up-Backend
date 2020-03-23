from django.db.models import CharField
from simple_history.models import HistoricalRecords


class ChoiceField(CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.choices and not self.help_text:
            self.help_text = '<br>'.join([f'`{item[0]}`: {item[1]}\n' for item in self.choices])


class DiffHistoricalRecords(HistoricalRecords):
    pass
