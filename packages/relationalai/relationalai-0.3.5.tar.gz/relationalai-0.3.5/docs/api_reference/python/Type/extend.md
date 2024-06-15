# `relationalai.Type.extend()`

```python
relationalai.Type.extend(self, *args: Type, **kwargs: Any) -> None
```

Extends the type with all objects from the types passed as positional arguments.
Keyword arguments are set as properties on the objects.
You can call `Type.extend()` outside of a [rule](../Model/rule.md) or [query](../Model/query.md) context.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | [`Type`](./README.md) | Any additional types to which the object being added belongs. |
| `*kwargs` | `Any` | Properties to set on the objects. |

## Returns

`None`.

## Example

```python
import relationalai as rai

model = rai.Model("books")

# Create a type named Book.
Book = model.Type("Book")
Fiction = model.Type("Fiction")
Fantasy = model.Type("Fantasy")
SciFi = model.Type("SciFi")

# Add some book instances to the Book type.
with model.rule():
    Book.add(SciFi, name="Foundation", author="Isaac Asimov")
    Book.add(Fantasy, name="The Hobbit", author="J.R.R. Tolkien")

# The finction type should include all Fantasy and SciFi books,
# so we extend it with the Fantasy and SciFi types.
Fiction.extend(Fantasy)
Fiction.extend(SciFi)
```

## See Also

[`Type.add()`](./add.md)
