import sys

from django.urls import path

from . import views

urlpatterns = [
    path('items/', views.get_page),
    path("like", views.add_like),
    path("publish", views.publish),
    path("detail", views.detail),
    path("test", views.api_test)
]
