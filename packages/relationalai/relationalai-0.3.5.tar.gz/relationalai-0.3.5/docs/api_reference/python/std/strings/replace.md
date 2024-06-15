# `relational.std.strings.replace()

```python
relationalai.std.strings.replace(string: Producer, old: str | Producer, new: str | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces strings by replacing all occurrences of the substring `old` in strings from the `string` Producer with the substring `new`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `string` | `str` or [`Producer`](../../../Producer/README.md) | A string or a producer that produces string values. |
| `old` | `str` or [`Producer`](../../../Producer/README.md) | The substring to replace. |
| `new` | `str` or [`Producer`](../../../Producer/README.md) | The substring to replace `old` with. |

## Returns

An [`Expression`](../../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std.strings import replace

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")

# Replace all occurrences of "ice" with "icia".
with model.query() as select:
    person = Person()
    replaced_name = replace(person.name, "ice", "icia")
    response = select(replaced_name)

print(response.results)
# Output:
#     name       v
# 0  Alice  Alicia
# 1    Bob     Bob
```
