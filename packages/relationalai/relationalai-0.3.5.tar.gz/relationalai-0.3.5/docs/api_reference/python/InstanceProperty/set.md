# `relationalai.InstanceProperty.set()`

```python
relationalai.InstanceProperty.set(*args: Type, **kwargs: Any) -> Instance
```

Set properties or assigns types to the object associated with the current `InstanceProperty`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | [`Type`](../Type/README.md) | Optional types to apply to the object. |
| `**kwargs` | `Any` | Properties to set on the objects with `<property_name>=<value>` format. Accepts [`Producer`](../Producer/README.md) objects, numbers, strings, dates, and `datetime` objects. |

## Returns

Returns the [`Instance`](../Instance/README.md) object on which the property or type is set.

## Example

Use `.set()` to assign properties and [types](../Type/README.md) directly on objects associated with a specific property:

```python
import relationalai as rai

# Create a model named "books" with Author and Book types.
model = rai.Model("books")
Author = model.Type("Author")
Book = model.Type("Book")

# Add some authors and books to the model.
with model.rule():
    Book.add(title="Foundation", author=Author.add(name="Isaac Asimov"))

# Set a note property on the author of the Foundation book.
with model.rule():
    Book(title="Foundation").author.set(note="Science fiction author")

with model.query() as select:
    author = Author()
    response = select(author.name, author.note)

print(response.results)
# Output:
#            name                    note
# 0  Isaac Asimov  Science fiction author
```

`.set()` also works with multi-valued properties created using [`.add()`](./add.md) or [`.extend()`](./extend.md):

```python
# Add a books property to the Author type.
with model.rule():
    # Get all books
    book = Book()
    # Get the author of the book.
    author = book.author
    # Create multi-values books property for the author and add the book to it.
    # books multi-valued because it is created with InstanceProperty.add().
    author.books.add(book)

# Set the genre property to "Sciene Fiction" on books by Isaac Asimov.
with model.rule():
    Author(name="Isaac Asimov").books.set(genre="Science fiction")

# Get the names of authors and the titles and genres of their books.
with model.query() as select:
    # Get all author objects.
    author = Author()
    # Select the name of the author and the title and genre of their books.
    response = select(author.name, author.books.title, author.books.genre)

print(response.results)
# Output:
#            name       title            genre
# 0  Isaac Asimov  Foundation  Science fiction
```

`InstanceProperty.set()` works exactly the same as `Instance.set()`.
See the [`Instance.set()`](../Instance/set.md) documentation for more examples and details.\

## See Also

[`Instance.set()`](../Instance/set.md)
