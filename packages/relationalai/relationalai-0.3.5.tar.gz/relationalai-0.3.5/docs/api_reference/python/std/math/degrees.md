# `relationalai.std.math.degrees()`

```python
relationalai.std.math.degrees(radians: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) object that produces the equivalent number of `radians` in degrees.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `radians` | `Number` or [`Producer`](../../Producer/README.md) | The number of radians to convert to degrees. |

## Returns

An [`Expression`](../../Expression.md) object that produces `float` values.

## Example

`degrees()` works with both numeric [producers](../../Producer/README.md) and Python number objects:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import degrees

# Create a model named "people" with a Person type.
model = rai.Model("people")
Person = model.Type("Person")

# Add a person to the model.
with model.rule():
    Person.add(name="Alice", age=30)

# degrees() works with numeric producers, such as a person's age property.
with model.query() as select:
    person = Person()
    response = select(person.name, alias(degrees(person.age), "degrees_age"))

print(response.results)
# Output:
#     name  degrees_age
# 0  Alice  1718.873385

# degrees() also works with Python number objects.
with model.query() as select:
    response = select(degrees(3.141593))

print(response.results)
# Output:
#            v
# 0  180.00002
```

## See Also

[`radians()`](./radians.md)
