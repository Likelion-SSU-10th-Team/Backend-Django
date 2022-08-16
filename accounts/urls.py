from django.urls import path
from . import views
urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('session', views.session),
    path('session2', views.test),
]