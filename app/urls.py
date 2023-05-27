from django.urls import path
from . import views



urlpatterns = [
    path('prices/', views.prices, name='prices'),
    path('', views.index, name="index"),
    path('contact/', views.contact, name="contact"),
    path('analyse/', views.analyse, name="analyse"),
    path('register/', views.register, name="register"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name="logout")
]
