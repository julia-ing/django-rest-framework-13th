# CEOS 13기 백엔드 스터디 최예원
## REST API 서버 개발 - 인스타그램 클론

---

### 모델 설명
#### ERD 만들기
- ERD를 처음 만들어봤는데 쉽지 않았습니다. 구조를 잡아놓고 모델링을 시작했는데 
  제가 짠 ERD가 탄탄하지 않았는지 코드 작성하면서 관계를 바꾼 부분이 꽤 있었습니다ㅎㅎ 

![erd](./media/image/instagram_erd.PNG)
#### 모델 - Profile, Post, Comment, Follow, Like

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
        return self.nickname
```
1. 사용자 프로필 사진 : 이미지필드를 사용해봤습니다. 물론 모델링만 하는 과제였지만 잘 작동하는지 눈으로 확인해보고 싶어서
Pillow를 임포트해준 뒤 media/image 디렉토리를 생성하고 settings, urls를 수정해주는 작업을 했습니다. (admin.py에 등록해서 확인해봄)

- Post
```python
from taggit.managers import TaggableManager  # taggit 사용

class Post(models.Model):
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)
    can_comment = models.BooleanField(default=True)  # 댓글 허용 / 차단
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
        ordering = ['-created_at']  # 최신순으로 정렬
```
1. 게시물 : 이미지나 영상의 형태이기 때문에 확장자에 구애받지 않도록 파일필드 이용.
   
2. 해시태그 : manytomany -> [taggit](https://django-taggit.readthedocs.io/en/latest/getting_started.html) ... 
   이것도 마찬가지로 settings.py에 추가해주었고, 나중에 실제로 views나 urls 작성할 때 사용방법이 따로 있는 것 같아 살펴보는 중입니다. 
   
3. like_users : manytomany 연결, 한 게시물에 여러 개의 좋아요 / 한 사람이 여러 게시물에 좋아요

- Comment
```python
class Comment(models.Model):
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    root = models.ForeignKey('self', null=True, related_name='rootcomment', on_delete=models.CASCADE)  # 대댓글 기능
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.commenter, self.text)
```

- Follow
```python
class Follow(models.Model):  # 중요 기능은 아닌 것 같지만 가장 헷갈렸던 부분 중 하나
    follower = models.ForeignKey(Profile, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return '{} -> {}'.format(self.follower, self.following)
```

- Like
```python
class Like(models.Model):  # 중개 모델
    liker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='like_posts', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {}'.format(self.liker, self.post)
```

- File (피드백 반영 후 - 한 게시물에 여러 사진,영상이 올라갈 수 있으므로)
```python
class File(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to="image")  # 영상일 수도 있으므로 파일필드 이용
```
---

## ORM 적용해보기
```shell
>>> from api.models import User, Profile, Post
>>> User.objects.create(username='최예원')
>>> Profile.objects.create(user_id=1, nickname='yew0n_derful', bio='세오스 사랑해요')  # superuser
>>> Profile.objects.create(user_id=3, nickname='julia-ing', bio='세오스 사랑해요')  # admin에서 한번 생성 후 지웠더니 id값이 3이 됨

>>> Post.objects.create(writer=test_user2, text='우와 이게 되네요ㅎㅎ') # test_user2에 최예원 저장
<Post: julia-ing : 우와 이게 되네요ㅎㅎ>
>>> Post.objects.create(writer=test_user, text='푸쳐핸섭푸푸푸푸풋') # test_user에 yewon 저장
<Post: yew0n_derful : 푸쳐핸섭푸푸푸푸풋>

>>> Comment.objects.create(commenter=test_user, post=test_post, text='great')
<Comment: yew0n_derful : great>
>>> Comment.objects.create(commenter=test_user, post=test_post2, text='amazing')
<Comment: yew0n_derful : amazing>
>>> Comment.objects.create(commenter=test_user2, post=test_post, text='excellent')
<Comment: julia-ing : excellent>
>>> Comment.objects.create(commenter=test_user2, post=test_post2, text='perfect')
<Comment: julia-ing : perfect>

>>> Comment.objects.filter(commenter=test_user2)
<QuerySet [<Comment: julia-ing : excellent>, <Comment: julia-ing : perfect>]>
>>> Comment.objects.filter(post=test_post)
<QuerySet [<Comment: yew0n_derful : great>, <Comment: julia-ing : excellent>]>  
```

---

### 간단한 회고
1. ERD를 이번에 마음대로 짜봤다가 고생함. 다음부터는 처음부터 꼼꼼하게 열심히 짜야겠다.
2. tag를 mannytomany로 바꿀까? follow를 profile 필드로 넣어버릴까?
3. 이번 과제를 하며, 정돈되지 않았지만 여러 생각들을 많이 해본 것 같다. 
   다 하고 나니 뭔가 큰 일을 해낸 것 같은 기분이고, 모델링이 굉장히 중요한 작업이라는 것을 깨달았다.
4. 결론 : 모델링 너무 어렵다ㅜㅜ 아직 많이 부족한 것 같고, 더 열심히 노력해야겠다!!

---

---

## 3주차 과제 (기한: 4/1 목요일까지)
### 모델 선택 및 데이터 삽입
```python
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
        return self.post_comments.values().count()  # 카운트 메소드는 admin.py에서 확인하고 싶어서 넣어봤습니다.

    class Meta:
        ordering = ['-created_at']


class Comment(Base):
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    root = models.ForeignKey('self', null=True, related_name='root_comment', on_delete=models.CASCADE, blank=True)
    text = models.TextField(max_length=500)

    def __str__(self):
        return '{} : {}'.format(self.commenter, self.text)
```
![img.png](media/image/img.png)

### 모든 list를 가져오는 API
- URL: api/posts/
- Method: GET
```json
[
    {
        "id": 3,
        "writer_nickname": "jay_jhyunl",
        "writer": 3,
        "tags": [
            "맛집",
            "롯데월드몰"
        ],
        "text": "랍스타 무한리필",
        "location": "viking's wharf",
        "files": [
            3
        ],
        "can_comment": true,
        "post_comments": [],
        "post_likes": [
            {
                "liker": 2,
                "post": 3
            },
            {
                "liker": 1,
                "post": 3
            }
        ]
    },
    {
        "id": 2,
        "writer_nickname": "in_young912",
        "writer": 2,
        "tags": [
            "맛집"
        ],
        "text": "가로수길 새들러하우스 크로플 JMT",
        "location": "Saddler House",
        "files": [],
        "can_comment": true,
        "post_comments": [
            {
                "id": 1,
                "commenter": 1,
                "text": "근데 여기 웨이팅이 너무 길어 엉엉",
                "root": null
            },
            {
                "id": 2,
                "commenter": 2,
                "text": "그래두 기다려서라도 먹어봐야 하는 맛",
                "root": 1
            }
        ],
        "post_likes": []
    },
    {
        "id": 1,
        "writer_nickname": "yew0n_derful",
        "writer": 1,
        "tags": [
            "ceos"
        ],
        "text": "세오스 3주차 미션중",
        "location": "Seoul",
        "files": [
            1,
            2
        ],
        "can_comment": true,
        "post_comments": [
            {
                "id": 3,
                "commenter": 3,
                "text": "화이팅!!",
                "root": null
            }
        ],
        "post_likes": [
            {
                "liker": 3,
                "post": 1
            }
        ]
    }
]
```
files는 nested로 하면 너무 정신없어 보이길래 필드로만 전달해줬습니다.
추가적으로, 특정 id 값을 갖는 게시물만 불러와보는 걸 해봤습니다. 

- URL: api/posts/1
- Method: GET
```python
# api/urls.py
path('posts/<int:pk>', views.get_one_post)

#api/views.py
@csrf_exempt
def get_one_post(request, pk):  # 특정 id 값을 갖는 게시물만 보여줌
    if request.method == 'GET':
        posts = Post.objects.filter(id=pk)  # get으로 하면 안됨: not iterable 에러, filter 써야 queryset 반환
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
```

### 새로운 데이터를 create하도록 요청하는 API
- URL: api/posts/
- Method: POST
- Body: 
```json
{
    "id": 4,
    "writer_nickname": "yew0n_derful",
    "writer": 1,
    "tags": [
            "ceos",
            "django"
        ],
    "text": "포스트 요청 테스트 중입니다~",
    "location": "합정역 할리스",
    "files": [],
    "can_comment": true,
    "post_comments": [],
    "post_likes": []
}
```

### 공부한 내용 정리
1. Serializers - JSON형식의 데이터를 주고 받기 위해 모델 인스턴스를 직렬화, 인코딩 느낌
2. admin list_display - 

```text
list_display = ['id', 'writer', 'text', 'tag_list', 'like_count', 'comment_count']
```

   
3. postman에서 요청 보낼 때 get 을 제외한 요청들은 url 끝에 /가 있어야 함 (데이터 손실 가능성 때문..?)

4. id 대신 nickname을 보고 싶을때 (근데 이때 필드에 writer은 꼭 입력해주어야 post 가능)- 
```python
class PostSerializer(serializers.ModelSerializer):
    writer_nickname = serializers.SerializerMethodField()
    ~~~
    def get_writer_nickname(self, obj):
        return obj.writer.nickname
```
   
5. postman에서 post로 게시물 생성할 때 혹시나혹시나 likes까지 동시에 같이 생성할 수 있나 해봤는데 역시 안됐다...

### 간단한 회고
1. 재밌었다!! 모델링에 비해 수월하게 끝낸 것 같아 기분이 좋다ㅜㅜ 