from django import forms
from django.contrib import admin

from members.models import User
from .models import Player, Position


class PlayerForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.order_by('name'))

    class Meta:
        model = Player
        fields = '__all__'


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    form = PlayerForm


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass
