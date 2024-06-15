# `relationalai.Producer.__rfloordiv__()`

```python
relationalai.Producer.__rfloordiv__(other: Any) -> Expression
```

Returns an [`Expression`](../Expression.md) that produces the quotient of `other` and the [`Producer`](./README.md) values, rounded towards negative infinity.
The type of the result is the same as the type of `other`.
`.__rfloordiv__()` is implemented so that you may use a non-`Producer` object as the left operand with the `//` operator.

## See Also

[`__floordiv__()`](./floordiv__.md)
