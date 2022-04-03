import sys

from celery import shared_task

from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_email(user_pk, context, template_path, subject):
    user = User.objects.get(pk=user_pk)

    email_message_html = render_to_string(template_path,
                                          context=context)
    email_message_plaintext = strip_tags(email_message_html)

    email = EmailMultiAlternatives(
        subject=subject,
        body=email_message_plaintext,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
        )

    email.attach_alternative(email_message_html, 'txt/html')
    sys.stdout.write('Sending Email...')
    try:
        email.send()
        sys.stdout.write('Email sent successfully.')
    except Exception:
        sys.stdout.write('An error occurred!')
