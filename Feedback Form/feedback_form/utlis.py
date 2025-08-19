from django.conf import settings
from django.core.mail import send_mail


def send_form_submission_mail(subject, message, reciver_mail):
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [reciver_mail]

    send_mail(subject, message, from_email, recipient_list)
