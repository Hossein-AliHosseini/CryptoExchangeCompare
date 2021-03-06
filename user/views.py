from django.contrib.auth import (login,
                                 logout,
                                 authenticate)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.utils.http import urlsafe_base64_decode
from django.conf import settings

from .forms import CustomUserCreationForm, ProfileForm
from .models import User, ActivateUserToken
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
                user.save()
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
    if user is not None and ActivateUserToken.objects.filter(eid=eid).last().token == token:
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation.\
            Now you can login to your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='/users/login/')
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            associated_users = User.objects.get(email=email)
            associated_users.send_change_password_link()
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="user/password_reset.html",
                  context={"password_reset_form": password_reset_form})


@login_required(login_url='/users/login/')
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/users/login/')
def profile_view(request):
    user = request.user
    person = request.user.person
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            person.phone_number = form.cleaned_data['phone_number']
            person.address = form.cleaned_data['address']
            person.profile_image = form.cleaned_data['profile_image']
            person.save()
    else:
        form = ProfileForm(initial={
            'email': user.email,
            'phone_number': person.phone_number,
            'address': person.address,
            'national_code': person.national_code,
            'birthdate': person.birthdate,
            'profile_image': person.profile_image
        })
    return render(request, 'user/profile.html',
                  {'person': person,
                   'form': form,
                   'MEDIA_URL': settings.MEDIA_URL})
