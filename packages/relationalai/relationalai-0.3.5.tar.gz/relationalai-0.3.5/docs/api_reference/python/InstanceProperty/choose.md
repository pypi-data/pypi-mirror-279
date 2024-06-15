# `relationalai.InstanceProperty.choose()`

```python
relationalai.InstanceProperty.choose(n: int, unique: bool = True) -> tuple[Producer]
```

Choose `n`-combinations of values from a multi-valued property,
returning them as a tuple `(v1, v2, ..., vn)` of [`Producer`](../Producer/README.md) objects.
By default, `unique` is `True`, and combination are sorted in ascending order with no repeated values.
If `unique` is `False`, all possible permutations (including repeated values) are produced.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `n` | `int` | The number of values to choose. Must be a positive integer. |
| `unique` | `bool` | If `True`, the combination is sorted in ascending order with no repeated values. If `False`, all possible permutations (including repeated values) are produced. Default is `True`. |

## Returns

A tuple of `n` [`Producer`](../Producer/README.md) objects.

## Example

Use `.choose()` the get pairs, triples, or other combinations of values from a multi-valued property:

```python
import relationalai as rai

# Create a model named "books" with Author and Book types.
model = rai.Model("books")
Author = model.Type("Author")
Book = model.Type("Book")

# Add some authors and books to the model.
with model.rule():
    Author.add(name="Kurt Vonnegut").books.add(Book.add(title="Cat's Cradle"))
    Author.add(name="Isaac Asimov").books.extend([
        Book.add(title="Foundation"),
        Book.add(title="Foundation and Empire")
    ])

# Get pairs of books written by the same author.
with model.query() as select:
    author = Author()
    book1, book2 = author.books.choose(2)
    response = select(book1.title, book2.title)

print(response.results)
# Output:
#         title                 title2
# 0  Foundation  Foundation and Empire
```

The model only contains one book for Kurt Vonnegut, so it is impossible to choose two unique books,
which is why the dataframe returned by the query only contains titles of books by Isaac Asimov.

Set `unique=False` to get all possible permutations (including repeated values) of books by the same author:

```python
with model.query() as select:
    author = Author()
    book1, book2 = author.books.choose(2, unique=False)
    response = select(book1.title, book2.title)

print(response.results)
# Output:
#                    title                 title2
# 0           Cat's Cradle           Cat's Cradle
# 1             Foundation             Foundation
# 2             Foundation  Foundation and Empire
# 3  Foundation and Empire             Foundation
# 4  Foundation and Empire  Foundation and Empire
```

`.choose()` should only be used with multi-valued properties.
Calling it on a single-valued property, such a book's `title` property, returns producers that produce no values:

```python
with model.query() as select:
    title1, title2 = Book().title.choose(2)
    respose = select(title1, title2)

print(response.results)
# Output:
# Empty DataFrame
# Columns: []
# Index: []
```

Passing a `0` or a negative value to `.choose()` raises a `ValueError`:

```python
with model.query() as select:
    title = Book().title.choose(0)
    response = select(title)

# Output:
# ValueError: Must choose a positive number of items
```

## See Also

[`.add()`](./add.md) and [`.extend()`](./extend.md).
