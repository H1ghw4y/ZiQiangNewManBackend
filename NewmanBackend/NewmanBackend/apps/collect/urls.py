from django.urls import path
from . import views, views1

urlpatterns = [
    #path('search/', views.search),
    path('', views.get)
]
