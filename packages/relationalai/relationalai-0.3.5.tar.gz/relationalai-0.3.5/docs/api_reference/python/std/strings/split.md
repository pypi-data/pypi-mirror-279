# `relational.std.strings.split()`

```python
relationalai.std.strings.split(string: str | Producer, separator: str | Producer) -> tuple[Expression]
```

Returns a tuple of [`Expression`](../../Expression.md) objects
where the first element produces the zero-based indices of each substring in `string` that is separated by `separator`
and the second element produces the substrings themselves.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `string` | `str` or [`Producer`](../../../Producer/README.md) | A string or a producer that produces string values. |
| `separator` | `str` or [`Producer`](../../../Producer/README.md) | A string or a producer that produces string values. |

## Returns

A tuple of two [`Expression`](../../Expression.md) objects.

## Example

```python
import relationalai as rai
from relationalai.std.strings import split

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
    index, substring = split(person.name, " ")
    with index == 0:
        person.set(first=substring)
    with index == 1:
        person.set(last=substring)

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

[`split_part`](./split_part.md), [`join`](./join.md), and [`concat`](./concat.md).
