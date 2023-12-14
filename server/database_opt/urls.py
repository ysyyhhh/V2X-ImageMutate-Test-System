from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("register_db", views.register_db),
    path("remove_db", views.remove_db),
    path("get_db", views.get_db),
]
