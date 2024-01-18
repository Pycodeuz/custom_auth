import jwt
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed

from users.models import User
from users.models import User


class CommonAuthMixin:
    def authenticate_user(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user = get_object_or_404(User, id=payload.get('id'))
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        return user


class News(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)


class Portfolio(models.Model):
    image = models.ImageField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    owner = models.ForeignKey(User, models.CASCADE, related_name='portfolio_owner')


class Comment(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(User, models.CASCADE, related_name='comment_owner')
