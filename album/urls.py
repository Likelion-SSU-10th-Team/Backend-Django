from django.urls import path
from . import views
import diary.views as d_views

urlpatterns = [
    path('', views.album_list), # 앨범 페이지 정보 / GET ✔
    path('new/', views.make_album), # 앨범 만들기 / POST ✔
    path('<int:album_id>', views.album_detail), # album 하나의 디테일 data / GET ✔
    path('edit/<int:diary_id>', views.read_page), # Read 페이지 데이터 다 쏴줌 / GET ✔
    # path('<int:album_id>/<int:diary_id>/', views.diary_detail), # diary 정보 data / GET
    # path('composition/<int:diary_id>', views.send_album_id), # 일기가 속한 앨범 / GET
    path('select', views.select_album), # 앨범 선택 / POST
]