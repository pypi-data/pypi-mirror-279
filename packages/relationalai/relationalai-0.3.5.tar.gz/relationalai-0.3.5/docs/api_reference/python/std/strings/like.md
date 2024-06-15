# `relational.std.strings.like()`

```python
relationalai.std.strings.like(string: str | Producer, pattern: str | Producer) -> Expression
```

Adds a constraint to a [rule](../../Model/rule.md) or [query](../../Model/query.md) that
`string` must match the SQL LIKE pattern `pattern`.
The `%` character acts as a wildcard, matching any sequence of characters.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `string` | `str` or [`Producer`](../../../Producer/README.md) | The string to match against. |
| `pattern` | `str` or [`Producer`](../../../Producer/README.md) | A SQL LIKE pattern. |

## Returns

An [`Expression`](../../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std.strings import like

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")

# Get all people whose name contains 'li'.
with model.query() as select:
    person = Person()
    like(person.name, "%li%")
    response = select(person.name)

print(response.results)
# Output:
#     name
# 0  Alice
```

## See Also

[`contains`](./contains.md),
[`ends_with`](./ends_with.md),
[`regex_match`](./regex_match.md),
and [`starts_with`](./starts_with.md).
