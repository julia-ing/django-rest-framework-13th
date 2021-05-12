from django.http import Http404
from api.models import Profile, Post
from api.serializers import ProfileSerializer, PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django_filters import rest_framework as filters
from api.filters import PostFilter, ProfileFilter
from api.permissions import *


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter
    permission_classes = (IsWriterOrReadonly,)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProfileFilter
    permission_classes = (ProfileUpdatePermission,)


# FBV
# @csrf_exempt
# def post_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def get_one_post(request, pk):  # 특정 id 값을 갖는 게시물만 보여줌
#     if request.method == 'GET':
#         posts = Post.objects.filter(id=pk)  # get으로 하면 안됨: not iterable 에러, filter 써야 queryset 반환
#         serializer = PostSerializer(posts, many=True)
#         return JsonResponse(serializer.data, safe=False)


# CBV
# class ProfileList(APIView):
#     def get(self, request, format=None):
#         profiles = Profile.objects.all()
#         serializer = ProfileSerializer(profiles, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ProfileDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Profile.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         profile = self.get_object(pk)
#         profile.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
