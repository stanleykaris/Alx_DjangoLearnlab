# Deleting the Book from the Instance

```python
from bookshelf.models import Book

book = Book.objects.all()
book.delete()
#(1, {'bookshelf.Book': 1})
```
