from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.Register.as_view(), name='register'),
    path('register2/', views.Register2.as_view(), name='register2'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Login.logout, name='logout'),
    path('', views.Base.as_view()),

]
