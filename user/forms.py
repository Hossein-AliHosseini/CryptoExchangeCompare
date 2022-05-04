from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User, Person


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Username")
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    national_code = forms.IntegerField(label='National Code')
    phone_number = forms.CharField(label='Phone Number')
    birthdate = forms.DateField(label='Birth Date')
    send_sms = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'username',
                  'first_name', 'last_name',
                  'birthdate', 'phone_number', 'national_code',
                  'send_sms')

    def save(self, commit=False):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.save()
        user.email = self.cleaned_data['email']
        person = Person.objects.create(
            user=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            national_code=self.cleaned_data['national_code'],
            birthdate=self.cleaned_data['birthdate'],
            phone_number=self.cleaned_data['phone_number']
        )
        if commit:
            person.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["readonly"] = True
        self.fields["national_code"].widget.attrs["readonly"] = True
        self.fields["birthdate"].widget.attrs["readonly"] = True

    # profile_image = forms.ImageField()
    email = forms.EmailField()
    # phone_number = forms.IntegerField()
    # national_code = forms.IntegerField()
    # address = forms.CharField()
    # birthdate = forms.DateField()

    class Meta:
        model = Person
        fields = ['profile_image', 'phone_number', 'national_code', 'address', 'birthdate']
