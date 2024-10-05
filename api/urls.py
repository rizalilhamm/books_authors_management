from django.urls import path
from api.author_views import AuthorsView
from api.book_views import BooksView
from api.user_views import UserView

urlpatterns = [
    path('user/<str:action>', UserView.as_view(), name='user-action'),
    
    path('authors', AuthorsView.as_view(), name='authors'),
    path('authors/<str:id>', AuthorsView.as_view(), name='author-detail'),
    
    path('books', BooksView.as_view(), name='books'),
    path('books/<str:id>', BooksView.as_view(), name='books-detail'),   
]
