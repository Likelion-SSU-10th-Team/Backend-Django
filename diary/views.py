from accounts.crud import user
from django.shortcuts import render
import json
from .models import Diary, Comment
from album import Album
from accounts.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


def diaryWrite(request):
    data = json.loads(request.body)

    try:
        user = User.objects.get(session_id=request.COOKIES.get('session_id'))
        if user.session_id:
            Diary.objects.create(
                writer=user,
                belong_to_film=user.current_film,
                image=data['image'],
                content=data['content']
            ).save()
        return HttpResponse(status=200)


    except KeyError:
        return JsonResponse({"message": "INVALID_KEYS"}, status=400)
# 임시저장 기능..
# 사진첩 추가 기능
def make_album(request) :
    data = json.loads(request.body)
    if request.method == 'POST': # POST라면 -> 새 앨범 추가
        # Album 객체 생성
        album = Album(
            name =data['name'],
            owner=user
        )
        album.save()
        return HttpResponseRedirect('http://localhost:8000/diary/')
    else:
        return HttpResponse(status=400)

#댓글작성
def comment(request):
    data = json.loads(request.body)

    try:
        user = User.objects.get(session_id=request.COOKIES.get('session_id'))
        diary = Diary.objects.get(writer=user.email)
        if diary.writer:
            Comment.objects.create(
                belong_to_diary=diary, #여긴 불확실함
                comment=data['comment']
            ).save()
        return HttpResponse(status=200)


    except KeyError:
        return JsonResponse({"message": "INVALID_KEYS"}, status=400)


def comment(request, diary_id) :
    data = json.loads(request.body)

    if request.method == 'POST':  # POST라면 -> 댓글 추가
        # Comment 객체 생성
        comment = Comment(
            content = data['comment'],
            belong_to_diary = diary_id
        )
        comment.save()
        return HttpResponse(status=200)

