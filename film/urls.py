from django.urls import path
from . import views
urlpatterns = [
    path('', views.main_film), # 메인 페이지 film data / GET(main 페이지 정보), POST(main 페이지에서 + 버튼 눌렀을 때)
    path('choice', views.choose_film), # film 선택 팝업창 / GET
    path('<int:pk>', views.film_detail), # film 하나의 디테일 data / GET
    path('new', views.make_film), # film 만들기 / POST
    path('all', views.all_film), # film 보관함 전체 조회 / GET
    path('all/type', views.all_film_classify), # film 보관함 전체 종류별 조회 / GET
    path('inhwa', views.film_inhwa), # film 인화하고 기본 앨범으로 종속시킴 / POST
]