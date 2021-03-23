from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to="image", default='default_img/default_img.jpg')
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return '{} / {}'.format(self.user.username, self.nickname)
