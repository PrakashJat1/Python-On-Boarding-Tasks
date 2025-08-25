from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def generate_unique_slug(model_class, title):
    slug = slugify(title)
    unique_slug = slug
    num = 1
    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug


@login_required(login_url="login")
def redirect_dashboard(user):
    return (
        redirect("seller_dashboard") if user.role == 3 else redirect("customer_dashboard") if user.role == 4 else redirect("deliverymanager_dashboard")
    )
