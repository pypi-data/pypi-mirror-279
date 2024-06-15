# `relational.std.strings.regex_compile()`

```python
relationalai.std.strings.regex_compile(regex: str | Producer) -> Expression
```

Returns an [`Expression`](../../../Expression.md) representing a compiled regular expression.
The compiled expression may be used in subsequent calls to [`regex_match`](./regex_match.md).

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `regex` | `str` or [`Producer`](../../../Producer/README.md) | A string containing a regular expression. |

## Returns

An [`Expression`](../../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std.strings import regex_match, regex_compile

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
    pattern = regex_compile(r"Ali.*")
    regex_match(person.name, pattern)
    response = select(person.name)

print(response.results)
# Output:
#     name
# 0  Alice
```

## See Also

[`regex_match`](./regex_match.md).
