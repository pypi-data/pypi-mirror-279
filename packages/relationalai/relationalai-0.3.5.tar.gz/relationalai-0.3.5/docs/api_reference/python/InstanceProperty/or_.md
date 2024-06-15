# `relationalai.InstanceProperty.or_()`

```python
relationalai.InstanceProperty.or_(other: Any) -> InstanceProperty
```

Produces a default property value for objects that lack one or have it set to `None`.
Returns an [`InstanceProperty`](./README.md) that produces the original values, along with the default value `other`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | The default property value. Supported types include [`Producer`](../Producer/README.md) objects, numbers, strings, dates, and `datetime` objects. For optimal performance, the type should match the values produced by the `InstanceProperty`. |

## Returns

An [`InstanceProperty`](./README.md) object.

## Example

Use `.or_()` to assign a default property value to objects where the property is either unset or set to `None`:

```python
import relationalai as rai

# Create a model named "books" with a Book type.
model = rai.Model("books")
Book = model.Type("Book")

# Add some books to the model.
with model.rule():
    Book.add(title="Foundation", author="Isaac Asimov")
    Book.add(title="Dune", author="Frank Herbert")
    Book.add(title="Sir Gowain and the Green Knight")

# Get the title and publication year of all books.
with model.query() as select:
    # Get all book objects.
    book = Book()
    # Select the title and author properties of the books.
    # `.or_()` sets a default value of "Unknown" for books without an author.
    response = select(book.title, book.author.or_("Unknown"))

print(response.results)
# Output:
#                              title         author
# 0                             Dune  Frank Herbert
# 1                       Foundation   Isaac Asimov
# 2  Sir Gowain and the Green Knight        Unknown
```

Above, `book` is an [`Instance`](../Instance/README.md) that produces `Book` objects.
`book.author.or_("Unknown")` returns an `InstanceProperty` that produces the author's name
or `"Unknown"` if the book lacks an `author` property, such as in "Sir Gawain and the Green Knight."

Without `.or_()`, the query outputs `None` for books lacking an author.
In the resulting pandas `DataFrame`, `None` may appear as `NaN`, depending on the column type:

```python
# Get the title and publication year of all books.
with model.query() as select:
    book = Book()
    response = select(book.title, book.author)  # .or() is not used.

print(response.results)
# Output:
#                              title         author
# 0                             Dune  Frank Herbert
# 1                       Foundation   Isaac Asimov
# 2  Sir Gowain and the Green Knight            NaN
```

`.or_()` also works with multi-valued properties created using [`.add()`](./add.md) or [`.extend()`](./extend.md):


```python
# Add genres to the books.
# genres is a multi-valued property because it is created with Instance.extend().
with model.rule():
    Book(title="Foundation").genres.extend(["Science Fiction"])
    Book(title="Dune").genres.extend(["Science Fiction", "Adventure"])

# Get the genres of all books.
with model.query() as select:
    book = Book()
    # Select the title and genres properties of the books.
    # `.or_()` sets a default value of "Unknown" for books without genres.
    response = select(book.title, book.genres.or_("Unknown"))

print(response.results)
# Output:
#                              title           genres
# 0                             Dune        Adventure
# 1                             Dune  Science Fiction
# 2                       Foundation  Science Fiction
# 3  Sir Gowain and the Green Knight          Unknown
```

## See Also

[`.in_()`](./in_.md) and [`.set()`](./set.md).
