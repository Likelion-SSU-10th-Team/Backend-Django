from django.urls import path
from . import views
urlpatterns = [
    path('', views.main_film), # 메인 페이지 film data / GET(main 페이지 정보), POST(main 페이지에서 + 버튼 눌렀을 때)
    path('<int:pk>', views.film_detail), # film 하나의 디테일 data / GET
    path('new/', views.make_film), # film 만들기 / POST
    path('all', views.all_film), # film 보관함 전체 조회 / GET

]