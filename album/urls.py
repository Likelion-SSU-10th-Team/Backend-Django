from django.urls import path
from . import views

urlpatterns = [
    path('album/', views.album_list),
]