import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
import os

cred = credentials.Certificate(
    os.path.join(settings.BASE_DIR, "config", "firebase_key.json")
)


if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


def verify_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        return None
