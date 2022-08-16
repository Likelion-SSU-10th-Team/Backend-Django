from django.shortcuts import render, get_object_or_404
import json
import bcrypt
from .models import User
from album.models import Album
import requests as rq
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse


@csrf_exempt
def register(request):
    print(request.body)
    data = json.loads(request.body)

    try:
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({"message": "EXISTS_EMAIL"}, status=400)
        user = User.objects.create(
            email=data['email'],
            password=bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
            name=data['name']
        )
        Album(
            name='기본',
            owner=user
        ).save()
        return HttpResponse(status=200)

    except KeyError:
        return JsonResponse({"message": "INVALID_KEYS"}, status=400)


@csrf_exempt
def login(request):
    data = json.loads(request.body)
    user = get_object_or_404(User, email=data["email"])

    try: # email이랑 password로 존재하는 회원가입을 하였는지 체크
        if User.objects.filter(email=data["email"]).exists()\
                and bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
            session_id = user.email+user.password
            user.session_id = session_id
            user.save()
            # chrome이든 edge든 response에 session_id 값 만들어서 리턴해주기
            response = {
                "session_id": session_id
            }
            # response = JsonResponse({"msg": "login success"}, status=200)
            # response.headers('session_id', session_id)
            response = JsonResponse(response, status=200)
            response.set_cookie('session_id', session_id, samesite='None', secure=True)
            response.__setitem__('session_id', session_id)
            response.__setitem__('authorization', session_id)
            return response

        return JsonResponse({"msg": "invalid pw"}, status=400)

    except KeyError:
        return JsonResponse({'message': "INVALID_KEYS"}, status=400)


@csrf_exempt
def logout(request):
    # session_id랑 user가 일치하는지 확인하는 부분도 필요할 듯?
    try:
        user = User.objects.get(session_id=request.COOKIES.get('session_id'))
        if user.session_id:
            user.session_id = ""
            user.save()

            response = HttpResponse("로그아웃 성공", status=200)
            response.delete_cookie('session_id')
            return response

        return HttpResponse(status=400)

    except KeyError:
        return JsonResponse({'message': "INVALID_KEYS"}, status=400)


def session(request):
    print(request.COOKIES)
    print(request.COOKIES.get('sessionid')) # edge
    print(request.COOKIES.get('JSESSIONID')) # chrome
    response = HttpResponse('session 테스트')
    response.__setitem__('session_id', 'qqq')
    response.__setitem__('authorization', 'qqq')
    response.set_cookie('test', 'test1111')
    return response


def test(request):
    url = "https://port-0-backend-django-1k5zz25l6f9nen1.gksl1.cloudtype.app/accounts/session"
    # url = "http://localhost:8000/accounts/session"
    result = rq.get(url).headers
    print(result)
    return HttpResponse(result, status=200)
