from rest_framework import authentication, exceptions

from takto_api.apps.business.models import User


class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            user = User.objects.get(device_id=request.META['HTTP_AUTHORIZATION'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None
