from django.urls import path, include
from . import views

urlpatterns = [
    path("user-home/<int:user_id>",views.user_home_view,name="user-home"),
    path("register/", views.register_view, name="register"),
    path("verifyotp/<int:user_id>", views.verify_otp_view, name="verifyotp"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("reset-password/", views.reset_password_view, name="reset-password"),
    path(
        "verify-reset-password-otp/<int:user_id>",
        views.verify_reset_password_otp,
        name="verify-reset-password-otp",
    ),
    path(
        "update-password/<int:user_id>",
        views.update_password_view,
        name="update-password",
    ),
    path(
        "dashboard/delivery_manager/",
        views.delivery_manager_dashboard_view,
        name="deliverymanager_dashboard",
    ),
    path(
        "dashboard/seller/",
        views.seller_dashboard_view,
        name="seller_dashboard",
    ),
    path(
        "dashboard/customer/",
        views.customer_dashboard_view,
        name="customer_dashboard",
    ),
]
