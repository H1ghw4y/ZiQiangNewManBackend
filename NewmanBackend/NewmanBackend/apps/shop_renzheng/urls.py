from django.urls import path
from . import views

urlpatterns = [
    path('todo/', views.Todo.as_view()),
    path('done/', views.Done.as_view()),
]
