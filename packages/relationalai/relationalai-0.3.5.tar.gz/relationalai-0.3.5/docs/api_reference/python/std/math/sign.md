# `relationalai.std.math.sign()`

```python
relationalai.std.math.sign(x: Number | Producer) -> Expression
```

Returns an [`Expression`](../../Expression.md) that produces the sign of `x`.
The sign of a number is `1` if the number is positive, `-1` if the number is negative, and `0` if the number is zero.
The type of the sign is the same as the type of `x`.

## Parameters

| Name | Type | Description |
| :--- | :--- | :--------- |
| `x` | `Number` or [`Producer`](../../Producer/README.md) | The number to take the sign of. |

## Returns

An [`Expression`](../../Expression.md) object.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.math import sign

# Create a model with `Account` and `Transaction` types.
model = rai.Model("people")
Account = model.Type("Account")
Transaction = model.Type("Transaction")

# Add some people to the model.
with model.rule():
    account = Account.add(id="ACC1", balance=0.0)
    Transaction.add(id=1, account=account, amount=50.0)
    Transaction.add(id=2, account=account, amount=-25.0)

# What is the sign of each transaction amount?
with model.query() as select:
    t = Transaction()
    sign_amount = sign(t.amount)
    response = select(t.id, t.amount, alias(sign_amount, "sign_amount"))

print(response.results)
# Output:
#    id  amount  sign_amount
# 0   1    50.0          1.0
# 1   2   -25.0         -1.0
```
