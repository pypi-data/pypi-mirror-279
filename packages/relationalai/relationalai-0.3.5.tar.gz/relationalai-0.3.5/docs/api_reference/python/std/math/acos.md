# `relationalai.std.math.acos()`

```python
relationalai.std.math.acos(number: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) object that produces the arccosine of `number` radians.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `number` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the arccosine of. |

## Returns

An [`Expression`](../../Expression.md) object that produces `float` values.

## Example

`acos()` works with both numeric [producers](../../Producer/README.md) and Python number objects:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import acos

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add a person to the model.
with model.rule():
    Person.add(name="Alice", age=3, height_m=0.95)

# acos() works with numeric producers, such as a person's height property.
# Inputs are assumed to be in radians.
with model.query() as select:
    person = Person()
    response = select(person.name, alias(acos(person.height_m), "acos_height"))

print(response.results)
# Output:
#     name  acos_height
# 0  Alice      0.31756

# acos() also works with Python number objects.
with model.query() as select:
    response = select(acos(0))

print(response.results)
# Output:
#           v
# 0  1.570796
```

The input to `acos()` must be in the range -1 to 1, inclusive.
If the input is outside this range,
the [query](../../Model/query.md) or [rule](../../Model/rule.md) will be impossible to satisfy:

```python
with model.query() as select:
    person = Person()
    response = select(person.name, alias(acos(person.age), "acos_age"))

print(response.results)
# Output:
# Empty DataFrame
# Columns: []
# Index: []
```

## See Also

[`cos()`](./cos.md), [`asin()`](./asin.md), and [`atan()`](./atan.md).
