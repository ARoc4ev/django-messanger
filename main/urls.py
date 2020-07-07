from django.urls import path, re_path
from . import views

urlpatterns = [
    path('ch/', views.ChannelNew.as_view()),
    path('tr/', views.ThreadNew.as_view()),
    re_path(r'^u/(?P<id_team>\w+)/(?P<id_channel>\w+)/(?P<id_traid>\w+)/$', views.Main.as_view()),
    re_path(r'^u/(?P<id_team>\w+)/(?P<id_channel>\w+)/$', views.Main.as_view()),
    re_path(r'^u/(?P<id_team>\w+)/$', views.Main.as_view()),
    re_path(r'^im/(?P<id_traid>\w+)/$', views.Im.as_view()),
    re_path(r'^im/$', views.Im.as_view()),
    re_path(r'^ims/$', views.Ims.as_view()),
    re_path(r'^tm/$', views.TeamList.as_view()),
    re_path(r'^team/$', views.TeamR.as_view()),
    re_path(r'^newteam/$', views.CreateTeam.as_view(), name='newteam'),
    re_path(r'^in/$', views.Invitations.as_view(), name='Invitations'),
    re_path(r'^int/$', views.Inteam.as_view(), name='inteam'),



]