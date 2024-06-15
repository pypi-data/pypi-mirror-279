<!-- markdownlint-disable MD024 -->

# `relationalai.InstanceProperty`

```python
class relationalai.InstanceProperty()
```

Instances of `InstanceProperty`, a subclass of [`Producer`](../Producer/README.md),
produce property values within [rule](../Rule/README.md) or [query](../Query/README.md) contexts.
They are instantiated by accessing attributes of an [`Instance`](../Instance/README.md).

## Methods

In addition to the methods inherited from [`Producer`](../Producer/README.md), `InstanceProperty` supports:

| Name | Description | Returns |
| :------ | :---------- | :------ |
| [`.or_(value: Any)`](./or_.md) | Set a default property value on objects lacking a value. | `InstanceProperty` |
| [`.in_(others: Iterable[Any])`](./in_.md) | Check if the property value is in a collection. | [`Expression`](../Expression.md) |
| [`.add(other: Any)`](./add.md) | Add a value to a property, creating the property if it doesn't exist. | `None` |
| [`.extend(others: Iterable[Any])`](./extend.md) | Extend a multi-valued property with multiple values from an iterable, creating the property if it doesn't exist. | `None` |
| [`.choose(n: int)`](./choose.md) | Choose `n` values from a multi-valued property. | `tuple` of `n` [`Instance`](../Instance/README.md) |
| [`.set(*args, **kwargs)`](./set.md) | Set properties or assigns types to the object associated with the current `InstanceProperty`. | [`Instance`](../Instance/README.md) |

## Example

As [producers](../Producer/README.md), instances of `InstanceProperty` serve as variables in
[rules](../Rule/README.md) or [queries](../Query/README.md) that represent property values of objects.
You create them by accessing attributes of an [`Instance`](../Instance/README.md):

```python
import relationalai as rai

# Create a model named "books" with a Book type.
model = rai.Model("books")
Book = model.Type("Book")

# Add some books to the model.
with model.rule():
    # Each call to `Book.add` creates a book with title, author, and year_published properties.
    Book.add(title="Foundation", author="Isaac Asimov", year_published=1951)
    Book.add(title="Foundation and Empire", author="Isaac Asimov", year_published=1952)
    Book.add(title="Dune", author="Frank Herbert")  # Note that year_published is not set.

# Get the names of books authored by Isaac Asimov.
with model.query() as select:
    # Get all books.
    book = Book()
    # InstanceProperty objects are created by accesing an attribute of an Instance, like book.author.
    # Here it is used in an expression to filter books by author.
    book.author == "Isaac Asimov"
    # Select the book.title property to include in the query result.
    response = select(book.title)

print(response.results)
# Output:
#                    title
# 0             Foundation
# 1  Foundation and Empire
```

Envision this rule executing for each book in the model, with each book passing through the rule's criteria sequentially:

1. `Book()` returns an  [`Instance`](../Instance/README.md) that produces a `Book` object.
2. `book.author` returns an `InstanceProperty` for the author's name.
   The [`==` operator](../Producer/eq__.md) filters books by comparing `book.author` to "Isaac Asimov".
3. `book.title` returns an `InstanceProperty` for the book's title, which is selected in the query results.

`InstanceProperty` supports various comparison and mathematical operators such as `==`, `!=`, `<`, `+`, `-`, `*`, `/`, and `%`.
The following example demonstrates using the [`%` operator](../Producer/mod__.md) with `InstanceProperty`
to filter books published in an even-numbered year:

```python
# Get books published in an even numbered year.
with model.query() as select:
    book = Book()
    book.year_published % 2 == 0  # Filter books by even year.
    response = select(book.title, book.year_published)

print(response.results)
# Output:
#                    title  year_published
# 0  Foundation and Empire            1952
```

For the full list of supported operators, see the [`Producer`](../Producer/README.md) class documentation.


By default, `InstanceProperty` outputs `None` for undefined properties,
which may display as `NaN` in the query's pandas `DataFrame` depending on the property's data type.


```python
# Get the genre and rating of each book.
with model.query() as select:
    book = Book()
    response = select(book.title, book.year_published)

print(response.results)
# Output:
#                    title  year_published
# 0                   Dune             NaN
# 1             Foundation          1951.0
# 2  Foundation and Empire          1952.0
```

Use [`.or_()`](./or_.md) to assign default values to properties lacking explicit values:


```python
with model.query() as select:
    book = Book()
    response = select(book.title, book.year_published.or_(-1))

print(response.results)
# Output:
#                    title  year_published
# 0                   Dune              -1
# 1             Foundation            1951
# 2  Foundation and Empire            1952
```

By default, properties support only a single value, and setting a new value overwrites the previous one.
You can create and manage multi-valued properties by using [`.add()`](./add.md) or [`.extend()`](./extend.md):

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
```

See the documentation for [`.add()`](./add.md) and [`.extend()`](./extend.md) for further details on multi-valued properties.

## See Also

[`Producer`](./Producer/README.md), [`Instance`](./Instance/README.md) and [`Expression`](../Expression.md).
