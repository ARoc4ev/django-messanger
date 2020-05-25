from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^send_message_api/(?P<thread_id>\d+)/$', views.send_message_api_view),
    re_path(r'^send_message_api_ls/(?P<thread_id>\d+)/$', views.send_message_api_view_ls),
]