# `relationalai.std.math.atan()`

```python
relationalai.std.math.atan(number: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) object that produces the arctangent of `number` radians.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `number` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the arctangent of. |

## Returns

An [`Expression`](../../Expression.md) object that produces `float` values.

## Example

`atan()` works with both numeric [producers](../../Producer/README.md) and Python number objects:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import atan

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add a person to the model.
with model.rule():
    Person.add(name="Alice", age=3, height_m=0.95)

# atan() works with numeric producers, such as a person's height property.
# Inputs are assumed to be in radians.
with model.query() as select:
    person = Person()
    response = select(person.name, alias(atan(person.height_m), "atan_height"))

print(response.results)
# Output:
#     name  atan_height
# 0  Alice     0.759763

# atan() also works with Python number objects.
with model.query() as select:
    response = select(atan(0))

print(response.results)
# Output:
#      v
# 0  0.0
```

## See Also

[`tan()`](./sin.md), [`acos()`](./acos.md), and [`asin()`](./asin.md).
