from django import forms

from .models import ExchangeChoice


class AccountForm(forms.Form):
    exchange = forms.ChoiceField(choices=ExchangeChoice.TYPES)
    exchange_email = forms.EmailField(max_length=128)
    exchange_phone_number = forms.IntegerField(max_value=99999999999)
    exchange_password = forms.CharField(max_length=128)
