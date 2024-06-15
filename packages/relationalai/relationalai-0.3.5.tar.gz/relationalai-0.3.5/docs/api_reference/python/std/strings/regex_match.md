# `relational.std.strings.regex_match()`

```python
relationalai.std.strings.regex_match(string: str | Producer, regex: str | Producer) -> Expression
```

Adds a constraint to a [rule](../../Model/rule.md) or [query](../../Model/query.md) that
`string` must match the regular expression `regex`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `string` | `str` or [`Producer`](../../../Producer/README.md) | The string to match against. |
| `regex` | `str` or [`Producer`](../../../Producer/README.md) | A string containing a regular expression. |

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

# Get all people whose name ends with "ice".
with model.query() as select:
    person = Person()
    regex_match(person.name, r"Ali.*")
    response = select(person.name)

print(response.results)
# Output:
#     name
# 0  Alice
```

## See Also

[`regex_compile`](./regex_compile.md).
