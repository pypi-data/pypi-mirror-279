# `relationalai.std.math.asin()`

```python
relationalai.std.math.asin(number: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) object that produces the arcsine of `number` radians.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `number` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the arcsine of. |

## Returns

An [`Expression`](../../Expression.md) object that produces `float` values.

## Example

`asin()` works with both numeric [producers](../../Producer/README.md) and Python number objects:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import asin

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add a person to the model.
with model.rule():
    Person.add(name="Alice", age=3, height_m=0.95)

# asin() works with numeric producers, such as a person's height property.
# Inputs are assumed to be in radians.
with model.query() as select:
    person = Person()
    response = select(person.name, alias(asin(person.height_m), "asin_height"))

print(response.results)
# Output:
#     name  asin_height
# 0  Alice     1.253236

# asin() also works with Python number objects.
with model.query() as select:
    response = select(asin(0))

print(response.results)
# Output:
#           v
# 0  1.570796
```

The input to `asin()` must be in the range -1 to 1, inclusive.
If the input is outside this range,
the [query](../../Model/query.md) or [rule](../../Model/rule.md) will be impossible to satisfy:

```python
with model.query() as select:
    person = Person()
    response = select(person.name, alias(asin(person.age), "asin_age"))

print(response.results)
# Output:
# Empty DataFrame
# Columns: []
# Index: []
```

## See Also

[`sin()`](./sin.md), [`acos()`](./acos.md), and [`atan()`](./atan.md).
