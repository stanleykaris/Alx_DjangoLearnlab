from django.db import models

# Create your models here.

"""
Represents an author with a name attribute.

Attributes:
    name (CharField): The name of the author, with a maximum length of 200 characters.

Methods:
    __str__(): Returns the string representation of the author, which is the author's name.
"""
class Author(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

"""
Represents a book with a title, author, and publication year.

Attributes:
    title (CharField): The title of the book, with a maximum length of 200 characters.
    author (ForeignKey): A reference to the Author of the book, with a cascade delete behavior.
    publication_year (IntegerField): The year the book was published.
"""
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.IntegerField()