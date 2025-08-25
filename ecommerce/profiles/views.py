from django.shortcuts import get_object_or_404, render, redirect
from authentication.models import CustomUser
from django.contrib import messages
from .models import Profile, Address
from main.utils import redirect_dashboard
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def address_page_view(request):

    user = CustomUser.objects.filter(id=request.user.id).first()
    try:

        addresses = Address.objects.filter(user=user)

        context = {"user": user, "addresses": addresses}

        return render(request, "common/address.html", context=context)

    except Exception as e:
        print("An exception occurred in address_page_view", e)
        messages.error(request, "Error in address_page_view")
        return redirect_dashboard(user)


@login_required(login_url="login")
def add_address_view(request):
    user = CustomUser.objects.filter(id=request.user.id).first()
    try:
        if user is None:
            messages.error(request, "User not found")
            return redirect_dashboard(user)

        data = request.POST

        street = data.get("street").strip()
        city = data.get("city").strip()
        state = data.get("state").strip()
        zip_code = data.get("zip_code").strip()
        country = data.get("country").strip()
        default = int(data.get("default").strip())

        if not street or not city or not state or not zip_code or not country:
            messages.warning(request, "All fields are required")
            return redirect("address-page")

        address = Address.objects.create(
            user=user,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            is_default=True if default == 1 else False,
        )

        if default == 1:
            default_addresses = Address.objects.filter(
                id != address.pk, is_default=True
            )
            for address in default_addresses:
                address.is_default = False
                address.save()

        messages.success(request, "Address added successfully")
        return redirect("address-page")

    except Exception as e:
        print("An exception occurred in add_address_view", e)
        messages.error(request, "Error in add_address_view")
        return redirect("address-page")


@login_required(login_url="login")
def edit_address_view(request, address_id):
    try:

        data = request.POST

        street = data.get("street").strip()
        city = data.get("city").strip()
        state = data.get("state").strip()
        zip_code = data.get("zip_code").strip()
        country = data.get("country").strip()
        default = int(data.get("default").strip())

        if default == 1:
            default_addresses = Address.objects.filter(
                id != address_id, is_default=True
            )
            for address in default_addresses:
                address.is_default = False
                address.save()

        if not street or not city or not state or not zip_code or not country:
            messages.warning(request, "All fields are required")
            return redirect("address-page")

        address = Address.objects.filter(id=address_id).first()

        if address is not None:
            address.street = street
            address.city = city
            address.state = state
            address.zip_code = zip_code
            address.country = country
            address.is_default = True if default == 1 else False
            address.save()
            messages.success(request, "Address updated successfully")
            return redirect("address-page")
        else:
            messages.error(request, "Address not exist")
            return redirect("address-page")

    except Exception as e:
        print("An exception occurred in add_address_view", e)
        messages.error(request, "Error in add_address_view")
        return redirect("address-page")


@login_required(login_url="login")
def delete_address_view(request, address_id):
    try:
        address = Address.objects.filter(id=address_id).first()

        if address:
            address.delete()

        return redirect("address-page")
    except Exception as e:
        print("An exception occurred in delete_address_view", e)
        messages.error(request, "Error in delete_address_view")
        return redirect("address-page")


@login_required(login_url="login")
def profile_page_view(request):
    user = CustomUser.objects.filter(id=request.user.id).first()

    try:

        if user is None:
            messages.error(request, "user not exist")
            return redirect("home")

        profile = Profile.objects.filter(user=user).first()

        if profile is None:
            profile = {
                "dob": "N/A",
                "bio": "N/A",
                "profile_picture": "N/A",
            }

        context = {"user": user, "profile": profile}
        return render(request, "common/profile.html", context=context)

    except Exception as e:
        print("An exception occurred in profile_page_view", e)
        messages.error(request, "Error in profile_page_view")
        return render(request, "common/profile.html", {"user": user})


@login_required(login_url="login")
def edit_profile_picture_view(request, id):

    user = CustomUser.objects.filter(id=id).first()
    try:
        profile = Profile.objects.filter(user=user).first()

        if not profile:
            profile = Profile.objects.create(user=user)
        profile_picture = None

        if request.method == "POST":
            profile_picture = request.FILES.get("profile_picture")

            if not profile_picture:
                messages.error(request, "Please upload a profile picture.")
            else:

                profile.profile_picture = profile_picture
                profile.save()
                messages.success(request, "Profile picture updated successfully.")

        return redirect("profile-page")

    except Exception as e:
        print("An exception occurred in edit_profile_picture_view:", e)
        messages.error(request, "Error in edit_profile_picture_view")
        return redirect("profile-page")


@login_required(login_url="login")
def edit_profile_view(request, id):
    try:
        user = CustomUser.objects.filter(id=request.user.id).first()
        if user is None:
            messages.error(request, "user not exist")
            return redirect("profile-page")

        data = request.POST

        first_name = data["first_name"]
        last_name = data["last_name"]
        #    email = data['email']
        phone_no = data["phone_no"]
        bio = data["bio"]
        dob = data["dob"]

        if not first_name or not last_name or not phone_no or not bio or not dob:
            messages.warning(request, "All fields required")
            return redirect("profile-page")

        profile = Profile.objects.filter(user=user).first()

        if profile is None:
            profile = Profile.objects.create(user=user, bio=bio, dob=dob)
        else:

            profile.bio = bio
            profile.dob = dob
            profile.save()

        user.first_name = first_name
        user.last_name = last_name
        user.phone_no = phone_no
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("profile-page")

    except Exception as e:
        print("An exception occurred in edit_profile_view", e)
        messages.error(request, "Error in edit_profile_view")
        return redirect("profile-page")
