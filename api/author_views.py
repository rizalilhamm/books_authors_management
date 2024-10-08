# author_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Authors, BooksAuthors
from .serializers import AuthorSerializer
from api.token import validate_user_and_get_user_id


class AuthorsView(APIView):
    """
    Manage Authors: Retrieve, create, update, and delete authors.
    """
    
    def get(self, request, id=None):

        search_query = request.query_params.get('search', None)
        
        if search_query:
            authors = Authors.objects.filter(name__icontains=search_query)
            serializer = AuthorSerializer(authors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if id:
            try:
                author = Authors.objects.get(id=id)
                serializer = AuthorSerializer(author)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Authors.DoesNotExist:
                return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)


        # Limit by 50 because Books has large data, as alternative we can make pagination for it.
        authors = Authors.objects.all()[:50]
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        if not validate_user_and_get_user_id(request.headers.get('Authorization')):
            return Response({'error': 'Invalid Bearer Token'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id):
        
        if not validate_user_and_get_user_id(request.headers.get('Authorization')):
            return Response({'error': 'Invalid Bearer Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            author = Authors.objects.get(id=id)
        except Authors.DoesNotExist:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        if not validate_user_and_get_user_id(request.headers.get('Authorization')):
            return Response({'error': 'Invalid Bearer Token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            author = Authors.objects.get(id=id)

            BooksAuthors.objects.filter(author_id=author.id).delete()
            author.delete()

            return Response({'message': 'Authors deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Authors.DoesNotExist:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)