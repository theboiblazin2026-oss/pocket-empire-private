---
name: Django
description: ORM, admin panel, authentication, REST framework
---

# Django Skill

## Models

```python
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
```

## Views

```python
from django.http import JsonResponse
from django.views import View

class UserListView(View):
    def get(self, request):
        users = User.objects.all().values()
        return JsonResponse(list(users), safe=False)

# Function-based
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return JsonResponse({'name': user.name})
```

## Django REST Framework

```python
from rest_framework import serializers, viewsets

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

## Commands

```bash
django-admin startproject myproject
python manage.py startapp myapp
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## When to Apply
Use when building Python web applications with Django.
