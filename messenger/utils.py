import json

import redis

from django.utils import dateformat
from django.shortcuts import HttpResponse

from messenger.models import Message , MessageIm


def json_response(obj):
    return HttpResponse(json.dumps(obj), content_type="application/json")


def send_message(thread_id,
                 sender_id,
                 message_text,
                 sender_name=None):
    message = Message()
    message.text = message_text
    message.thread_id = thread_id
    message.sender_id = sender_id
    message.save()


def send_message_ls(thread_id,
                 sender_id,
                 message_text,
                 sender_name=None):
    message = MessageIm()
    message.text = message_text
    message.thread_id = thread_id
    message.sender_id = sender_id
    message.save()

