from django.urls import path
from . import views

urlpatterns = [
    path('', views.album_list), # 메인 페이지 album data / GET(앨범 페이지 정보), POST(+ 버튼 눌렀을 때)
    path('new/', views.make_album), # 앨범 만들기 / POST
    path('<int:album_id>', views.album_detail), # album 하나의 디테일 data / GET
    path('<int:album_id>/<int:diary_id>', views.diary_detail), # diary 하나의 디테일 data / GET
]