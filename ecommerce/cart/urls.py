from django.urls import path
from . import views

urlpatterns = [
    path("add-product-to-wishlist/<slug:product_slug>",views.add_product_to_wishlist_view,name="add-product-to-wishlist"),
    path("remove-product-from-wishlist/<int:user_id>/<slug:product_slug>",views.remove_product_from_wishlist_view,name="remove-product-from-wishlist"),
    path("wishlist-page/", views.wishlist_page_view, name="wishlist-page"),
    path("cart-page/<int:user_id>", views.cart_page_view, name="cart-page"),
    path(
        "add-item-to-cart/<int:user_id>/<int:product_id>",
        views.add_item_to_cart_view,
        name="add-item-to-cart",
    ),
    path(
        "remove-item-from-cart/<int:user_id>/<int:item_id>",
        views.remove_item_from_cart_view,
        name="remove-item-from-cart",
    ),
]
