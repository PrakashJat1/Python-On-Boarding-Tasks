import random
from django.core.mail import EmailMultiAlternatives
from django_otp.oath import hotp
from typing import List
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .permission_config import PERMISSION_CONFIG
from celery import shared_task


def assign_permission(user, role):
    role_permission = PERMISSION_CONFIG.get(role, {})

    for model, permissions in role_permission.items():

        content_type = ContentType.objects.get_for_model(
            model
        )  # returns the ContentType instance representing that model

        for perm_codename in permissions:

            permission = Permission.objects.get(
                content_type=content_type,
                codename=f"{perm_codename}_{model._meta.model_name}",
            )

            user.user_permissions.add(permission)


def generate_otp():
    return hotp(key=b"12345678901234567890", counter=random.randint(1, 9), digits=6)

@shared_task
def mailer(subject, body, to: List[str]):
    email = EmailMultiAlternatives(
        subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to,
    )

    email.send()


def otp_mail_message(
    username,
    otp,
    app_name,
    app_contact_url,
):
    return f"""
        <html lang="en">

    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>OTP Email Template</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

      <link rel="stylesheet" href="/style.css">
      <style>
      </style>
    </head>

    <body>
      <div class="container-sec">
        <div class="text-center">
          <div><i class="fas fa-lock otp-lock"></i></div>
          <div class="welcome-section">
            <div class="app-name">
              {app_name}
            </div>
            <div class="welcome-text">
              Thanks for signing up !
            </div>

            <div class="verify-text">
              Please Verify Your Email Address
            </div>
            <div class="email-icon">
              <i class="fas fa-envelope-open"></i>
            </div>

          </div>
          <h2>Hello, {username}</h2>
          <p>Your One-Time Password (OTP) for verification is:</p>
          <div class="otp-code">{otp}</div>
          <p class="mt-4">Please use this OTP to complete your verification. </p>
        </div>
        <div class="footer-text">
          <p>If you did not request this OTP, please <a href={app_contact_url}>contact us</a> immediately.</p>
          <p>Thank you,<br>The {app_name} Team</p>
        </div>
      </div>

      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    </body>

    </html>
    """


def registration_successfull_message():
    return """
    <html>
        <body>
            <h1>Welcome!</h1>
            <p>Thank you for joining us. <strong>Enjoy our services!</strong></p>
        </body>
    </html>
    """
