from rest_framework import serializers
from .models import Authors, Books, FavoriteBook

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = '__all__'  
        
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = [
            'id',
            'title',
            'work_id',
            'isbn',
            'isbn13',
            'asin',
            'language',
            'average_rating',
            'rating_dist',
            'ratings_count',
            'text_reviews_count',
            'publication_date',
            'original_publication_date',
            'format',
            'edition_information',
            'image_url',
            'publisher',
            'num_pages',
            'series_id',
            'series_name',
            'series_position',
            'shelves',
            'description',
        ]
        
class FavoriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        fields = ['id', 'user', 'book_id', 'title', 'created_at']  