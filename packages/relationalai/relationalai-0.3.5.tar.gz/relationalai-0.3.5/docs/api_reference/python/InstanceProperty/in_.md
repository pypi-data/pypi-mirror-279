# `relationalai.InstanceProperty.in_()`

```python
relationalai.InstanceProperty.in_(others: Iterable[Any]) -> Expression
```

Checks if any value produced by `InstanceProperty` exists within a specified collection.
This method returns an [`Expression`](../Expression.md) that filters objects and property values
based on their membership in the `others` iterable.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `others` | `Iterable[Any]` | Collection of values for checking membership. Supports [`Producer`](../Producer/README.md) objects, numbers, strings, dates, and `datetime` objects. |

## Returns

An [`Expression`](../Expression.md) object that filters objects and property values based on their membership in the `others` collection.

## Example
Use `.in_()` to filter objects in a [rule](../Rule/README.md) or [query](../Query/README.md) context,
checking if their property values exist within a specified collection:

```python
import relationalai as rai

# Create a model named "books" with a Book type.
model = rai.Model("books")
Book = model.Type("Book")

# Add some books to the model.
with model.rule():
    Book.add(title="Foundation", author="Isaac Asimov")
    Book.add(title="Cat's Cradle", author="Kurt Vonnegut")
    Book.add(title="Dune", author="Frank Herbert")

# Get the titles of books written by Kurt Vonnegut or the author of Foundation.
with model.query() as select:
    book = Book()  # Get all book objects.
    book.author.in_(["Kurt Vonnegut", Book(title="Foundation").author])  # Filter books by author in the collection.
    response = select(book.title, book.author)  # Select the title and author properties of the books.

print(response.results)
# Output:
#           title         author
# 0  Cat's Cradle  Kurt Vonnegut
# 1    Foundation   Isaac Asimov
```


In the above example, `book` is an [`Instance`](../Instance/README.md) that produces `Book` objects.
`book.author.in_()` returns an [`Expression`](../Expression.md) that filters books to include
only those authored by `"Kurt Vonnegut"` or the author of `"Foundation"`.

If no authors from the collection match, the query yields no results:

```python
with model.query() as select:
    book = Book()  # Get all book objects.
    book.author.in_(["Ted Chiang", "J.R.R. Tolkien"])  # Filter books by author in the collection.
    response = select(book.title, book.author)  # Select the title and author properties of the books.

print(response.results)
# Output:
# Empty DataFrame
# Columns: []
# Index: []
```

`.in_()` also works with multi-valued properties,
such as properties created with [`.add()`](./add.md) or [`.extend()`](./extend.md):

```python
# Add genres to the books.
# The genre property is multi-valued because it is created with Instance.extend().
with model.rule():
    Book(title="Foundation").genres.extend(["Science Fiction", "Space Opera"])
    Book(title="Cat's Cradle").genres.extend(["Science Fiction", "Satire"])
    Book(title="Dune").genres.extend(["Science Fiction", "Space Opera"])

# Get books with the genre "Satire", "Fantasy", or both.
with model.query() as select:
    book = Book()  # Get all book objects.
    book.genres.in_(["Satire", "Fantasy"])  # Filter books by genre in the collection.
    response = select(book.title, book.author, book.genres)  # Select the title and genre properties of the books.

print(response.results)
# Output:
#           title         author  genres
# 0  Cat's Cradle  Kurt Vonnegut  Satire
```

Note that only the `"Satire"` genre appears in the results.
This is because `book.genres` produces multiple values, and `.in_()` filters both the `book` objects and their `genres`.
Consequently, only genres that meet the filter criteria are included in the final results.

## See Also

[`.or_()`](./or_.md) and [`.set()`](./set.md)