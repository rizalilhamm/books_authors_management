from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from api.models import FavoriteBook, User, Books
from api.serializers import FavoriteBookSerializer
from api.token import validate_user_and_get_user_id
from api.levenshtein_distance import find_most_similar_words
from django.core import serializers


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
    
    def recommend_books(self, user, book, title):
        
        # recommended_books = find_most_similar_words(favorite_book.title)
        books = Books.objects.filter(title__icontains=title)[:5]
        recommended_books = list(books.values('id', 'title'))  # Get only 'id' and 'title'

        if len(recommended_books) < 5:
            needed_count = 5 - len(recommended_books)
        
            additional_books = Books.objects.exclude(id__in=[book['id'] for book in recommended_books])[:needed_count]
            recommended_books.extend(list(additional_books.values('id', 'title')))
        
        return list(recommended_books)
    
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
        if FavoriteBook.objects.filter(user_id=user_id).count() >= 20:
            return Response({"error": "You currently have a limit of 20 favorite books"}, status=status.HTTP_400_BAD_REQUEST)
        
        is_exist = FavoriteBook.objects.filter(user=user, book=book).values()    
        if len(is_exist) > 0:
            is_exist = is_exist[0]
            recommended_books = self.recommend_books(user, book, is_exist['title'])
            return Response({"error": "Book is already in favorites", "title": is_exist["title"], "recommended_books": list(recommended_books)}, status=status.HTTP_400_BAD_REQUEST)

        favorite_book = FavoriteBook(user=user, book=book, title=book.title)
        favorite_book.save()
        
        # recommended_books = find_most_similar_words(favorite_book.title)
        
        recommended_books = self.recommend_books(user, book, favorite_book.title)

        return Response({"message": "Book added to favorites","title": favorite_book.title, "recommended_books": list(recommended_books)}, status=status.HTTP_201_CREATED)

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