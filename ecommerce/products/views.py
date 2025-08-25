from django.shortcuts import render, redirect
from authentication.models import CustomUser
from profiles.models import Address
from .models import Product, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from main.utils import redirect_dashboard


# @login_required(login_url='login')
# def products_by_category_view(request,category_slug):


@login_required(login_url="login")
def product_view(request, product_slug):
    try:
        product = Product.objects.filter(slug=product_slug).first()
        user = CustomUser.objects.filter(id=request.user.id).first()
        addresses = Address.objects.filter(user=user)
        if not user:
            messages.error(request, f"User not exist")
            return redirect_dashboard(request.user)

        if not product:
            messages.error(request, f"Product not exist using slug {product_slug}")
            return redirect_dashboard(request.user)
        else:

            context = {"user": user, "product": product, "addresses": addresses}
            return render(request, "pages/product_detail.html", context=context)
    except Exception as e:
        print("An Erro occured in product_view", e)
        messages.error(request, f"Error in product_view")
        return redirect_dashboard(request.user)


@login_required(login_url="login")
def products_by_category_view(request, category_slug):
    try:
        user = request.user
        category = Category.objects.filter(slug=category_slug).first()
        products = Product.objects.filter(category=category)
        categories = Category.objects.all()
        addresses = Address.objects.filter(user=user)
        paginator = Paginator(products, 3)
        page = request.GET.get("page")
        products = paginator.get_page(page)
        context = {
            "user": user,
            "products": products,
            "categories": categories,
            "addresses": addresses,
        }

        match request.user.role:
            case 2:
                return render(
                    request, "pages/delivery_manager/products.html", context=context
                )
            case 3:
                return render(request, "dashboards/seller.html", context=context)
            case 4:
                return render(request, "dashboards/customer.html", context=context)
            case _:
                messages.error(request, "Invalid role")
                return redirect_dashboard(request.user)
    except Exception as e:
        print("An exception occurred in products_by_category_view", e)
        messages.error(request, "Error in products_by_category_view")
        return redirect_dashboard(request.user)


@login_required(login_url="login")
def add_product_view(request, id):
    try:
        data = request.POST

        name = data.get("name")
        price = data.get("price")
        quantity = data.get("quantity")
        image = request.FILES.get("image")
        color = data.get("color")
        category = data.get("category")
        description = data.get("description")

        category = Category.objects.filter(name=category).first()

        user = CustomUser.objects.filter(pk=id).first()

        if user is not None:
            product = Product.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                seller=user,
                image=image,
                color=color,
                category=category,
                description=description,
            )
            messages.success(request, "Product addedd successfully")
            return redirect("seller_dashboard")
        else:
            messages.error(request, "User not found for add product")
            return redirect("seller_dashboard")
    except Exception as e:
        print("An exception occurred in add_product_view", e)
        messages.error(request, "Error in add_product_view")
        return redirect("seller_dashboard")


@login_required(login_url="login")
def get_all_products(request, id):

    user = CustomUser.objects.filter(pk=id).first()
    products = Product.objects.filter(seller=id)
    paginator = Paginator(products, 3)
    page = request.GET.get("page")
    products = paginator.get_page(page)

    return render(request, "dashboards/seller.html")


@login_required(login_url="login")
def delete_product_view(request, id):

    product = Product.objects.filter(id=id).first()

    if product is not None:
        product.delete()
        messages.success(request, "Product deleted successfully")
        return redirect("seller_dashboard")
    else:
        messages.error(request, "Product is not present")
        return redirect("seller_dashboard")


@login_required(login_url="login")
def add_category_view(request):
    try:
        name = request.POST.get("name")
        Category.objects.create(name=name)
        return redirect("seller_dashboard")

    except Exception as e:
        print("An exception occurred in add_category_view", e)
        messages.error(request, "Error in add_category_view")
        return redirect("seller_dashbaord")


@login_required(login_url="login")
def search_products_view(request):
    try:
        categories = Category.objects.all()
        user = request.user
        is_seller = user.role == 3
        query = request.GET.get("search", "").strip()

        if not query:
            messages.warning(request, "Empty query")
            return redirect_dashboard(user)

        if len(query) > 100:
            messages.warning(request, "Too long search query")
            return redirect_dashboard(user)

        if is_seller:
            products = Product.objects.filter(
                (Q(name__icontains=query) | Q(description__icontains=query))
                & Q(seller=user)
            )
            paginator = Paginator(products, 3)
            page = request.GET.get("page")
            products = paginator.get_page(page)
            return render(
                request,
                "dashboards/seller.html",
                {"user": user, "products": products},
            )
        else:
            addresses = Address.objects.filter(user=user)

            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            paginator = Paginator(products, 3)
            page = request.GET.get("page")
            products = paginator.get_page(page)
            return render(
                request,
                "dashboards/customer.html",
                {
                    "user": user,
                    "products": products,
                    "categories": categories,
                    "addresses": addresses,
                },
            )

    except Exception as e:
        print("An exception occurred in search_products_view", e)
        messages.error(request, "Error in search_products_view")
        return redirect_dashboard(request.user)


@login_required(login_url="login")
def filter_product_view(request, filter_order):
    try:
        user = request.user
        if user.role == 3:  # seller
            products = Product.objects.filter(seller=user)
        else:
            products = Product.objects.all()

        categories = Category.objects.all()

        match filter_order:
            case 1:
                products = products.order_by("price")
            case 2:
                products = products.order_by("-price")
            case 3:
                products = products.order_by("created_at")
            case 4:
                products = products.order_by("-created_at")
            case _:
                products = products

        paginator = Paginator(products, 3)
        page = request.GET.get("page")
        products = paginator.get_page(page)
        addresses = Address.objects.filter(user=user)

        context = {
            "user": user,
            "products": products,
            "categories": categories,
            "addresses": addresses,
        }

        match request.user.role:
            case 2:
                return render(
                    request, "pages/delivery_manager/products.html", context=context
                )
            case 3:
                return render(request, "dashboards/seller.html", context=context)
            case 4:
                return render(request, "dashboards/customer.html", context=context)
            case _:
                messages.error(request, "Invalid role")
                return redirect_dashboard(request.user)
    except Exception as e:
        print("An exception occurred in filter_product_view", e)
        messages.error(request, "Error in filter_product_view")
        return redirect_dashboard(request.user)
