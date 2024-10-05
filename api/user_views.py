from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

class UserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, action):
        """
        Handle both registration and login actions based on the URL.
        action can be 'register' or 'login'.
        """

        if action == 'register':
            return self.register(request)
        elif action == 'login':
            return self.login(request)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    def register(self, request):
        # Get user data from request
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Validate the input
        if not username or not password or not email:
            return Response({'error': 'Please provide username, password, and email'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create(
            username=username,
            password=make_password(password),  # Hash the password
            email=email
        )

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    def login(self, request):
        # Get login data from request
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Create or retrieve a token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)