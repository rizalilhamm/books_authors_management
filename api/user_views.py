from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import bcrypt
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth.models import User


class UserView(APIView):

    def post(self, request, action):
        """
        Handle both registration and login actions based on the URL 'register' or 'login'.
        """

        if action == 'register':
            return self.register(request)
        elif action == 'login':
            return self.login(request)
        
        return Response({'error': ' Error while login/register '}, status=status.HTTP_400_BAD_REQUEST)


    def register(self, request):

        username = request.data.get('username')
        password = request.data.get('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())                
        
        if not username or not password:
            return Response({'error': 'Please provide username, password'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            password=hashed_password,  
        )

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')        
        
        user = User.objects.filter(username=username).values()
        
        if len(user) <= 0:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        stored_password_hash = ast.literal_eval(user[0]['password'])
        
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        exp = datetime.utcnow() + timedelta(days=1)
        
        payload = {
            'iat': datetime.utcnow(),
            'nbf': datetime.utcnow(),
            'username': user[0]['username'],
            'role': "USER",
        }
        token = jwt.encode(
            payload,
            settings.SECRET_KEY_JWT, 
            algorithm='HS256'
        )
        
        return Response({'token': token, 'statusCode':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    