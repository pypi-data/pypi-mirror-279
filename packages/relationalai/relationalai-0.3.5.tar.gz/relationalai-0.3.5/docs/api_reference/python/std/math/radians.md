# `relationalai.std.math.radians()`

```python
relationalai.std.math.radians(degrees: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) object that produces the equivalent number of `degrees` in radians.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `degrees` | `Number` or [`Producer`](../../Producer/README.md) | The number of degrees to convert to radians. |

## Returns

An [`Expression`](../../Expression.md) object that produces `float` values.

## Example

`radians()` works with both numeric [producers](../../Producer/README.md) and Python number objects:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import radians

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add a person to the model.
with model.rule():
    Person.add(name="Alice", age=30)

# radians() works with numeric producers, such as a person's age property.
with model.query() as select:
    person = Person()
    response = select(person.name, alias(radians(person.age), "radians_age"))

print(response.results)
# Output:
#     name  radians_age
# 0  Alice     0.523599

# radians() also works with Python number objects.
with model.query() as select:
    response = select(radians(180))

print(response.results)
# Output:
#           v
# 0  3.141593
```

## See Also

[`degrees()`](./degrees.md)
