import jwt
from django.conf import settings

def validate_user_and_get_user_id(token):
    """
    Validates a JWT token.
    """
    if token is None:
        return 0
    
    token = token.split()
    if len(token) != 2:
        return 0
    
    try:
        decoded_token = jwt.decode(token[1], settings.SECRET_KEY_JWT, algorithms=['HS256'])
        return decoded_token["id"]

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return 0