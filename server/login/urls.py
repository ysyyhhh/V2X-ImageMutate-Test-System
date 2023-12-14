from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("djlogin", views.djlogin),
    path("djlogout", views.djlogout),
    path("djregister", views.djregister),
]
