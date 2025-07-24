import json
import requests
import datetime
import jwt
from jwt.algorithms import RSAAlgorithm
from django.conf import settings
from login.models import Email

def get_public_key(kid):
    jwks = requests.get(settings.SUPABASE_JWKS_URL).json()
    key = next((k for k in jwks['keys'] if k['kid'] == kid), None)
    if not key:
        raise ValueError("Clave pública no encontrada")
    return RSAAlgorithm.from_jwk(json.dumps(key))

def verify_supabase_jwt(token):
    header = jwt.get_unverified_header(token)
    public_key = get_public_key(header['kid'])
    payload = jwt.decode(
        token,
        public_key,
        algorithms=['RS256'],
        issuer=f"https://{settings.SUPABASE_PROJECT_URL}/auth/v1",
        audience=None,
        options={"verify_exp": True}
    )
    return payload


def login_with_supabase(email: str, password: str):
    url = f"{settings.SUPABASE_PROJECT_URL}/auth/v1/token?grant_type=password"
    headers = {
        "apikey": settings.SUPABASE_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "email": email,
        "password": password
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Login Supabase falló: {response.json()}")

    return response.json()  # Contiene el JWT y user info
