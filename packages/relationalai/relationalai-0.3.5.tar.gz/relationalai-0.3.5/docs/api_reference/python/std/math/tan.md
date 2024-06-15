# `relationalai.std.math.tan()`

```python
relationalai.std.math.tan(number: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) object that produces the tangent of `number` radians.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `number` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the tangent of. |

## Returns

An [`Expression`](../../Expression.md) object that produces `float` values.

## Example

`tan()` works with both numeric [producers](../../Producer/README.md) and Python number objects:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import tan

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add a person to the model.
with model.rule():
    Person.add(name="Alice", age=30)

# tan() works with numeric producers, such as a person's age property.
# Inputs are assumed to be in radians.
with model.query() as select:
    person = Person()
    response = select(person.name, alias(tan(person.age), "tan_age"))

print(response.results)
# Output:
#     name   tan_age
# 0  Alice -6.405331

# tan() also works with Python number objects.
with model.query() as select:
    response = select(tan(0))

print(response.results)
# Output:
#      v
# 0  0.0
```

## See Also

[`atan()`](./atan.md), [`cos()`](./cos.md), and [`sin()`](./sin.md).
