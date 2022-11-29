from django.urls import path
from . import views

urlpatterns = [
    path('', views.get),
    # path('collect/', views.PostReplyView.as_view()),
    path('change_tx', views.change_tx),
    path('change_name', views.change_name),
    path('renzheng', views.Renzheng.as_view()),
    ]
