# `relationalai.Producer.__floordiv__()`

```python
relationalai.Producer.__floordiv__(other: Any) -> Expression
```

Returns an [`Expression`](../Expression.md) that produces the quotient of the [`Producer`](./README.md) values and `other`, rounded towards negative infinity.
The type of the result is the same as the type of the producer's values.
`.__floordiv__()` is called when the `//` operator is used.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | The denominator of the floor division operation. |

## Returns

An [`Expression`](../Expression.md) object.

## Example

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39, account_balance=-123.45)
    Person.add(name="Wilma", age=36, account_balance=123.45)

with model.query() as select:
    person = Person()
    half_age = person.age // 2
    response = select(person.name, half_age)

print(response.results)
# Output:
#     name  result
# 0   Fred      19
# 1  Wilma      18
```

The type of the result is the same as the type of the numerator in the division.
Since the `age` property is an integer, the result is also an integer.

For negative numbers, the result is rounded towards negative infinity:

```python
with model.query() as select:
    person = Person()
    response = select(person.account_balance // 2)

print(response.results)
# Output:
#    result
# 0   -62.0
# 1    61.0
```

## See Also

[`Producer.__add__()`](./add__.md),
[`Producer.__sub__()`](./sub__.md),
[`Producer.__mul__()`](./mul__.md),
[`Producer.__truediv__()`](./truediv__.md),
[`Producer.__pow__()`](./pow__.md),
and [`Producer.__mod__()`](./mod__.md).
