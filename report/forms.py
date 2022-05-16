from django import forms

from .models import ReportType
from user.models import User


class ReportForm(forms.Form):
    display_field = forms.ChoiceField(choices=ReportType.TYPES)
    user = forms.ModelChoiceField(queryset=User.objects.all())
