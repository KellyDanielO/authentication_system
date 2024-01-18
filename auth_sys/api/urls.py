from django.urls import path
from .views import BaseView, RegisterView, LoginView

urlpatterns = [
    path("", BaseView.as_view(), name="base-view"),
    path("register/", RegisterView.as_view(), name='register-view'),
    path('login/', LoginView.as_view(), name='login-view')
]