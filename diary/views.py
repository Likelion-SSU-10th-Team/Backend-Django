from django.shortcuts import render
import json

from django.views.decorators.csrf import csrf_exempt

from .models import Diary, Comment
from accounts.models import User
from django.http import HttpResponse, JsonResponse
# Create your views here.


#일기쓰기
@csrf_exempt
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
        return HttpResponse("일기작성 성공", status=200)

    except KeyError:
        return JsonResponse({"message": "INVALID_KEYS"}, status=400)


#댓글작성
@csrf_exempt
def comment(request, diary_id):
    data = json.loads(request.body)

    try:
        user = User.objects.get(session_id=request.COOKIES.get('session_id'))
        diary = Diary.objects.get(pk=diary_id, writer=user.pk)
        if diary:
            Comment.objects.create(
                belong_to_diary=diary,
                comment=data['comment']
            ).save()
        return HttpResponse("댓글작성 성공", status=200)

    except KeyError:
        return JsonResponse({"message": "INVALID_KEYS"}, status=400)