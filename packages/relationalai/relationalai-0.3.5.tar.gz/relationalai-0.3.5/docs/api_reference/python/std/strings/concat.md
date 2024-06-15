# `relational.std.strings.concat()`

```python
relationalai.std.strings.concat(string1: str | Producer, string2: str | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces strings by concatenating `string1` and `string2`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `string1` | `str` or [`Producer`](../../../Producer/README.md) | A string or a producer that produces string values. |
| `string2` | `str` or [`Producer`](../../../Producer/README.md) | A string or a producer that produces string values. |

## Returns

An [`Expression`](../../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std.strings import concat

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    alice = Person.add(first="Alice", last="Smith")
    bob = Person.add(first="Bob", last="Jones")

# Concatenate the first and last names of all people.
with model.query() as select:
    person = Person()
    full_name = concat(person.first, person.last)
    response = select(full_name)

print(response.results)
# Output:
#             v
# 0  AliceSmith
# 1    BobJones
```

To add a space between the first and last names, you can concatenate a space string with last name:

```python
concat = std.strings.concat
with model.query() as select:
    person = Person()
    full_name = concat(person.first, concat(" ", person.last))
    # Alternatively, you could use std.strings.join:
    # full_name = join([person.first, person.last], " ")
    response = select(full_name)

print(response.results)
# Output:
#              v
# 0  Alice Smith
# 1    Bob Jones
```

## See Also

[`join`](./join.md)
