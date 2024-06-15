# `relationalai.std.math.cos()`

```python
relationalai.std.math.cos(number: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) object that produces the cosine of `number` radians.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `number` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the cosine of. |

## Returns

An [`Expression`](../../Expression.md) object that produces `float` values.

## Example

`cos()` works with both numeric [producers](../../Producer/README.md) and Python number objects:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import cos

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add a person to the model.
with model.rule():
    Person.add(name="Alice", age=30)

# cos() works with numeric producers, such as a person's age property.
# Inputs are assumed to be in radians.
with model.query() as select:
    person = Person()
    response = select(person.name, alias(cos(person.age), "cos_age"))

print(response.results)
# Output:
#     name   cos_age
# 0  Alice  0.154251

# cos() also works with Python number objects.
with model.query() as select:
    response = select(cos(0))

print(response.results)
# Output:
#      v
# 0  1.0
```

## See Also

[`acos()`](./acos.md), [`sin()`](./sin.md), and [`tan()`](./tan.md).
