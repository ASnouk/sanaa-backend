from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from .firebase import verify_firebase_token

User = get_user_model()


class FirebaseAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            id_token = auth_header.split("Bearer ")[1]
        except IndexError:
            raise exceptions.AuthenticationFailed("Invalid token format")

        decoded_token = verify_firebase_token(id_token)

        if not decoded_token:
            raise exceptions.AuthenticationFailed("Invalid Firebase token")

        phone = decoded_token.get("phone_number")
        firebase_uid = decoded_token.get("uid")

        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={"username": firebase_uid}
        )

        return (user, None)
