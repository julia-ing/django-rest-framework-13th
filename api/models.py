from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to="image", default='image/default_img.jpg')
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nickname


class Post(models.Model):
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='writer')
    tags = TaggableManager(blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    can_comment = models.BooleanField(default=True)
    text = models.TextField(null=True)
    like_users = models.ManyToManyField(
        'Profile',
        through='Like',
        related_name='like_posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.writer, self.text)

    def like_count(self):
        return self.like_users.all().count()

    class Meta:
        ordering = ['-created_at']


class File(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to="image")


class Comment(models.Model):
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    root = models.ForeignKey('self', null=True, related_name='rootcomment', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.commenter, self.text)


class Follow(models.Model):
    follower = models.ForeignKey(Profile, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return '{} -> {}'.format(self.follower, self.following)


class Like(models.Model):
    liker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='like_posts', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {}'.format(self.liker, self.post)
