# `relationalai.std.math.isclose()`

```python
relationalai.std.math.isclose(x: Number | Producer, y: Number | Producer, tolerance: Number | Producer = 1e-9) -> Expression
```

Adds a constraint to a [rule](../../Model/rule.md) or [query](../../Model/query.md) that
the absolute difference between `x` and `y` is less than or equal to `tolerance`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `x` | `Number` or [`Producer`](../../Producer/README.md) | The first number to compare. |
| `y` | `Number` or [`Producer`](../../Producer/README.md) | The second number to compare. |
| `tolerance` | `Number` or [`Producer`](../../Producer/README.md) | The maximum difference allowed between `x` and `y`. Default is `1e-9`. |

## Returns

An [`Expression`](../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import isclose

# Create a model with a `Person` type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    Person.add(name="Alice", height_cm=170)
    Person.add(name="Bob", height_cm=180)
    Person.add(name="Charlie", height_cm=180.0001)

# Find people who have the same height.
with model.query() as select:
    p1, p2 = Person(), Person()
    p1 < p2
    isclose(p1.height_cm, p2.height_cm, tolerance=1e-3)
    response = select(p1.name, p2.name)

print(response.results)e
# Output:
#   name    name2
# 0  Bob  Charlie
```
