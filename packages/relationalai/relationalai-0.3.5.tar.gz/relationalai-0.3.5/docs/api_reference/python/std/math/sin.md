# `relationalai.std.math.sin()`

```python
relationalai.std.math.sin(number: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) object that produces the sine of `number` radians.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `number` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the sine of. |

## Returns

An [`Expression`](../../Expression.md) object that produces `float` values.

## Example

`sin()` works with both numeric [producers](../../Producer/README.md) and Python number objects:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import sin

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add a person to the model.
with model.rule():
    Person.add(name="Alice", age=30)

# sin() works with numeric producers, such as a person's age property.
# Inputs are assumed to be in radians.
with model.query() as select:
    person = Person()
    response = select(person.name, alias(sin(person.age), "sin_age"))

print(response.results)
# Output:
#     name   sin_age
# 0  Alice -0.988032

# sin() also works with Python number objects.
with model.query() as select:
    response = select(sin(0))

print(response.results)
# Output:
#      v
# 0  0.0
```

## See Also

[`asin()`](./asin.md), [`cos()`](./cos.md), and [`tan()`](./tan.md).
