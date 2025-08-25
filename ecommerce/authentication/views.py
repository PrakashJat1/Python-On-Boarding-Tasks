from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from profiles.models import Address
from products.models import Product, Category
from .models import CustomUser
from django.contrib import messages

from .utils import (
    generate_otp,
    mailer,
    otp_mail_message,
    registration_successfull_message,
)
from orders.models import Order
from django.core.paginator import Paginator


@login_required
def user_home_view(request, user_id):

    try:
        user = CustomUser.objects.filter(pk=user_id).first()
        if user is None:
            messages.error(request, "User not found")
            return redirect("home")
        else:
            match user.role:
                case 1:
                    return redirect("/admin/")
                case 2:
                    return redirect("deliverymanager_dashboard")
                case 3:
                    return redirect("seller_dashboard")
                case 4:
                    return redirect("customer_dashboard")
                case _:
                    messages.error(request, "invalid user role")
                    return redirect("home")

    except Exception as e:
        print("An exception occurred user_home_view ", e)
        messages.error(request, "invalid user role")
        return redirect("home")


def register_view(request):
    if request.method == "GET":
        return render(request, "auth/Register.html")

    data = request.POST

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    phone_no = data.get("phone_no")
    password = data.get("password")
    confrim_password = data.get("confirmpassword")
    role = data.get("role")

    match role:
        case "customer":
            role = CustomUser.CUSTOMER
        case "seller":
            role = CustomUser.SELLER
        case "delivery_manager":
            role = CustomUser.DELIVERY_MANAGER
        case _:
            messages.warning(request, "Invalid Role")
            return redirect("register")

    if password != confrim_password:
        messages.warning(request, "Password and Confirm Password must be same")
        return redirect("register")

    is_unverfied_user = CustomUser.objects.filter(email=email).first()

    if is_unverfied_user is not None and is_unverfied_user.is_verified == False:
        otp = generate_otp()

        mailer(
            subject="Registration OTP",
            message="OTP VERIFICATION",
            html_content=otp_mail_message(
                is_unverfied_user.first_name,
                otp,
                "Cubexo Software Solutions",
                "https://cubexo.io/Contactus",
            ),
            to=[email],
        )
        is_unverfied_user.otp = otp
        is_unverfied_user.save()
        context = {"email": email, "user_id": is_unverfied_user.pk}
        print("Unverified User")
        return render(request, "auth/OTPPage.html", context=context)

    if is_unverfied_user is not None and is_unverfied_user.is_verified == True:
        messages.warning(request, f"Email has been already taken")
        return redirect("register")
    else:
        otp = generate_otp()

        mailer(
            subject="Registration OTP",
            message="OTP VERIFICATION",
            html_content=otp_mail_message(
                first_name,
                otp,
                "Cubexo Software Solutions",
                "https://cubexo.io/Contactus",
            ),
            to=[email],
        )
        print("new user")
        user = CustomUser.objects.create_user(
            first_name, last_name, email, phone_no, role, password
        )
        user.otp = otp
        user.is_verified = False
        user.save()

    context = {"email": email, "user_id": user.pk}

    return render(request, "auth/OTPPage.html", context=context)


def verify_otp_view(request, user_id):
    if request.method == "GET":
        return render(request, "OTPPage.html")

    user = CustomUser.objects.get(pk=user_id)
    otp = request.POST.get("otp")
    if user.otp == otp:

        mailer(
            subject="Registration Successfully ",
            message=f"Welcome {user.first_name}",
            html_content=registration_successfull_message(),
            to=[user.email],
        )
        user.is_verified = True
        user.save()
        return redirect("login")

    messages.warning(request, "Enter Correct OTP")
    context = {"email": user.email, "user_id": user.pk}
    return render(request, "OTPPage.html", context=context)


