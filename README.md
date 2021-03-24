# CEOS 13기 백엔드 스터디 최예원
## REST API 서버 개발
### 인스타그램 클론

---

## 모델 설명
### ERD 만들기
- ERD를 처음 만들어봤는데 쉽지 않았습니다. 구조를 잡아놓고 모델링을 시작했는데 
  제가 짠 ERD가 탄탄하지 않았는지 코드 작성하면서 관계를 바꾼 부분이 꽤 있었습니다ㅎㅎ 

![erd](./media/image/instagram_erd.PNG)
### 모델 - Profile, Post, Comment, Follow, Like

- Profile
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #유저모델 확장
    nickname = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to="image", default='image/default_img.jpg')
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return '{} / {}'.format(self.user.username, self.nickname)
```
1. 사용자 프로필 사진 : 이미지필드를 사용해봤습니다. 물론 모델링만 하는 과제였지만 잘 작동하는지 눈으로 확인해보고 싶어서
Pillow를 임포트해준 뒤 media/image 디렉토리를 생성하고 settings, urls를 수정해주는 작업을 했습니다. (admin.py에 등록해서 확인해봄)
```python
# config/settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#config/urls.py
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- Post
```python
from taggit.managers import TaggableManager  # taggit 사용

class Post(models.Model):
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.FileField(upload_to="image")
    # tags = models.ManyToManyField('Tag', verbose_name='해시태그', related_name='posts', blank=True)
    tags = TaggableManager(blank=True)
    text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} : {}'.format(self.writer, self.text)

    def like_count(self):        # migrate 시 문제 발생 -> db에서 디폴트 0으로 지정해줌
        return self.like_set.count()

    class Meta:
        ordering = ['-created_at']  # 최신순으로 정렬
```
1. 게시물 : 이미지나 영상의 형태이기 때문에 확장자에 구애받지 않도록 파일필드 이용.
   
2. 해시태그 : manytomany -> [taggit](https://django-taggit.readthedocs.io/en/latest/getting_started.html) ... 
   이것도 마찬가지로 settings.py에 추가해주었고, 나중에 실제로 views나 urls 작성할 때 사용방법이 따로 있는 것 같아 살펴보는 중입니다. 
   
3. like_count : migrate 시 문제가 생겨 mysql에서 default값을 0으로 직접 지정

- Comment
```python
class Comment(models.Model):
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    root = models.ForeignKey('self', null=True, related_name='rootcomment', on_delete=models.CASCADE)  # 대댓글 기능
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} : {}'.format(self.commenter, self.text)
```

- Follow
```python
class Follow(models.Model):
    follower = models.ForeignKey(Profile, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return '{} -> {}'.format(self.follower, self.following)
```

- Like
```python
class Like(models.Model):
    liker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {}'.format(self.liker, self.post)
```
---

## ORM 적용해보기
```shell
>>> from api.models import User, Profile, Post
>>> User.objects.create(username='최예원')
>>> Profile.objects.create(user_id=1, nickname='yew0n_derful', bio='세오스 사랑해요')  # superuser
>>> Profile.objects.create(user_id=3, nickname='julia-ing', bio='세오스 사랑해요')  # admin에서 한번 생성 후 지웠더니 id값이 3이 됨

>>> Post.objects.create(writer=test_user2, text='우와 이게 되네요ㅎㅎ') # test_user2에 최예원 저장
<Post: 최예원 / julia-ing : 우와 이게 되네요ㅎㅎ>
>>> Post.objects.create(writer=test_user, text='푸쳐핸섭푸푸푸푸풋') # test_user에 yewon 저장
<Post: yewon / yew0n_derful : 푸쳐핸섭푸푸푸푸풋>

>>> Comment.objects.create(commenter=test_user, post=test_post, text='great')
<Comment: yewon / yew0n_derful : great>
>>> Comment.objects.create(commenter=test_user, post=test_post2, text='amazing')
<Comment: yewon / yew0n_derful : amazing>
>>> Comment.objects.create(commenter=test_user2, post=test_post, text='excellent')
<Comment: 최예원 / julia-ing : excellent>
>>> Comment.objects.create(commenter=test_user2, post=test_post2, text='perfect')
<Comment: 최예원 / julia-ing : perfect>

>>> Comment.objects.filter(commenter=test_user2)
<QuerySet [<Comment: 최예원 / julia-ing : excellent>, <Comment: 최예원 / julia-ing : perfect>]>
>>> Comment.objects.filter(post=test_post)
<QuerySet [<Comment: yewon / yew0n_derful : great>, <Comment: 최예원 / julia-ing : excellent>]>  # 지저분해서 손봐야될 것 같음.
```

---

## 간단한 회고
1. ERD를 이번에 마음대로 짜봤다가 고생함. 다음부터는 처음부터 꼼꼼하게 열심히 짜야겠다.
2. tag를 mannytomany로 바꿀까? follow를 profile 필드로 넣어버릴까? like-post 다대다?
3. 결론 : 모델링 너무 어렵다ㅜㅜ 피드백 많이 해주세요..😭💪

