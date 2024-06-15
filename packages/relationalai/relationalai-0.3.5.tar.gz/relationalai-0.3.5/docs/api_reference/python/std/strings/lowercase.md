# `relational.std.strings.lowercase()`

```python
relationalai.std.strings.lowercase(string: Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces the lowercase version
of the strings produced by the `string` producer.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `string` | [`Producer`](../../../Producer/README.md) | A producer that produces string values. |

## Returns

An [`Expression`](../../../Expression.md) object that produce lowercase strings.

## Example

```python
import relationalai as rai
from relationalai.std.strings import lowercase

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
    name_lower = lowercase(person.name)
    response = select(person.name, name_lower)

print(response.results)
# Output:
#     name      v
# 0  Alice  alice
# 1    Bob    bob
```

## See Also

[`uppercase`](./uppercase.md)
