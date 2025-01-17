from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
import re

# 모델에서 validator 작성 가능
# MinLengthValidator 등 장고에서 기본적으로 제공하는 validator 있음

textLength_validator = MinLengthValidator(3, "3글자 이상 입력해주세요.")


def validate_phone(value):
    regex = re.compile('\d{2,3}-\d{3,4}-\d{4}')

    if not regex.match(value):
        raise ValidationError("0-0-0형식의 전화번호를 입력해주세요.")


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to="image", default='image/default_img.jpg')
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(blank=True, validators=[textLength_validator])
    phone = models.CharField(max_length=50, null=True, blank=True, validators=[validate_phone])

    def realname(self):
        return self.user.username

    def follower_count(self):
        return self.follower.values().count()

    def following_count(self):
        return self.following.values().count()

    def post_count(self):
        return self.posts.values().count()

    def __str__(self):
        return self.nickname


class Post(Base):
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager(blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    can_comment = models.BooleanField(default=True)
    text = models.TextField(null=True)

    def __str__(self):
        return '{} : {}'.format(self.writer, self.text)

    def like_count(self):
        return self.post_likes.values().count()

    def comment_count(self):
        return self.post_comments.values().count()

    class Meta:
        ordering = ['-created_at']


class File(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to="image")


class Comment(Base):
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    root = models.ForeignKey('self', null=True, related_name='root_comment', on_delete=models.CASCADE, blank=True)
    text = models.TextField(max_length=500)

    def __str__(self):
        return '{} : {}'.format(self.commenter, self.text)


class Follow(Base):
    follower = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='follower', on_delete=models.CASCADE)

    def __str__(self):
        return '{} -> {}'.format(self.follower, self.following)


class Like(Base):
    liker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)

    def __str__(self):
        return '{} -> {}'.format(self.liker, self.post)
