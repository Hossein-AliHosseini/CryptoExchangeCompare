from django import forms

from .models import ExchangeChoice, Crypto


class AccountForm(forms.Form):
    exchange = forms.ChoiceField(choices=ExchangeChoice.TYPES)
    exchange_email = forms.EmailField(max_length=128)
    exchange_phone_number = forms.IntegerField(max_value=99999999999)
    exchange_password = forms.CharField(max_length=128)
    token = forms.CharField(max_length=128, help_text="Optional", required=False)
    wallet_address = forms.CharField(max_length=128, help_text="Optional", required=False)


class ProfitAndLossForm(forms.Form):
    ranged_show = forms.BooleanField(required=False)
    range_start = forms.DateTimeField(required=False)
    range_end = forms.DateTimeField(required=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not self.fields['ranged_show']:
    #         self.fields['range_start'].disabled = True
    #         self.fields['range_end'].disabled = True


class ChoiceExchangeForm(forms.Form):
    currency = forms.ChoiceField(choices=Crypto.TYPES)
