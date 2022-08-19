import boto3, json, random, string

from django.views.decorators.csrf import csrf_exempt

from .models import Diary, Comment
from accounts.models import User
from django.http import HttpResponse, JsonResponse
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, IMAGE_URL
# Create your views here.


#일기쓰기
@csrf_exempt
def diary_write(request):
    print(request.POST)
    print(request.FILES)
    n = 20
    rand_str = ""
    for i in range(n):
        rand_str += str(random.choice(string.ascii_uppercase + string.digits))
    try:
        user = User.objects.get(session_id=request.COOKIES.get('session_id'))
        print("현재 유저 : ")
        print(user)
        image_url = "https://myimageimagebucket.s3.ap-northeast-2.amazonaws.com/example/default.png"
        print(request.FILES.get('image'))
        if request.FILES.get('image') is not None:
            image = request.FILES.__getitem__('image')
            s3r = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            key = "%s" % (user)
            image._set_name(rand_str)
            s3r.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=key + '/%s' % (image), Body=image, ContentType='.png')
            image_url = IMAGE_URL + "%s/%s" % (user, image)
        content = request.POST['content']

        if user.session_id:
            Diary(
                writer=user,
                belong_to_film=user.current_film,
                image=image_url,
                content=content
            ).save()
        return JsonResponse({"msg": "일기 작성 성공"}, status=200)

    except KeyError:
        return JsonResponse({"message": "INVALID_KEYS"}, status=400)


#댓글작성
@csrf_exempt
def comment(request):
    data = json.loads(request.body)

    try:
        user = User.objects.get(session_id=request.COOKIES.get('session_id'))
        diary = Diary.objects.get(pk=data['diary_id'], writer=user.pk)
        if diary:
            Comment.objects.create(
                belong_to_diary=diary,
                comment=data['comment']
            ).save()
        return JsonResponse({"msg": "댓글 작성 성공"}, status=200)

    except KeyError:
        return JsonResponse({"message": "INVALID_KEYS"}, status=400)
