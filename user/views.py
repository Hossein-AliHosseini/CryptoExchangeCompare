from django.contrib.auth import (login,
                                 logout,
                                 update_session_auth_hash,
                                 authenticate)
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.utils.http import urlsafe_base64_decode
from django.conf import settings

from .forms import CustomUserCreationForm, ProfileForm
from .models import User
from .token import account_activation_token


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                user = User.objects.get(username=username)
                user.is_active = False
                send_sms = form.cleaned_data.get('send_sms')
                user.send_activation_link(send_sms)
                return HttpResponse('Check your Email to activate your account')
        else:
            form = CustomUserCreationForm()
        return render(request, 'user/signup.html', {'form': form})
    else:
        return HttpResponse("You have signed up before!")


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username,
                                    password=password)
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Please Activate your account first!')
        else:
            form = AuthenticationForm()
        return render(request,
                      'user/login.html',
                      {'form': form})
    else:
        return HttpResponse('You have logged in before!')


def activate(request, eid, token):
    try:
        uid = urlsafe_base64_decode(eid).decode('utf-8')
        user = User.objects.get(email=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print(token)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation.\
            Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def password_reset_request(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                email = password_reset_form.cleaned_data['email']
                associated_users = User.objects.get(email=email)
                associated_users.send_change_password_link()
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="user/password_reset.html",
                      context={"password_reset_form": password_reset_form})
    else:
        return HttpResponse('Please login first...')


def logout_view(request):
    logout(request)
    return redirect('home')


def profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        person = request.user.person
        if request.method == "POST":
            form = ProfileForm(request.POST)
            if form.is_valid():
                person.phone_number = form.cleaned_data['phone_number']
                person.address = form.cleaned_data['address']
                person.save()
        else:
            form = ProfileForm(initial={
                'email': user.email,
                'password': user.password,
                'phone_number': person.phone_number,
                'address': person.address,
                'national_code': person.national_code,
                'birth_date': person.birthdate
            })
        return render(request, 'user/profile.html',
                      {'person': person,
                       'form': form,
                       'MEDIA_URL': settings.MEDIA_URL})
    else:
        return HttpResponse('Please login first...')
