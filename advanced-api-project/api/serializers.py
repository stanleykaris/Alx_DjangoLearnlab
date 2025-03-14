from rest_framework import serializers
from .models import Author, Book
from django.utils import timezone

# Serializer for the Book model

"""
Serializer for the Book model, including fields for title, publication year, 
and author. Validates that the publication year is not set in the future.
"""
class BookSerializer(serializers.ModelSerializer):
    """
Meta class for the Book serializer, specifying the model and the fields to be included.
"""
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']
    
    """
Serializer for the Book model, including fields for title, publication year, 
and author. Validates that the publication year is not set in the future.
"""
    def validate(self, data):
        if data['publication_year'] > timezone.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return data

"""
Serializer for the Author model, including fields for name and a list of books.
The books field is read-only and uses the BookSerializer to represent related
Book instances.
"""
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    
    """
Meta class for the Book serializer, specifying the model and the fields to be included
in the serialized output: title, publication year, and author.
"""
    class Meta:
        model = Author
        fields = ['name', 'books']