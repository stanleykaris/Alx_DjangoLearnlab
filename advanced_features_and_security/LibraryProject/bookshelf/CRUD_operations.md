# CRUD Operations on the Book Model

## Creating a Book instance

```python
book = Book(title="1984", author="George Orwell", publication_year=1949)

book.save()
```

## Retrieving all books

```python
books = Book.objects.all()
```

## Updating the book title

```python
book.title = "Nineteen Eighty-Four"
book.save()
```

## Deleting book records

```python
book.delete()
#(1, {'bookshelf.Book': 1})
```
