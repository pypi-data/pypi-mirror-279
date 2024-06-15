# `relational.std.strings.uppercase()`

```python
relationalai.std.strings.uppercase(string: Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces the uppercase version
of the strings produced by the `string` producer.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `string` | [`Producer`](../../../Producer/README.md) | A producer that produces string values. |

## Returns

An [`Expression`](../../../Expression.md) object that produce uppercase strings.

## Example

```python
import relationalai as rai
from relationalai.std.strings import uppercase

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
    name_upper = uppercase(person.name)
    response = select(person.name, name_upper)

print(response.results)
# Output:
#     name      v
# 0  Alice  ALICE
# 1    Bob    BOB
```

## See Also

[`lowercase`](./lowercase.md)
