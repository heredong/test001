from rest_framework.authentication import BaseAuthentication

from .models import MyUser


class LoginAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_id = request.session.get("_auth_user_id")
        if user_id:
            user = MyUser.objects.get(pk=user_id)
            return user,user_id
        else:
            return None,None
