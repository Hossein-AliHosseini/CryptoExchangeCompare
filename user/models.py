from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import sys
import requests

from model_utils.models import TimeStampedModel

from .token import account_activation_token


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def send_activation_link(self, is_sms):
        activate_user_token = ActivateUserToken(
            token=account_activation_token.make_token(self),
            eid=urlsafe_base64_encode(force_bytes(self.email)),
        )
        activate_user_token.save()

        context = {
            'domain': settings.DOMAIN,
            'eid': activate_user_token.eid,
            'token': activate_user_token.token,
            'first_name': self.person.first_name
        }
        # from user.tasks import send_email

        # send_email.delay(self.id, context,
        #                  'user/registerifinal.htm',
        #                  'Account Activation Email')

        activation_message_html = render_to_string('user/user_activate_email.html',
                                                   context=context)
        activation_message_plaintext = strip_tags(activation_message_html)
        sys.stdout.write(activation_message_plaintext)

        if not is_sms:
            email = EmailMultiAlternatives(
                subject='Account Activation Email',
                body=activation_message_plaintext,
                from_email=settings.EMAIL_HOST_USER,
                to=[self.email]
                )

            email.attach_alternative(activation_message_html, 'text/html')
            sys.stdout.write('Sending Email...')
            try:
                email.send()
                sys.stdout.write('Email sent successfully.')
            except Exception:
                sys.stdout.write('An error occurred!')
        else:
            response = requests.get('http://0.0.0.0:5000/send-activation-sms?phone-number=' +
                                    self.person.phone_number +
                                    '&eid=' + activate_user_token.eid +
                                    '&token=' + activate_user_token.token)
            print(response)

    # @classmethod
    # def activate(cls, eid, token):
    #     activate_user_token = get_object_or_404(ActivateUserToken,
    #                                             eid=eid, token=token)

    #     email = urlsafe_base64_decode(eid).decode('utf-8')
    #     user = cls.objects.get(email=email)
    #     user.is_active = True
    #     activate_user_token.delete()
    #     user.save()


class Person(TimeStampedModel):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE,
                                related_name='person')
    national_code = models.CharField(max_length=10, null=True)  # validator
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    birthdate = models.DateField(null=True)
    address = models.CharField(max_length=256)  # validator
    phone_number = models.CharField(max_length=32, null=True)
    profile_image = models.ImageField(upload_to='profile_images',
                                      null=True, default='profile_images/default.png')

    @property
    def is_complete(self):
        return all(
            (
                self.national_code, self.first_name, self.last_name,
                self.birthdate, self.address, self.phone_number,
                self.profile_image
            )
        )


class ActivateUserToken(models.Model):
    token = models.CharField(max_length=100)
    eid = models.CharField(max_length=100, null=True)


class ResetPasswordToken(models.Model):
    uid = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    expiration_date = models.DateTimeField()