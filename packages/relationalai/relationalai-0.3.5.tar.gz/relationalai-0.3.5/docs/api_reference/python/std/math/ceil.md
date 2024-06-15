# `relationalai.std.math.ceil()`

```python
relationalai.std.math.ceil(number: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces the smallest whole number greater than or equal to `number`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `number` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the ceiling of. |

## Returns

An [`Expression`](../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import ceil

# Create a model with a `Person` type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    Person.add(name="Alice", height_cm=170.1)
    Person.add(name="Bob", height_cm=180.9)

# What is each person's height rounded up to the nearest whole number?
with model.query() as select:
    p = Person()
    height_rounded = ceil(p.height_cm)
    response = select(p.name, alias(height_rounded, "height_rounded"))

print(response.results)
# Output:
#     name  height_rounded
# 0  Alice           171.0
# 1    Bob           181.0
```

For negative numbers, the result is rounded towards zero:

```python
with model.query() as select:
    response = select(ceil(-5.5))

print(response.results)
# Output:
#      v
# 0 -5.0
```

## See Also

[`floor()`](./floor.md)
