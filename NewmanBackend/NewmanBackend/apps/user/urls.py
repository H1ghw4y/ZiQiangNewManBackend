from django.urls import path
from . import views

urlpatterns = [
    path('', views.get),
    path('change_tx', views.change_tx),
    path('change_name', views.change_name),
    path('renzheng', views.Renzheng.as_view()),
    ]
