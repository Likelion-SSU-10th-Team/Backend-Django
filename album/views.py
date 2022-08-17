import json

import diary.models as d
from accounts.models import User
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt


# session_id로 user 인식
def find_user_by_sid(request):
    session_id = request.COOKIES.get('session_id')
    print("session_id : " + session_id)
    return get_object_or_404(User, session_id=session_id)


# 앨범 리스트 보여주기
@csrf_exempt
def album_list(request):
    user = find_user_by_sid(request)
    try:
        list = []
        albums = Album.objects.filter(owner=user.pk)
        for album in albums:
            list.append(
                {
                    "album_id": album.pk,
                    "album_name": album.name
                }
            )
        return JsonResponse({"albums": list}, status=200)
    except:
        return JsonResponse({"albums": list}, status=200)


# + 버튼 눌렀을 때 앨범 생성 POST
@csrf_exempt
def make_album(request):
    user = find_user_by_sid(request)
    data = json.loads(request.body)
    if request.method == 'POST': # POST라면 -> 새 앨범 추가
        # Album 객체 생성
        album = Album(
            name=data['name'],
            owner=user
        )
        album.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


# 앨범 하나를 눌렀을 때 해당 앨범의 정보 넘겨주기 GET <int:album_id>
@csrf_exempt
def album_detail(request, album_id):
    user = find_user_by_sid(request)
    if request.method == 'GET':
        try:
            album = Album.objects.get(pk=album_id)
            diary_id = Composition.objects.filter(album=album)
            print(diary_id)

        except:  # 로그인한 사람과 앨범의 소유 권한이 다를 때
            return HttpResponse('Invalid request', status=400)
        # 영훈고친부분
        response_body = {
            'diaries': [
                {
                    'diary_id': diary.diary.pk,
                    'created_at': str(diary.diary.createdAt.month)+'월 '+str(diary.diary.createdAt.day)+'일',
                    'image': diary.diary.image,
                    'content': diary.diary.content
                } for diary in Composition.objects.filter(album=album)
            ]
        }
        #영훈고친부분끝
        return JsonResponse(response_body, status=200)
    else:
        return HttpResponse(status=400)


# diary의 정보 넘겨주기 / GET
@csrf_exempt
def diary_detail(request, album_id, diary_id):
    user = find_user_by_sid(request)
    if request.method == 'GET' :
        diary = d.Diary.objects.get(pk=diary_id, writer=user.pk)
        response_body = {
            'created_at': diary.createdAt.strftime("%Y.%m.%d"),
            'image': diary.image,
            'content': diary.content
        }
        return JsonResponse(response_body, status=200)
    else:
        return HttpResponse(status=400)


# album 선택 / POST
@csrf_exempt
def select_album(request, diary_id, album_id):
    user = find_user_by_sid(request)
    diary = d.Diary.objects.get(pk=diary_id, writer=user.pk)
    albums = Album.objects.filter(owner=user.pk)

    # album_id_list = [4, 5]
    # album_id_list = request.POST.getlist('selected_album[]')

    data = json.loads(request.body)
    album_id_list = data['selected_album']
    print(album_id_list)
    for i in range(len(album_id_list)):
        for album in albums:
            if album_id_list[i] == album.pk:
                composition = Composition(
                    diary=diary,
                    album=album
                )
            composition.save()

    return HttpResponse(status=200)


# 일기가 속한 앨범 목록
def send_album_id(request, diary_id):
    user = find_user_by_sid(request)
    if request.method == 'GET':
        try:
            diary = d.Diary.objects.get(pk=diary_id, writer=user.pk)
        except:
            return HttpResponse('Invalid request', status=400)
        # 해당 다이어리가 속한 앨범객체들 가져오기
        albumObjects = Composition.objects.filter(diary=diary.pk)
        # 다이어리가 속한 앨범의 pk를 배열 형태로 보내주기
        list = []
        for albumObject in albumObjects:
            list.append(
                {
                    "album_id": albumObject.album.pk,
                    "album_name": albumObject.album.name
                }
            )
        return JsonResponse({"album_name_list": list}, status=200)
    else:
        return HttpResponse(status=400)