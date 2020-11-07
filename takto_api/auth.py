from django.contrib.auth.middleware import AuthenticationMiddleware
from rest_framework import authentication, exceptions

from takto_api.apps.business.models import User
from django.http import HttpResponseForbidden


class AuthMiddleware(AuthenticationMiddleware):
    def __call__(self, request):

        try:
            request.user = User.objects.get(device_id=request.META['HTTP_AUTHORIZATION'])
        except User.DoesNotExist:
            raise HttpResponseForbidden

        return self.get_response(request)


class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            user = User.objects.get(device_id=request.META['HTTP_AUTHORIZATION'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None
