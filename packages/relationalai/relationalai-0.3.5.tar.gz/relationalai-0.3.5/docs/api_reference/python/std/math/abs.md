# `relationalai.std.math.abs()`

```python
relationalai.std.math.abs(number: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces the absolute value of `number`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `number` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the absolute value of. |

## Returns

An [`Expression`](../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import abs

# Create a model with a `Person` type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    Person.add(name="Alice", age=30)
    Person.add(name="Bob", age=40)
    Person.add(name="Charlie", age=50)

# What is the difference in age for each pair of people?
with model.query() as select:
    p1, p2 = Person(), Person()
    p1 < p2
    age_difference = abs(p1.age - p2.age)
    response = select(p1.name, p2.name, alias(age_difference, "age_difference"))

print(response.results)
# Output:
#       name  name2  age_difference
# 0      Bob  Alice              10
# 1  Charlie  Alice              20
# 2  Charlie    Bob              10
```
