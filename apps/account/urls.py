from django.urls import path

from .views import RegisterApi, LogoutApi

urlpatterns = [
    path('register/', RegisterApi.as_view()),
    path('logout/', LogoutApi.as_view()),
]