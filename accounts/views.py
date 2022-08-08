from django.shortcuts import render
import json
import bcrypt
from .models import User

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse


@csrf_exempt
def register(request):
    data = json.loads(request.body)

    try:
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({"message": "EXISTS_EMAIL"}, status=400)
        User.objects.create(
            email=data['email'],
            password=bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
            name=data['name'],
            age=data['age']
        ).save()
        return HttpResponse(status=200)

    except KeyError:
        return JsonResponse({"message": "INVALID_KEYS"}, status=400)


def login(request):
    data = json.loads(request.body)

    try:
        if User.objects.filter(email=data["email"]).exists():
            user = User.objects.get(email=data["email"])
            session_id = user.email+user.password
            user.session_id=session_id
            user.save()

            if bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
                return JsonResponse({"session_id": session_id}, status=200)

            return HttpResponse(status=401)

        return HttpResponse(status=400)

    except KeyError:
        return JsonResponse({'message': "INVALID_KEYS"}, status=400)


def logout(request):
    data = json.loads(request.body)

    try:
        user = User.objects.get(email=data["email"])
        if user.session_id:
            user.session_id = ""
            user.save()
            return JsonResponse({"session_id": user.session_id}, status=200)
        return HttpResponse(status=200)

    except KeyError:
        return JsonResponse({'message': "INVALID_KEYS"}, status=400)