from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.generic import View
from .models import Thread, ThreadIm
from .models import Message
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from account.models import Account
from messenger.utils import json_response, send_message, send_message_ls
from django.conf import settings


@method_decorator(csrf_exempt)
def send_message_api_view(request, thread_id):
    if not request.method == "POST":
        return json_response({"error": "Please use POST."})

    api_key = request.POST.get("api_key")

    if api_key != settings.API_KEY:
        return json_response({"error": "Please pass a correct API key."})

    try:
        thread = Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:

        return json_response({"error": "No such thread."})

    try:
        sender = Account.objects.get(id=request.POST.get("sender_id"))
    except Account.DoesNotExist:
        return json_response({"error": "No such user."})


    message_text = request.POST.get("message")

    if not message_text:
        return json_response({"error": "No message found."})

    if len(message_text) > 10000:
        return json_response({"error": "The message is too long."})

    print(send_message(
        thread.id,
        sender.id,
        message_text
    ))
    return json_response({"status": "ok"})



@method_decorator(csrf_exempt)
def send_message_api_view_ls(request, thread_id):
    if not request.method == "POST":
        return json_response({"error": "Please use POST."})

    api_key = request.POST.get("api_key")

    if api_key != settings.API_KEY:
        return json_response({"error": "Please pass a correct API key."})

    try:
        thread = ThreadIm.objects.get(id=thread_id)
    except Thread.DoesNotExist:

        return json_response({"error": "No such thread."})

    try:
        sender = Account.objects.get(id=request.POST.get("sender_id"))
    except Account.DoesNotExist:
        return json_response({"error": "No such user."})


    message_text = request.POST.get("message")

    if not message_text:
        return json_response({"error": "No message found."})

    if len(message_text) > 10000:
        return json_response({"error": "The message is too long."})

    print(send_message_ls(
        thread_id,
        sender.id,
        message_text
    ))
    return json_response({"status": "ok"})