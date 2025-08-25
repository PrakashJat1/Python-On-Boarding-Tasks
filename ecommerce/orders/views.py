from profiles.models import Address
from django.shortcuts import redirect, render, get_object_or_404
from .models import Order
from products.models import Product
from authentication.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_SECRET))


@login_required(login_url="login")
def order_page_view(request):
    user = request.user
    orders = Order.objects.filter(customer=user)
    try:

        # products = [order.product for order in orders]

        context = {"user": user, "orders": orders}
        return render(request, "pages/customer/orders.html", context=context)

    except Exception as e:
        print("An exception occurred in order_page_view", e)
        messages.error(request, "Error in order_page_view")
        return render(
            request, "pages/customer/orders.html", {"user": user, "orders": orders}
        )


@csrf_exempt
@login_required(login_url="login")
def order_product_view(request, user_id, product_id):

    try:
        data = request.POST

        customer = CustomUser.objects.filter(id=user_id).first()
        product = get_object_or_404(Product, id=product_id)
        quantity = int(data.get("quantity").strip())
        address = data.get("address")

        if not quantity or not address:
            messages.warning(request, "All fields are required")
            return redirect("customer_dashboard")

        price = quantity * product.price

        order_data = {
            "amount": int(price * 100),
            "currency": "INR",
            "payment_capture": "1",
        }
        razorpay_order = client.order.create(order_data)
        Order.objects.create(
            customer=customer,
            product=product,
            quantity=3,
            price=price,
            status="on the way",
            address=address,
            razorpay_order_id=razorpay_order["id"],
        )
        product.quantity -= 1
        product.save()
        return JsonResponse(
            {
                "order_id": razorpay_order["id"],
                "razorpay_key_id": settings.RAZORPAY_API_KEY,
                "product_name": product.name,
                "amount": order_data["amount"],
                "razorpay_callback_url": settings.RAZORPAY_CALLBACK_URL,
                "user": {
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                    "email": request.user.email,
                    "phone_no": getattr(request.user, "phone_no", ""),
                },
            }
        )
    except Exception as e:
        print("An exception occurred in order_product_view", e)
        messages.error(request, "Error in order_product_view")
        return redirect("customer_dashboard")


# @csrf_exempt
# @login_required(login_url="login")
# def order_product_view(request, user_id, product_id):

#     try:
#         data = request.POST

#         customer = CustomUser.objects.filter(id=user_id).first()
#         product = get_object_or_404(Product, id=product_id)
#         order_data = {
#             "amount": int(product.price * 100),  # rupee to paise
#             "currency": "INR",
#             "payment_capture": "1",
#         }
#         razorpay_order = client.order.create(order_data)
#         Order.objects.create(
#             customer=customer,
#             product=product,
#             quantity=3,
#             price=product.price,
#             status="on the way",
#             address="",
#             razorpay_order_id=razorpay_order["id"],
#         )
#         product.quantity -= 1
#         product.save()
#         return JsonResponse(
#             {
#                 "order_id": razorpay_order["id"],
#                 "razorpay_key_id": settings.RAZORPAY_API_KEY,
#                 "product_name": product.name,
#                 "amount": order_data["amount"],
#                 "razorpay_callback_url": settings.RAZORPAY_CALLBACK_URL,
#                 "user": {
#                     "first_name": request.user.first_name,
#                     "last_name": request.user.last_name,
#                     "email": request.user.email,
#                     "phone_no": getattr(request.user, "phone_no", ""),
#                 },
#             }
#         )
#     except Exception as e:
#         print("An exception occurred in order_product_view", e)
#         messages.error(request, "Error in order_product_view")
#         return redirect("customer_dashboard")


@login_required(login_url="login")
def update_order_view(request, order_id):
    data = request.POST
    status = data.get("status")

    order = Order.objects.filter(id=order_id).first()
    if order is not None:
        order.status = status
        order.save()
        messages.success(request, "Order updated successfully")
        return redirect("deliverymanager_dashboard")
    else:
        messages.error(request, "Order is not present")
        return redirect("deliverymanager_dashboard")


@login_required(login_url="login")
def checkout_view(request, product_id):
    try:
        product = Product.objects.filter(id=product_id).first()
        addresses = Address.objects.filter(user=request.user)

        if not product:
            messages.error(request, "Product not found")
            return redirect("cart-page")

        return render(
            request,
            "pages/customer/checkout.html",
            {"user": request.user, "product": product, "addresses": addresses},
        )
    except:
        print("An exception occurred in checkout_view")
        messages.error(request, "Error in checkout_view")
        return redirect("cart-page")


@csrf_exempt
# @login_required(login_url="login")
def payment_verify_view(request):
    try:
        if "razorpay_signature" in request.POST:
            order_id = request.POST.get("razorpay_order_id")
            payment_id = request.POST.get("razorpay_payment_id")
            signature = request.POST.get("razorpay_signature")

            order = get_object_or_404(Order, razorpay_order_id=order_id)

            if client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": order_id,
                    "razorpay_payment_id": payment_id,
                    "razorpay_signature": signature,
                }
            ):

                order.razorpay_payment_id = payment_id
                order.razorpay_signature = signature
                order.payment_status = True
                order.save()
                messages.success(request, "Payment successful")
                return redirect("customer_dashboard")
            else:
                messages.error(request, "Payment failed invalid signature")
                return redirect("customer_dashboard")
        else:
            messages.error(request, "Payment failed signature missing")
            return redirect("customer_dashboard")

    except Exception as e:
        print("An exception occurred in payment_verify_view", e)
        messages.error(request, "Error in payment_verify_view")
        return redirect("customer_dashboard")
