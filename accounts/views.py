from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
import bcrypt, json, random, string
from .models import User
from album.models import Album
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
    print(request)
    n = 20
    rand_str = ""
    for i in range(n):
        rand_str += str(random.choice(string.ascii_uppercase + string.digits))
    print(request.COOKIES.get('session_id'))
    data = json.loads(request.body)
    user = get_object_or_404(User, email=data["email"])

    try: # email이랑 password로 존재하는 회원가입을 하였는지 체크
        if User.objects.filter(email=data["email"]).exists()\
                and bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
            session_id = rand_str
            user.session_id = session_id
            user.save()
            # chrome이든 edge든 response에 session_id 값 만들어서 리턴해주기
            response = JsonResponse({"msg": "login success"}, status=200)
            response.set_cookie('session_id', session_id, samesite='None', secure=True)
            response.__setitem__('session_id', session_id)
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


@csrf_exempt
def userinfo(request):
    session_id = request.COOKIES.get('session_id')
    print("session_id : " + session_id)
    user = get_object_or_404(User, session_id=session_id)
    print(user.name)
    return JsonResponse({"name": user.name}, status=200)


def session(request):
    print(request.headers)
    print(request.COOKIES.get('session_id'))
    response = HttpResponse('session 테스트')
    return response
