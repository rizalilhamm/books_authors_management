from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Books
from .serializers import BookSerializer
from api.token import validate_user


class BooksView(APIView):
    """
    API view to retrieve, create, update, and delete books.
    """
    
    def get(self, request, id=None):
        search_query = request.query_params.get('search', None)
        
        if search_query:
            authors = Books.objects.filter(title__icontains=search_query)
            serializer = BookSerializer(authors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if id: 
            try:
                book = Books.objects.get(id=id)
                serializer = BookSerializer(book)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Books.DoesNotExist:
                return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        books = Books.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        if not validate_user(request.headers.get('Authorization')):
            return Response({'error': 'Invalid Bearer Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id):
        if not validate_user(request.headers.get('Authorization')):
            return Response({'error': 'Invalid Bearer Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            book = Books.objects.get(id=id)
        except Books.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        
        if not validate_user(request.headers.get('Authorization')):
            return Response({'error': 'Invalid Bearer Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            book = Books.objects.get(id=id)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Books.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)