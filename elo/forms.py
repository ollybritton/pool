import datetime

from django import forms
from .models import Player, Frame

class AddForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = Frame
        fields = ["winning_player", "losing_player", "breaking_player", "date"]
