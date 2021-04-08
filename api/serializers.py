from rest_framework import serializers
from api.models import Profile, Post, File, Comment, Like, Follow
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'commenter', 'text', 'root']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['liker', 'post']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following']


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    # files = FileSerializer(many=True, read_only=True)
    writer_nickname = serializers.SerializerMethodField()
    post_comments = CommentSerializer(many=True, read_only=True)
    post_likes = LikeSerializer(many=True, read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ['id', 'writer_nickname', 'writer', 'tags', 'text', 'location', 'files',
                  'can_comment', 'post_comments', 'post_likes']

    def get_writer_nickname(self, obj):
        return obj.writer.nickname


class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(read_only=True)
    # posts = PostSerializer(many=True, read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
    follower = FollowSerializer(many=True, read_only=True)
    following = FollowSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'nickname', 'website', 'bio', 'follower', 'following', 'likes']
