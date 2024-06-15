# `relationalai.std.math.floor()`

```python
relationalai.std.math.floor(number: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces the largest whole number less than or equal to `number`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `number` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the floor of. |

## Returns

An [`Expression`](../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import floor

# Create a model with a `Person` type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    Person.add(name="Alice", height_cm=170.1)
    Person.add(name="Bob", height_cm=180.9)

# What is each person's height rounded down to the nearest whole number?
with model.query() as select:
    p = Person()
    height_rounded = floor(p.height_cm)
    response = select(p.name, alias(height_rounded, "height_rounded"))

print(response.results)
# Output:
#     name  height_rounded
# 0  Alice           170.0
# 1    Bob           180.0
```

For negative numbers, the result is rounded towards negative infinity:

```python
with model.query() as select:
    response = select(floor(-5.5))

print(response.results)
# Output:
#      v
# 0 -6.0
```

## See Also

[`ceil()`](./ceil.md)
