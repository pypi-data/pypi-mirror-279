# `relationalai.std.math.log()`

```python
relationalai.std.math.log(x: Number | Producer, base: Number | Producer | None = None) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces the logarathm of `x` with base `base`.
If `base` is not provided, the natural logarithm is used.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `x` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the logarithm of. |
| `base` | `Number` or [`Producer`](../../Producer/README.md) or `None` | The base of the logarithm. If `None`, the natural logarithm is used (base _e_). |

## Returns

An [`Expression`](../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import log

# Create a model with a `Person` type.
model = rai.Model("people")
Person = model.Type("Person")

# Add some people to the model.
with model.rule():
    Person.add(name="Alice", age=9)
    Person.add(name="Bob", age=16)
    Person.add(name="Charlie", age=25)

# What is the log base 2 of each person's age?
with model.query() as select:
    p = Person()
    age_log2 = log(p.age, base=2)
    response = select(p.name, alias(age_log2, "age_log2"))

print(response.results)
# Output:
#       name  age_log2
# 0    Alice  3.169925
# 1      Bob  4.000000
# 2  Charlie  4.643856
```
