from django import forms

from user.models import Person


class PersonTagForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Person.objects.all())
    tag_title = forms.CharField(required=False)
