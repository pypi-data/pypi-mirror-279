# `relationalai.Producer.__mod__()`

```python
relationalai.Producer.__mod__(other: Any) -> Expression
```

Returns an [`Expression`](../Expression.md) object representing the remainder of dividing the `Producer` and another value.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | A numeric value or another `Producer` object. |

## Returns

An [`Expression`](../Expression.md) object that produces values of the same type as `other`.

## Example

You may calculate the remainder of dividing a `Producer` by a number literal:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)

# Get people with an even age.
with model.query() as select:
    person = Person()
    person.age % 2 == 0
    response = select(person.name, person.age)

print(response.results)
# Output:
#     name  age
# 0  Wilma   36
```

You may also calculate the remainder of dividing two `Producer` objects:

```python
with model.query() as select:
    fred = Person(name="Fred")
    wilma = Person(name="Wilma")
    response = select(fred.age % wilma.age)

print(response.results)
# Output:
#    v
# 0  3
```

## See Also

[`Producer.__add__()`](./add__.md),
[`Producer.__sub__()`](./sub__.md),
[`Producer.__mul__()`](./mul__.md),
[`Producer.__truediv__()`](./truediv__.md).
[`Producer.__floordiv__()`](./floordiv__.md),
and [`Producer.__pow__()`](./pow__.md).