def login_view(request):
    if request.user.is_authenticated:
        redirect("home")

    if request.method == "GET":
        return render(request, "auth/Login.html")

    data = request.POST

    email = data.get("email")
    password = data.get("password")

    existing_user = CustomUser.objects.filter(email=email).first()

    if existing_user is None:
        messages.warning(request, f"User not exist using this {email}")
        return redirect("login")
    elif existing_user.is_verified == False and not existing_user.role == 1:
        otp = generate_otp()
        mailer(
            subject="Registration OTP",
            message="OTP VERIFICATION",
            html_content=otp_mail_message(
                existing_user.first_name,
                otp,
                "Cubexo Software Solutions",
                "https://cubexo.io/Contactus",
            ),
            to=[email],
        )
        existing_user.otp = otp
        existing_user.save()
        context = {"email": email, "user_id": existing_user.pk}
        return render(request, "auth/OTPPage.html", context=context)

    # for delivery manager admin approval is required
    if existing_user.is_active == False:
        messages.warning(request, "Wait for admin approval")
        return redirect("login")

    authenticated_user = authenticate(request, username=email, password=password)

    if authenticated_user is None:
        messages.error(request, "Invalid Credentials")
        return redirect("login")

    login(request, authenticated_user)

    context = {"user": existing_user}

    redire = "home"

    match existing_user.role:
        case 1:
            return redirect("/admin/")
        case 2:
            dashboard = "deliverymanager_dashboard"
        case 3:
            dashboard = "seller_dashboard"
        case 4:
            dashboard = "customer_dashboard"
        case _:
            dashboard = "home"

    return redirect(dashboard)


def logout_view(request):
    logout(request)
    return redirect("home")


def reset_password_view(request):

    if request.method == "GET":
        return render(request, "auth/ResetPassword.html")

    data = request.POST
    email = data.get("email")

    existing_user = CustomUser.objects.filter(email=email).first()

    if existing_user is not None:
        if existing_user.is_verified == False:
            messages.warning(
                request, f"Please complete the registration process first {email}"
            )
            return redirect("register")

        otp = generate_otp()

        mailer(
            subject="Reset Password OTP",
            message="OTP VERIFICATION",
            html_content=otp_mail_message(
                existing_user.first_name,
                otp,
                "Cubexo Software Solutions",
                "https://cubexo.io/Contactus",
            ),
            to=[email],
        )
        existing_user.otp = otp
        existing_user.save()
        context = {"email": email, "user_id": existing_user.pk}
        return render(request, "auth/ResetPasswordOTPPage.html", context=context)
    else:
        messages.warning(request, f"User not exist with email {email}")
        return redirect("reset-password")


def verify_reset_password_otp(request, user_id):
    if request.method == "GET":
        return render(request, "auth/ResetPasswordOTPPage.html")

    user = CustomUser.objects.filter(id=user_id).first()
    if user is not None:
        otp = request.POST.get("otp")
        if user.otp == otp:
            context = {"user_id": user.pk}
            return render(request, "auth/NewPasswordPage.html", context=context)

        else:
            messages.warning(request, "Enter Correct OTP")
            context = {"email": user.email, "user_id": user.pk}
            return render(request, "auth/ResetPasswordOTPPage.html", context=context)
    else:
        return render(request, "auth/OTPPage.html")


def update_password_view(request, user_id):

    user = CustomUser.objects.filter(id=user_id).first()
    context = {"user_id": user_id}

    if request.method == "GET":
        return render(request, "auth/NewPasswordPage.html", context=context)
    else:
        data = request.POST
        password = data.get("password")
        confrim_password = data.get("confirmpassword")

        if password != confrim_password:
            messages.warning(request, "Password and Confirm Password must be same")
            return render(request, "auth/NewPasswordPage.html", context=context)

        if user is not None:
            user.set_password(password)
            user.save()
            messages.success(request, "Password Reset successfully")
            return redirect("login")
        else:
            messages.warning(request, "User not exist")
            return render(request, "auth/NewPasswordPage.html", context=context)


@login_required(login_url="login")
def delivery_manager_dashboard_view(request):
    id = request.user.id
    user = CustomUser.objects.filter(pk=id).first()
    orders = Order.objects.all()
    categories = Category.objects.all()
    context = {"user": user, "orders": orders, "categories": categories}
    return render(request, "dashboards/delivery_manager.html", context=context)


@login_required(login_url="login")
def seller_dashboard_view(request):
    id = request.user.id
    user = CustomUser.objects.filter(pk=id).first()
    products = Product.objects.filter(seller=id)
    categories = Category.objects.all()
    paginator = Paginator(products, 3)
    page = request.GET.get("page")
    products = paginator.get_page(page)
    context = {"user": user, "products": products, "categories": categories}
    return render(request, "dashboards/seller.html", context=context)


@login_required(login_url="login")
def customer_dashboard_view(request):
    # query = request.GET['search']
    id = request.user.id
    user = CustomUser.objects.filter(pk=id).first()
    products = Product.objects.all()
    addresses = Address.objects.filter(user=user)
    paginator = Paginator(products, 3)
    page = request.GET.get("page")
    products = paginator.get_page(page)

    categories = Category.objects.all()
    context = {"user": user, "products": products, "categories": categories,"addresses":addresses}
    return render(request, "dashboards/customer.html", context=context)
