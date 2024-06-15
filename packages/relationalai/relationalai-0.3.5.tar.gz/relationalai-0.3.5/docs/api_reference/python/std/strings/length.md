# `relational.std.strings.length()`

```python
relationalai.std.strings.length(string: str | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces the length of the string `string`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `string` | `str` or [`Producer`](../../../Producer/README.md) objects. | A string or a producer that produces string values. |

## Returns

An [`Expression`](../../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std.strings import length

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")

# Find the length of each person's name.
with model.query() as select:
    person = Person()
    name_length = length(person.name)
    response = select(p.name, name_length)

print(response.results)
# Output:
#     name  v
# 0  Alice  5
# 1    Bob  3
```
