from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('write', views.diary_write),
    path('comment/<int:diary_id>', views.comment),
]