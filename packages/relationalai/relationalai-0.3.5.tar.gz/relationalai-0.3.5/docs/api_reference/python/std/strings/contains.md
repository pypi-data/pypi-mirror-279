# `relational.std.strings.contains()`

```python
relationalai.std.strings.contains(string: str | Producer, substring: str | Producer) -> Expression
```

Adds a constraint to a [rule](../../Model/rule.md) or [query](../../Model/query.md) that
`string` must contain the substring `substring`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `string` | [`Producer`](../../../Producer/README.md) | The string to check. |
| `substring` | `str` or [`Producer`](../../../Producer/README.md) | The substring to check for. |

## Returns

An [`Expression`](../../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std.strings import contains

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")

# Get all people whose name contains "Ali".
with model.query() as select:
    person = Person()
    contains(person.name, "Ali")
    response = select(person.name)

print(response.results)
# Output:
#     name
# 0  Alice

# The `substring` argument can also be a Producer.
with model.query() as select:
    sub = Person(name="Bob").name
    person = Person()
    contains(person.name, sub)
    response = select(person.name)

print(response.results)
# Output:
#    name
# 0   Bob
```

## See Also

[`ends_with`](./ends_with.md)
