# `relational.std.strings.split_part()`

```python
relationalai.std.strings.split_part(string: str | Producer, separator: str | Producer, index: int | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) object that produces the substring of `string` that is separated by `separator` at the given `index`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `string` | `str` or [`Producer`](../../../Producer/README.md) | The string to split. |
| `separator` | `str` or [`Producer`](../../../Producer/README.md) | The separator to split the string by. |
| `index` | `int` or [`Producer`](../../../Producer/README.md) | The zero-based index of the substring to return. |

## Returns

An [`Expression`](../../Expression.md) object that producer `string` values.

## Example

```python
import relationalai as rai
from relationalai.std.strings import split_part

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    alice = Person.add(name="Alice Smith")
    bob = Person.add(name="Bob Jones")

# Create 'first' and 'last' properties by splitting the 'name' property.
with model.rule():
    person = Person()
    person.set(
        first=split_part(person.name, " ", 0),
        last=split_part(person.name, " ", 1)
    )

# Query the 'first' and 'last' properties.
with model.query() as select:
    person = Person()
    response = select(person.first, person.last)

print(response.results)
# Output:
#    first   last
# 0  Alice  Smith
# 1    Bob  Jones
```

## See Also

[`split`](./split.md), [`join`](./join.md), and [`concat`](./concat.md).
