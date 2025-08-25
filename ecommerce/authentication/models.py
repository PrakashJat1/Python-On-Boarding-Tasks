from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from .utils import assign_permission


class CustomUserManager(BaseUserManager):

    def create_user(
        self,
        first_name,
        last_name,
        email,
        phone_no,
        role,
        password=None,
    ):
        if not email:
            raise ValueError("Email is missing")

        is_active = True if role == 1 or role == 3 or role == 4 else False

        user = self.model(
            email=self.normalize_email(email),  # make email in lowercase
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
            role=role,
            is_active=is_active,  # By default the user is active
        )

        user.set_password(password)  # save password in hased format

        assign_permission(user, role)  # assign permissions to users not admin
        user.save(using=self._db)  # for manage multiple database

        return user

    def create_superuser(self, first_name, last_name, email, phone_no, password=None):

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            phone_no=phone_no,
            password=password,
            role=CustomUser.ADMIN,
        )

        # make user admin
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)


class CustomUser(
    AbstractBaseUser, PermissionsMixin
):  # with AbstractBaseUser we have full control on our User model (No extra filed unlike AbstractUser)

    # roles
    ADMIN = 1
    DELIVERY_MANAGER = 2
    SELLER = 3
    CUSTOMER = 4

    ROLE_CHOICE = (
        (ADMIN, "admin"),
        (DELIVERY_MANAGER, "delivery_manager"),
        (SELLER, "seller"),
        (CUSTOMER, "customer"),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    password = models.CharField(max_length=200)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICE, blank=False, null=True, default=CUSTOMER
    )
    otp = models.CharField()
    is_verified = models.BooleanField(default=False)

    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone_no",
    ]  # It should not include the USERNAME_FIELD

    objects = CustomUserManager = (
        CustomUserManager()
    )  # tells django to use CustomUserManager as UserManager

    # data level permissions
    def has_perm(
        self, perm, obj=None
    ):  # check if user_obj has the permission string perm. Returns False if the user is not is_active.
        if self.is_admin:
            return True
        return super().has_perm(perm, obj)  # for seller and customer & delivery_manager

    # module level permissions
    def has_module_perms(
        self, app_label
    ):  # Returns whether the user_obj has any permissions on the app app_label(Module)
        if self.is_admin:
            return True
        return super().has_module_perms(app_label)

    def __str__(self):
        return str(self.email)


class EmailConstants:
    REGISTRATION_OTP = "REGISTRATION_OTP"
    REGISTRATION_CONFIRMATION = "REGISTRATION_CONFIRMATION"
    RESET_PASSWORD = "RESET_PASSWORD"
    RESET_PASSWORD_OTP = "RESET_PASSWORD_OTP"
    PROFILE_UPDATE = "PROFILE_UPDATE"


class EmailTemplate(models.Model):

    EMAIL_CHOICE = (
        (EmailConstants.REGISTRATION_OTP, "REGISTRATION_OTP"),
        (EmailConstants.REGISTRATION_CONFIRMATION, "REGISTRATION_CONFIRMATION"),
        (EmailConstants.RESET_PASSWORD, "RESET_PASSWORD"),
        (EmailConstants.RESET_PASSWORD_OTP, "RESET_PASSWORD_OTP"),
        (EmailConstants.PROFILE_UPDATE, "PROFILE_UPDATE"),
    )

    identifier = models.CharField(max_length=50, choices=EMAIL_CHOICE)
    subject = models.CharField(max_length=100, blank=False, default="Email Subject")
    template = models.TextField()
