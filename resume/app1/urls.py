from django.urls import path

from . import views

urlpatterns = [
    path("resume", views.NewResume, name="NewResumePage"),
    path('new', views.GetNewUser, name="NewUserPage"),
    path('',views.homepage, name="welcome page" )
]