import json

from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import *
from accounts.models import User
from diary.models import *


# session_id로 user 인식
def find_user_by_sid(request):
    session_id = request.COOKIES.get('session_id')
    print("session_id : " + session_id)
    return get_object_or_404(User, session_id=session_id)


# Create your views here.
####### 필요한 API 목록(기본 전제 : 로그인이 되어있고 세션id로 필름 소유자 지정) ######
# 1. 로그인하고 들어갔을 때 지금 필름을 깐게 있으면 그 필름 데이터 쏴주고 아니면 빈화면 출력 GET
#   1-1. 선택된 필름이 없다면? -> NULL return ✔
#   1-2. 필름을 쓰고 있다면? -> 사용중인 영역까지만 image return GET ✔
#   1-3. 필름이 가득 찼다면?(메인 페이지 갈때마다 film이 가득 찼는지 정보가 감) ✔
#                               -> 필름 내용을 전체 조회(일기:사진,쓴 날짜) GET
def main_film(request):
    user = find_user_by_sid(request) # 로그인한 사람이 누군지?
    if request.method == 'GET':
        try:
            if model_to_dict(user).get('current_film') is not None:
                film = Film.objects.get(pk=model_to_dict(user).get('current_film'))  # 로그인한 사람이 쓰고있는 film이 무엇인지?
                if film.count == film.size:  # 리턴으로 Scoll 페이지 필요 정보 넘겨줌
                    film_id = user.current_film
                    user.current_film = None # user 정보 update(다 찼으니까 null로 바꿈)
                    user.save()
                    film.isFull = True # Film통 정보 update(가득참, endDate -> update)
                    film.endDate = timezone.localtime()
                    film.save()
                    # 추후 배포 IP로 바꿔야함
                    return HttpResponseRedirect('http://localhost:8000/film/' + str(film_id))
                response_body = {
                    'film_size': film.size,
                    'film_cnt': film.count,
                    'contents': [
                        {
                            'diary': diary.pk,  # 일기의 이미지만 가면 될듯?
                            'image': diary.image
                        } for diary in Diary.objects.filter(belong_to_film=film.pk)
                    ]
                }
                return JsonResponse(response_body, status=200)
            else:  # 선택된 필름이 없으면
                return JsonResponse({'curr_film': None}, status=200)
        except:
            return HttpResponse(status=400)
    # 3. 필름의 + 버튼을 누름 -> 일기 쓰는 페이지로 넘어가고 일기저장 버튼을 누름 -> 사이즈가 늘어나고 필름에 일기 등록됨 POST
    elif request.method == 'POST':
        film = Film.objects.get(pk=model_to_dict(user).get('current_film'))
        film.count += 1
        film.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


# 2. 필름 사이즈 고르면 그에 따라 새로운 필름 생성 POST
def make_film(request):
    user = find_user_by_sid(request)
    data = json.loads(request.body)
    if request.method == 'POST':
        # Film 객체 생성
        film = Film(
            size=data['size'],
            owner=user
        )
        film.save()
        # User의 current_film 정보 update
        user.current_film = film
        user.save()
        return HttpResponseRedirect('http://localhost:8000/film/') # Film 새로 만들면 새로 만든 film 정보 바로 쏴줌
    else:
        return HttpResponse(status=400)


# 4. 필름 보관함 페이지(년도 별로 정렬 -> 필름 완성 날짜 순 정렬) : 유저의 필름 전체 조회 GET
#   4-1. 1-3 재활용+필름 시작,끝 날짜
def all_film(request):
    user = find_user_by_sid(request)
    if request.method == 'GET':
        print(Film.objects.filter(owner=user.pk).order_by('endDate'))
        response_body = { # 연도별 정렬 -> 필름 완성된 날짜가 빠른순
             f.endDate.year: [
                {
                    'film_id': film.pk,
                    'start_date': str(film.startDate.month)+'월 '+str(film.startDate.day)+'일',
                    'end_date': str(film.endDate.month)+'월 '+str(film.endDate.day)+'일'
                }for film in Film.objects.filter(owner=user.pk, endDate__year=f.endDate.year).order_by('endDate')
            ]for f in Film.objects.filter(owner=user.pk).order_by('endDate')
        }
        return JsonResponse(response_body, status=200)
    else:
        return HttpResponse(status=400)


# 5. 필름통 하나를 눌렀을 때 해당 필름의 정보 넘겨주기 GET <int:pk>
def film_detail(request, pk):
    user = find_user_by_sid(request)
    if request.method == 'GET':
        try:
            film = Film.objects.get(pk=pk, owner=user.pk)
        except: # 로그인한 사람과 필름통의 소유 권한이 다를 때
            return HttpResponse('Invalid request', status=400)
        response_body = {
            'start_date': str(film.startDate.month)+'월 '+str(film.startDate.day)+'일',
            'end_date': str(film.endDate.month)+'월 '+str(film.endDate.day)+'일',
            'diaries': [
                {
                    'image': diary.image,
                    'created_at': diary.createdAt.strftime("%Y-%m-%d")
                } for diary in Diary.objects.filter(belong_to_film=film.pk)
            ]
        }
        return JsonResponse(response_body, status=200)
    else:
        return HttpResponse(status=400)
