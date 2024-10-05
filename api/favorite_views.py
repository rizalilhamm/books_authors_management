from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from api.models import FavoriteBook, User, Books
from api.serializers import FavoriteBookSerializer
from api.token import validate_user_and_get_user_id


class FavoriteBookAPIView(APIView):
    
    def get(self, request):
        """
        Retrieve all favorite books for the authenticated user.
        """
        user_id = validate_user_and_get_user_id(request.headers.get('Authorization')) 
        if not user_id:
            return Response({'error': 'Invalid Bearer Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects.get(id=user_id)
        
        favorite_books = FavoriteBook.objects.filter(user=user)
        serializer = FavoriteBookSerializer(favorite_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Add a book to the user's favorites.
        """
        
        user_id = validate_user_and_get_user_id(request.headers.get('Authorization')) 
        if not user_id:
            return Response({'error': 'Invalid Bearer Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects.get(id=user_id)
        
        book_id = request.data.get('book_id')
        if not book_id or int(book_id) == 0:
            return Response({'error': 'invalid paylaod'}, status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Books, id=book_id)
        
        if FavoriteBook.objects.filter(user=user, book=book).exists():
            return Response({"error": "Book is already in favorites"}, status=status.HTTP_400_BAD_REQUEST)

        favorite_book = FavoriteBook(user=user, book=book, title=book.title)
        favorite_book.save()

        return Response({"message": "Book added to favorites"}, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        """
        Delete a favorite book by its ID.
        """
        user_id = validate_user_and_get_user_id(request.headers.get('Authorization')) 
        if not user_id:
            return Response({'error': 'Invalid Bearer Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        user = User.objects.get(id=user_id)
        favorite_book = get_object_or_404(FavoriteBook, book=id, user=user)
        favorite_book.delete()

        return Response({"message": "Favorite book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)