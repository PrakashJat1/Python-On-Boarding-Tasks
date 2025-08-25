from django.urls import path
from . import views

urlpatterns = [
    path("order-page",views.order_page_view,name="order-page"),
    path(
        "order-product/<int:user_id>/<int:product_id>/",
        views.order_product_view,
        name="order-product",
    ),
    path('payment-verify/',views.payment_verify_view,name="payment-verify"),
    path("update-order/<int:order_id>", views.update_order_view, name="update-order"),
    path("checkout/<int:product_id>/",views.checkout_view,name="checkout")
]
