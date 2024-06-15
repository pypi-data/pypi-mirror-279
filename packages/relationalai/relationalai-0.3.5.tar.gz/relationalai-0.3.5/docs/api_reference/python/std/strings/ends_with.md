# `relational.std.strings.ends_with()`

```python
relationalai.std.strings.ends_with(string: Producer, suffix: str | Producer) -> Expression
```

Constrains the `string` Producer to only values that end in `suffix`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `string` | [`Producer`](../../../Producer/README.md) | A producer that produces string values. |
| `suffix` | `str` or [`Producer`](../../../Producer/README.md) | The substring to check for. |

## Returns

An [`Expression`](../../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std.strings import ends_with

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")

# Get all people whose name ends with "ice".
with model.query() as select:
    person = Person()
    ends_with(person.name, "Ali")
    response = select(person.name)

print(response.results)
# Output:
#     name
# 0  Alice

# The `substring` argument can also be a Producer.
with model.query() as select:
    sub = Person(name="Bob").name
    person = Person()
    ends_with(person.name, sub)
    response = select(person.name)

print(response.results)
# Output:
#    name
# 0   Bob
```

## See Also

[`contains`](./contains.md)
