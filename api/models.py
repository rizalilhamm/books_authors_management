from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

    @classmethod
    def get_user_by_username(cls, username):
        try:
            return cls.objects.get(username=username)
        except cls.DoesNotExist:
            return None


class Authors(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    ratings_count = models.IntegerField()
    average_rating = models.FloatField()
    text_reviews_count = models.IntegerField()
    works_count = models.IntegerField()
    book_ids = models.JSONField() 
    work_ids = models.JSONField()
    image_url = models.URLField(max_length=200)
    about = models.TextField()
    fans_count = models.IntegerField()
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Authors'
        

class Books(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('Authors', related_name='Books')  # Many-to-many relationship
    work_id = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    isbn13 = models.CharField(max_length=20, blank=True, null=True)
    asin = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=50)
    average_rating = models.FloatField()
    rating_dist = models.TextField()
    ratings_count = models.IntegerField()
    text_reviews_count = models.IntegerField()
    publication_date = models.CharField(max_length=255, blank=True, null=True) 
    original_publication_date = models.CharField(max_length=255, blank=True, null=True) 
    format = models.CharField(max_length=50, blank=True, null=True)
    edition_information = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(max_length=200)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    series_id = models.CharField(max_length=255, blank=True, null=True)
    series_name = models.CharField(max_length=255, blank=True, null=True)
    series_position = models.CharField(max_length=10, blank=True, null=True)
    shelves = models.JSONField() 
    description = models.TextField()

    class Meta:
        db_table = 'Books'

    def __str__(self):
        return self.title
    
class FavoriteBook(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID field
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "FavoriteBook"
        unique_together = ('user', 'book')  # Ensures that a user can only add a book once

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.book.title}"