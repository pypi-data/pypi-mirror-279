# `relational.std.strings.join()`

```python
relationalai.std.strings.join(strings: Sequence[str | Producer], separator: str | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces strings made by
concatenating all of the strings in `strings`, separated by the `separator` value.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `strings` | [Sequence](https://docs.python.org/3/glossary.html#term-sequence) of `str` or [`Producer`](../../../Producer/README.md) objects. | A sequence, such as a list or tuple, of strings to be joined. |
| `separator` | `str` or [`Producer`](../../../Producer/README.md) | The string to use as the separator value. |

## Returns

An [`Expression`](../../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std.strings import join

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    alice = Person.add(first="Alice", last="Smith")
    bob = Person.add(first="Bob", last="Jones")

# Join the first and last names of all people separated by a space.
with model.query() as select:
    person = Person()
    full_name = join([person.first, person.last], " ")
    response = select(full_name)

print(response.results)
# Output:
#              v
# 0  Alice Smith
# 1    BobJ ones
```

The sequence of strings to join can have any length.

## See Also

[`concat`](./concat.md)
