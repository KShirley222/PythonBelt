from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('main', views.login),
    path('register', views.register),
    path('travels', views.alltravel),
    path('travels/add', views.addtravel),
    path('login', views.loginUser),
    path('logout', views.logoutUser),
    path('createtrip', views.submitTravel),
    path('travels/destination/<tripID>', views.tripInfo),
    path('join/<joinID>', views.joinTrip),
]