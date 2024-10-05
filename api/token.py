import jwt
from django.conf import settings

def validate_user(token):
    """
    Validates a JWT token.
    """
    if token is None:
        return False
    
    token = token.split()
    if len(token) != 2:
        return False
    
    try:
        jwt.decode(token[1], settings.SECRET_KEY_JWT, algorithms=['HS256'])
        return True 
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False  