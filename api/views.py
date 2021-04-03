from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.models import Post
from api.serializers import PostSerializer


@csrf_exempt
def post_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def get_one_post(request, pk):  # 특정 id 값을 갖는 게시물만 보여줌
    if request.method == 'GET':
        posts = Post.objects.filter(id=pk)  # get으로 하면 안됨: not iterable 에러, filter 써야 queryset 반환
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

