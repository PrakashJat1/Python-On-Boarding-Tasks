from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import FeedbackSerializer
from .utlis import send_form_submission_mail
from django.shortcuts import redirect

# Create your views here.


def submit(request):
    data = request.POST

    serializer = FeedbackSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

    send_form_submission_mail(
        "Successfully Feedback Form Submission",
        "Your feedback is recorded successfully thank you",
        data.get("email"),
    )

    return redirect("home")
