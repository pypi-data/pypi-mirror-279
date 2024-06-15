# `relationalai.std.math.cbrt()`

```python
relationalai.std.math.cbrt(number: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces the cube root of `number`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `number` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the cube root of. |

## Returns

An [`Expression`](../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import cbrt

# Create a model with a `Person` type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    Person.add(name="Alice", age=8)
    Person.add(name="Bob", age=9)
    Person.add(name="Charlie", age=64)

# What is the cube root of each person's age?
with model.query() as select:
    p = Person()
    age_cbrt = cbrt(p.age)
    response = select(p.name, alias(age_cbrt, "age_cbrt"))

print(response.results)
# Output:
#       name  age_cbrt
# 0    Alice       2.0
# 1      Bob       3.0
# 2  Charlie       4.0
```

## See Also

[`sqrt()`](./sqrt.md)
