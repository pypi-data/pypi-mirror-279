# `relationalai.std.math.sqrt()`

```python
relationalai.std.math.sqrt(number: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces the square root of `number`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `number` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the square root of. |

## Returns

An [`Expression`](../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import sqrt

# Create a model with a `Person` type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    Person.add(name="Alice", age=9)
    Person.add(name="Bob", age=16)
    Person.add(name="Charlie", age=25)

# What is the square root of each person's age?
with model.query() as select:
    p = Person()
    age_sqrt = sqrt(p.age)
    response = select(p.name, alias(age_sqrt, "age_sqrt"))

print(response.results)
# Output:
#       name  age_cbrt
# 0    Alice       3.0
# 1      Bob       4.0
# 2  Charlie       5.0
```

## See Also

[`cbrt()`](./cbrt.md) and [`**`](../../Producer/pow__.md).
