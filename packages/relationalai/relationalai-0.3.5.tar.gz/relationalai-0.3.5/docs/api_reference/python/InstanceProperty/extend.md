# `relationalai.InstanceProperty.extend()`

```python
relationalai.InstanceProperty.extend(others: Iterable[Any]) -> None
```

Extend a multi-valued property with multiple values from an iterable,
creating the property if it doesn't exist.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `others` | `Iterable[Any]` | The values to add to the property. Acceptable value types include [`Producer`](../Producer/README.md) objects, as well as numbers, strings, dates, and `datetime` objects. |

## Returns

`None`

## Example

```python
import relationalai as rai

# Create a model named "books" with Author and Book types.
model = rai.Model("books")
Author = model.Type("Author")
Book = model.Type("Book")

# Add multiple books to an author using extend.
with model.rule():
    herbert = Author.add(name="Frank Herbert")
    herbert.books.extend([
        Book.add(title="Dune"),
        Book.add(title="Dune Messiah"),
        Book.add(title="Children of Dune")
    ])

# Get the titles of books written by Frank Herbert.
with model.query() as select:
    book = Author(name="Frank Herbert").books   # Get all books by Frank Herbert.
    response = select(book.title)  # Select the title property of the book.

print(response.results)
# Output:
#               title
# 0  Children of Dune
# 1              Dune
# 2      Dune Messiah
```

In the example above, `herbert.books.extend()` creates the multi-valued property `books` for the `herbert` object.
In contrast, the `Author.name` property is single-valued as it is defined through [`Type.add()`](../Type/add.md).
Single-valued properties can also be established using [`Instance.set()`](../Instance/set.md).
Calling `InstanceProperty.extend()` on a single-valued property raises an `Exception`:

```python
# Attempt to extend the author name property with multiple values.
# The author property is single-valued because it is created with Type.add().
with model.rule():
    Author(name="Isaac Asimov").name.extend(["Franklin Herbert", "Franklin Patrick Herbert, Jr."])

# Output:
# Exception: Trying to use a property `name` as both singular and multi-valued
```

Single values can be added to a multi-valued property by passing an iterable containing one value,
or directly using the [`InstanceProperty.add()`](./add.md) method.

You can extend multi-valued properties across multiple rules.
For instance, the next rule adds two more books to Frank Herbert's `books` property:

```python
with model.rule():
    author = Author(name="Frank Herbert")
    author.books.extend([
        Book.add(title="God Emperor of Dune"),
        Book.add(title="Heretics of Dune")
    ])
```

## See Also

[`.add()`](./add.md) and [`.choose()`](./choose.md).
