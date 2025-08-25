from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from profiles.models import Address
from .models import Cart, CartItem, WishList
from authentication.models import CustomUser
from django.contrib import messages
from products.models import Product


@login_required(login_url="login")
def cart_page_view(request, user_id):
    try:
        user = CustomUser.objects.filter(id=user_id).first()
        addresses = Address.objects.filter(user=user)

        if user is None:
            messages.error(request, "User not exist")
            return redirect("customer_dashboard")
        else:
            cart = Cart.objects.filter(user=user).first()
            if cart is None:
                messages.error(request, "Cart not exist")
                context = {"user": user}
                return render(request, "pages/customer/cart.html", context=context)
            else:

                cart_items = CartItem.objects.filter(cart=cart)
                # products = [item.product for item in cart_items]
                context = {"user": user, "cart_items": cart_items,"addresses":addresses}
                return render(request, "pages/customer/cart.html", context=context)

    except Exception as e:
        print("An exception occurred in cart_page_view", e)
        messages.error(request, "An exception occurred in cart_page_view")
        return redirect("customer_dashboard")


@login_required(login_url="login")
def add_item_to_cart_view(request, user_id, product_id):

    try:

        data = request.POST
        quantity = data.get("quantity")

        if not quantity:
            messages.error(request, "Please Select Quantity")
            return redirect("customer_dashboard")

        existing_cart = Cart.objects.filter(user=user_id).first()
        product = Product.objects.filter(id=product_id).first()

        if product is None:
            messages.error(request, "Product not exist for adding in cart")
            return redirect("customer_dashboard")

        if existing_cart is None:
            user = CustomUser.objects.filter(id=user_id).first()

            if user is None:
                messages.error(request, "User not exist for cart creation")
                return redirect("customer_dashboard")

            new_cart = Cart.objects.create(user=user)

            CartItem.objects.create(cart=new_cart, product=product, qantity=quantity)
            messages.success(request, f"{product.name} added into cart")
            return redirect("customer_dashboard")

        else:
            CartItem.objects.create(
                cart=existing_cart, product=product, quantity=quantity
            )
            messages.success(request, f"{product.name} added to cart")
            return redirect("customer_dashboard")

    except Exception as e:
        print("An exception occurred in add_item_to_cart_view", e)
        messages.error(request, "An exception occurred in add_item_to_cart_view")
        return redirect("customer_dashboard")


@login_required(login_url="login")
def remove_item_from_cart_view(request, user_id, item_id):
    try:
        item = CartItem.objects.filter(id=item_id)
        if item is None:
            messages.error(request, "Item is not exist")
            return redirect("cart-page")

        item.delete()
        return redirect("cart-page", user_id)

    except Exception as e:
        print("An exception occurred in remove_item_from_cart_view", e)
        messages.error(request, "An exception occurred in remove_item_from_cart_view")
        return redirect("cart-page")


@login_required(login_url="login")
def wishlist_page_view(request):
    try:
        user = CustomUser.objects.filter(id=request.user.id).first()

        if user is None:
            messages.error(request, "User not exist")
            return redirect("customer_dashboard")
        else:
            wishlist = WishList.objects.filter(user=user).first()
            if wishlist is None:
                messages.error(request, "wishlist not exist")
                context = {"user": user, "products": []}
                print(context)
                return render(request, "pages/customer/wishlist.html", context=context)
            else:

                products = wishlist.products.all()
                context = {"user": user, "products": products}
                print(context)
                return render(request, "pages/customer/wishlist.html", context=context)

    except Exception as e:
        print("An exception occurred in wishlist_page_view", e)
        messages.error(request, "An exception occurred in wishlist_page_view")
        return redirect("customer_dashboard")


@login_required
def add_product_to_wishlist_view(request, product_slug):
    try:
        user = CustomUser.objects.filter(id=request.user.id).first()

        if user is None:
            messages.error(request, "User not exist")
            return redirect("customer_dashboard")

        existing_wishlist = WishList.objects.filter(user=user.pk).first()
        product = Product.objects.filter(slug=product_slug).first()

        if product is None:
            messages.error(request, "Product not exist for adding in WishList")
            return redirect("customer_dashboard")

        if existing_wishlist is None:
            wishlist = WishList.objects.create(user=user)
            wishlist.products.add(product)
            messages.success(request, f"{product.name} added into WishList")
            return redirect("customer_dashboard")

        else:
            for existing_product in existing_wishlist.products.all():
                if existing_product.slug == product.slug:
                    messages.success(
                        request, f"{product.name} Already added to WishList"
                    )
                    return redirect("customer_dashboard")

            existing_wishlist.products.add(product)
            messages.success(request, f"{product.name} added to WishList")
            return redirect("customer_dashboard")

    except Exception as e:
        print("An exception occurred in add_product_to_wishlist_view", e)
        messages.error(request, "An exception occurred in add_product_to_wishlist_view")
        return redirect("customer_dashboard")


@login_required
def remove_product_from_wishlist_view(request, user_id, product_slug):
    try:
        existing_wishlist = WishList.objects.filter(user=user_id).first()

        if existing_wishlist is None:
            messages.error(request, "Wishlist is not exist")
            return redirect("wishlist-page")

        product = existing_wishlist.products.filter(slug=product_slug).first()
        if product is not None:
            existing_wishlist.products.remove(product)
            return redirect("wishlist-page")

        return redirect("wishlist-page")

    except Exception as e:
        print("An exception occurred in remove_product_from_wishlist_view", e)
        messages.error(
            request, "An exception occurred in remove_product_from_wishlist_view"
        )
        return redirect("wishlist-page")
