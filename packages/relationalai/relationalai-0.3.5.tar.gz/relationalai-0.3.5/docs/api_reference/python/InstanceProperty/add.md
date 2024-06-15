# `relationalai.InstanceProperty.add()`

```python
relationalai.InstanceProperty.add(other: Any) -> None
```

Add a value to a multi-valued property, creating the property if it doesn't exist.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | The value to be added to the property. Acceptable value types include [`Producer`](../Producer/README.md) objects, as well as numbers, strings, dates, and `datetime` objects. |

## Returns

`None`

## Example

```python
import relationalai as rai

# Create a model named "books" with Author and Book types.
model = rai.Model("books")
Author = model.Type("Author")
Book = model.Type("Book")

# Add authors and books to the model.
with model.rule():
    vonnegut = Author.add(name="Kurt Vonnegut")
    vonnegut.books.add(Book.add(title="Cat's Cradle"))
    asimov = Author.add(name="Isaac Asimov")
    asimov.books.add(Book.add(title="Foundation"))
    asimov.books.add(Book.add(title="Foundation and Empire"))

# Retrieve titles of books written by Isaac Asimov.
with model.query() as select:
    book = Author(name="Isaac Asimov").books
    response = select(book.title)

print(response.results)
# Output:
#                    title
# 0             Foundation
# 1  Foundation and Empire
```

In the example above, `vonnegut.books.add()` creates the multi-valued property `books` for the `vonnegut` object.
In contrast, the `Author.name` property is single-valued as it is defined through [`Type.add()`](../Type/add.md).
Single-valued properties can also be established using [`Instance.set()`](../Instance/set.md).
Calling `InstanceProperty.add()` on a single-valued property raises an `Exception`:

```python
# Attempt to add a second author name to the book titled "Foundation".
# The author property is single-valued because it is created with Instance.add().
with model.rule():
    Author(name="Isaac Asimov").name.add("Paul French")

# Output:
# Exception: Trying to use a property `name` as both singular and multi-valued
```

You can add values to multi-valued properties across multiple rules.
For instance, the next rule adds another book to Kurt Vonnegut's `books` property:

```python
with model.rule():
    author = Author(name="Kurt Vonnegut")
    author.books.add(Book.add(title="Slaughterhouse-Five"))

with model.query() as select:
    book = Author(name="Kurt Vonnegut").books
    response = select(book.title)

print(response.results)
# Output:
#                  title
# 0         Cat's Cradle
# 1  Slaughterhouse-Five
```

To add multiple values at once, use the [`InstanceProperty.extend()`](./extend.md) method:

```python
with model.rule():
    author = Author.add(name="Frank Herbert")
    author.books.extend([Book.add(title="Dune"), Book.add(title="Dune Messiah")])
```

## See Also

[`.extend()`](./extend.md) and [`.choose()`](./choose.md).
