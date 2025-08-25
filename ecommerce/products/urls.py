from django.urls import path
from . import views

urlpatterns = [
    path("product/<slug:product_slug>",views.product_view,name='product'),
    path(
        "products-by-category/<slug:category_slug>",
        views.products_by_category_view,
        name="products-by-category",
    ),
    path("filter-product/<int:filter_order>",views.filter_product_view,name='filter-product'),
    path("add-product/<int:id>", views.add_product_view, name="add-product"),
    path("delete-product/<int:id>", views.delete_product_view, name="delete-product"),
    path("search-products/", views.search_products_view, name="search-products"),
    path("add-category/", views.add_category_view, name="add-category"),
]
