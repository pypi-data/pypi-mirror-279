# `relationalai.std.math.trunc_divide()`

```python
relationalai.std.math.trunc_divide(numerator: Number | Producer, denominator: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces the result of the division of `numerator` by `denominator`, rounded towards zero.
The type of the result is the same as the type of the `numerator`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `numerator` | `Number` or [`Producer`](../../Producer/README.md) | The numerator of the division. |
| `denominator` | `Number` or [`Producer`](../../Producer/README.md) | The denominator of the division. |

## Returns

An [`Expression`](../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import trunc_divide

# Create a model with a `Person` type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    Person.add(name="Alice", height_cm=170.1)
    Person.add(name="Bob", height_cm=180)

# What is each person's height rounded down to the nearest whole number?
with model.query() as select:
    p = Person()
    half_height = trunc_divide(p.height_cm, 2)
    response = select(p.name, alias(half_height, "half_height"))

print(response.results)
# Output:
#     name  half_height
# 0  Alice         85.0
# 1    Bob         90.0
```

## See Also

[`//`](../../Producer/floordiv__.md) (floor division) and [`/`](../../Producer/truediv__.md) (true division).
