import requests
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import *


class PersonSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('_token')
    is_complete = serializers.SerializerMethodField('_is_complete')
    email = serializers.SerializerMethodField('_email')

    @staticmethod
    def _is_complete(obj: Person):
        return obj.is_complete

    @staticmethod
    def _email(obj: Person):
        return obj.user.email

    @staticmethod
    def _token(obj: Person):
        return Token.objects.get(user=obj.user).key

    class Meta:
        model = Person
        exclude = ['user', 'id', ]


class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)

    phone_number = serializers.CharField(
        max_length=32,
        required=True,
    )
    national_code = serializers.CharField(
        max_length=10,
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password_1 = serializers.CharField(
        style={'input_type': 'password'}
    )
    password_2 = serializers.CharField(
        style={'input_type': 'password'}
    )
    first_name = serializers.CharField(
        max_length=32
    )
    last_name = serializers.CharField(
        max_length=32
    )

    class Meta:
        unique_together = ('first_name', 'last_name')
        model = User
        fields = ['email', 'phone_number', 'password_1', 'password_2',
                  'national_code', 'first_name', 'last_name', 'person']

    def validate(self, attrs):
        if attrs.get('password_1') != attrs.get('password_2'):
            raise ValidationError(_("Passwords not match"))

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_2')
        validated_data['password'] = validated_data.pop('password_1')

        user = User.objects.create_user(
            username=validated_data.get('email'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            is_active=False
        )
        person = Person.objects.create(
            user=user,
            phone_number=validated_data.get('phone_number'),
            last_name=validated_data.get('last_name'),
            first_name=validated_data.get('first_name'),
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ResetPasswordConfirmSerializer(serializers.ModelSerializer):
    new_password1 = serializers.CharField(max_length=100)
    new_password2 = serializers.CharField(max_length=100)

    class Meta:
        model = ResetPasswordToken
        fields = ['new_password1', 'new_password2', 'uid', 'token']

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError('passwords don\'t match!')
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'})
    new_password1 = serializers.CharField(style={'input_type': 'password'})
    new_password2 = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(_('passwords don\'t match!'))
        if not self.context['request'].user.check_password(
                data['old_password']):
            raise serializers.ValidationError(_('invalid old password'))
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(
            raw_password=self.validated_data['new_password1']
        )
        user.save()

        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
