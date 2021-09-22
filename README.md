# Django로 instagram 클론해보기

- djanog project : insta
- django app : posts





### 기타 문서파일 생성

.gitignore

README.md



### 가상환경 설정 및 실행

pip -m venv venv

source venv/Scripts/activate



### 장고 설치

```bash
$ pip install django

# requirements.txt 생성
$ pip freeze > requirements.txt
# requirements.txt 설치
$ pip install -r requirements.txt
```



### project 생성

```bash
$ django-admin startproject insta . 
```



###  app 생성 - posts

```bash
$ python manage.py startapp posts
```

```python
# insta/settings.py
INSTALLED_APPS = [
    'posts',
]
```



### base.html 생성 및 기본설정 변경

```python
# insta/settings.py
'DIRS': [ BASE_DIR / 'templates' ],

LANGUAGE_CODE = 'ko-kor'
TIME_ZONE = 'Asia/Seoul'

# templates/base.html 생성
! + Tab
<div class="container">
  {% block body %}
  {% endblock  %}
</div>
```



### bootstrap 설치

```html
<head>
	...
    <!-- CSS only -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">
</head>


<body>
    ...
	<!-- JavaScript Bundle with Popper -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-/bQdsTh/da6pkI1MST/rWKFNjaCP5gBSY4sEBT38Q/9RBh9AH40zEOg7Hlq2THRZ" crossorigin="anonymous"></script>
</body>
```



### 앱 url 연결

```python
# insta/urls.py
from django.urls import path, include

urlpatterns = [
    path('posts/', include('posts.urls')),
]
```



### model 생성

```python
# posts/models.py
from django.db import models

class Post(models.Model):
    id_name = models.CharField(max_length=50)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
```



### form 생성

```python
# posts/forms.py 생성
# posts/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = '__all__'
```



### urls.py 생성

```python
# posts/urls.py 생성
# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    
]
```



### INDEX

```python
# posts/views.py
from django.shortcuts import render
from .models import Post
from django.views.decorators.http import require_safe

# Create your views here.
@require_safe
def index(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)
```

```python
# posts/templates/posts/index.html 생성
{% extends 'base.html' %}

{% block body %}
  {% for post in posts %}
    {{ post.id_name }}
    {{ post.content }}
    {{ post.created }}
  {% endfor %}
{% endblock  %}
```



### 관리자 계정 생성

```python
# posts/admin.py
from django.contrib import admin
from .models import Post

# Register your models here.
admin.site.register(Post)
```

```bash
$ python manage.py createsuperuser
```



### migration

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```



### runserver

```bash
$ python manage.py runserver
```



### CREATE

```python
# posts/urls.py
urlpatterns = [
    path('create/', views.create, name='create'),
]

# views.py
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.views.decorators.http import require_http_methods, require_safe

@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'posts/form.html', context)
```

```html
{% extends 'base.html' %}

{% block body %}

  <form action="" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>

{% endblock  %}
```



### DETAIL

```python
# posts/urls.py
urlpatterns = [
    path('<int:pk>/',views.detail, name='detail'),
]

# views.py
from django.shortcuts import render, redirect, get_object_or_404

@require_safe
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'posts/detail.html', context)
```

```html
# posts/templates/posts/index.html
{% extends 'base.html' %}
{% block body %}
  {% for post in posts %}
    <p>
      <a href="{% url 'posts:detail' post.pk %}">{{ post.id_name }}</a>
      {{ post.content }}
      {{ post.created }}
    </p>
  {% endfor %}
{% endblock  %}


# posts/templates/posts/form.html
{% extends 'base.html' %}
{% block body %}
  <p>{{ post.id_name }}</p>
  <p>{{ post.content }}</p>
  <p>{{ post.created }}</p>
{% endblock  %}
```



### UPDATE

```python
# posts/urls.py
urlpatterns = [
	path('<int:pk>/update/',views.update, name='update'),
]

@require_http_methods(['GET', 'POST'])
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', post.pk)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
    }
    return render(request, 'posts/form.html', context)
```

```html
# posts/templates/posts/detail.html
<a href="{% url 'posts:update' post.pk %}">update</a>
```



### DELETE

```python
# posts/urls.py
urlpatterns = [
	path('<int:pk>/delete/',views.delete, name='delete'),
]

# posts/views.py
from django.views.decorators.http import require_POST, require_http_methods, require_safe

@require_POST
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('posts:index')
```

```html
# posts/templates/posts/delete.html
<form action="{% url 'posts:delete' post.pk %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="delete">
</form>
```



### _navbar.html

```html
# templates/_navbar.html
<nav class="navbar navbar-expand-sm navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="{% url 'posts:index' %}">Instagram</a>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <form class="d-flex ms-auto">
        <input class="form-control me-2 text-center" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
      
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="{% url 'posts:index' %}">H</a>
        </li>

        <li class="nav-item">
          <a class="nav-link" href="#">M</a>
        </li>
