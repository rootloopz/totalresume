from django.urls import path

from . import views

urlpatterns = [
    path("", views.NewResume, name="NewResumePage"),
    path('new', views.GetNewUser, name="NewUserPage"),
]