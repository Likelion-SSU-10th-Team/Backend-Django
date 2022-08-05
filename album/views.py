from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def album_list(request):

    albums = Album.objects.all()
    list = []
    for album in albums:
        list.append(
            {
                "album_name": album.name
            }
        )
    return JsonResponse({"albums": list}, status=200)