...
```

- `navbar-expand-sm`
- `ms-auto`

```html
# templates/base.html
{% include '_navbar.html' %}
```



### _card.html

```html
<div class="card mb-3">
  <div class="card-header"><b>{{ post.id_name }}</b></div>
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <b>{{ post.id_name }}</b>
    {{ post.content }}<br>
    <small class="text-muted">{{ post.created }}</small>
  </div>
</div>
```

- `<br>`

```html
# posts/templates/posts/index.html
{% include 'posts/_card.html' %}
```



### naturaltime

```python
# insta/settings.py
INSTALLED_APPS = [
    'django.contrib.humanize',
]
```

```html
# posts/templates/posts/_cards.html
{% load humanize %}
<small class="text-muted">{{ post.created|naturaltime }}</small>
```



### image 업로드

```python
# insta/settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# media/images

# insta/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# posts/models.py
image = models.ImageField(upload_to='images/')
## or ##
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

image = ProcessedImageField(upload_to='images/',
                            processors=[ResizeToFill(400,400)],
                            format='JPEG',
                            options={'quality': 100})

# posts/views.py
def create(request):
    ...
    form = PostForm(request.POST, request.FILES)
    ...
    
def update(request):
    ...
    form = PostForm(request.POST, request.FILES, instance=post)
    ...
```

```html
# posts/templates/posts/form.html
<form action="" method="POST" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>

# posts/templates/posts/_cards.html
<img src="{{ post.image.url }}" class="card-img-top" alt="...">
```

migration



### Static 설정

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]

# static/images
```

```html
# templates/_navbar.html
{% load static %}
<img src="{% static 'images/logo.png' %}" alt="">
```





### 새로운 포스팅부터 표시하기

```python
# posts/views.py
@require_safe
def index(request):
    posts = Post.objects.all().order_by('-pk')

    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)
```



###  app 생성 - accounts

```bash
$ python manage.py startapp accounts
```

```python
# insta/settings.py
INSTALLED_APPS = [
    'accounts',
]
```



### url 연결

```python
# insta/urls.py
urlpatterns = [
	path('accounts/', include('accounts.urls')),
]
```



### signup

```python
# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]


# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    UserCreationForm,
)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)
```

```html
# accounts/templates/accounts/signup.html
{% extends 'base.html' %}

{% block body %}
  <form action="" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
  
{% endblock  %}
```

- `<form action="" method="POST">`



### login

```python
# accounts/urls.py
urlpatterns = [
    path('login/', views.login, name='login'),
]


# accounts/views.py
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django.contrib.auth import login as auth_login

def login(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'posts:index')
            
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)
```



### logout

```python
# accounts/urls.py
urlpatterns = [
    path('logout/', views.logout, name='logout'),
]


# accounts/views.py
from django.contrib.auth import logout as auth_logout

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect(request, 'posts:index')
```



### profile

```python
# accounts/urls.py
urlpatterns = [
    path('<str:username>/', views.profile, name='profile'),
]


# accounts/views.py
from django.contrib.auth.models import User

def profile(request, username):
    user = User.objects.get(username=username)
    
    context = {
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)
```

```html
# templates/base.html
<a href="{% url 'accounts:profile' user.username %}">profile</a>

# accounts/templates/accounts/profile.html
{% extends 'base.html' %}

{% block body %}
  {{ user.username }}
{% endblock  %}
```



### delete

```python
# accounts/urls.py
urlpatterns = [
	path('delete/', views.delete, name='delete'),
]


# accounts/views.py
from django.contrib.auth.models import User

def profile(request, username):
    user = User.objects.get(username=username)
    
    context = {
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)
```

```html
# templates/base.html
<a href="{% url 'accounts:profile' user.username %}">profile</a>

# accounts/templates/accounts/profile.html
{% extends 'base.html' %}

{% block body %}
  {{ user.username }}
{% endblock  %}
```























### imagekit

```bash
$ pip install pillow
$ pip install pilkit
$ pip install django-imagekit
```



### models 및 form 생성

```python
# posts/models.py
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Post(models.Model):
    image = ProcessedImageField(upload_to = 'images/',
                                processors=[ResizeToFill(500, 500)],
                                format = 'JPEG',
                                options = {'quality': 100})
    idname = models.CharField(max_length=50)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
    
# posts/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = '__all__'
```



### index.url 생성

```python
# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
]
```



```python
# posts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
```



```python
def index(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
    }

    return render(request, 'posts/index.html', context)
```



posts/templates/posts



### 관리자계정 생성

- 관리자 계정으로 게시물 생성 후 확인

```python
# posts/admin.py
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```



```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```



### 이미지 업로드

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# media/images
```



### 시간을 0 mins ago 형태로

```python
# settings.py
INSTALLED_APPS = [  
    'django.contrib.humanize',
]
```

```html
{% load humanize %}

{{ post.created | naturaltime }}
```

