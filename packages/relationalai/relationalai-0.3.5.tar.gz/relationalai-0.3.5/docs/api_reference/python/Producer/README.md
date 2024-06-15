<!-- markdownlint-disable MD024 -->

# `relationalai.Producer`

```python
class relationalai.Producer()
```

Instances of the `Producer` class act as variables in a [rule](../Model/rule.md) or [query](../Model/query.md) context.
When the context is evaluated, all possible values for the variable are produced.
Instead of constructing `Producer` instances directly, they are returned as the result of various operations.

The `Producer` class is the base class for different kinds of producers, including:

- [`Instance`](../Instance/README.md), returned when you call a [`Type`](../Type/README.md).
- [`InstanceProperty`](../InstanceProperty/README.md), returned when you access a property of an object.
- [`Expression`](../Expression.md), returned as the result of an operation on a producer, such as a mathematical or Boolean expression, or an aggregation.

## Methods

The following methods support mathematical operations on producers:

| Name | Description | Returns |
| :------ | :------------ | :------ |
| [`__add__()`](./add__.md), [`__radd__()`](./radd__.md) | Supports the `+` operator between producers and other values. | [`Expression`](../Expression.md) |
| [`__sub__()`](./sub__.md), [`__rsub__()`](./rsub__.md) | Supports the `-` operator between producers and other values. | [`Expression`](../Expression.md) |
| [`__mul__()`](./mul__.md), [`__rmul__()`](./rmul__.md) | Supports the `*` operator between producers and other values. | [`Expression`](../Expression.md) |
| [`__truediv__()`](./truediv__.md), [`__rtruediv__()`](./rtruediv__.md) | Supports the `/` operator between producers and other values. | [`Expression`](../Expression.md) |
| [`__floordiv__()`](./floordiv__.md), [`__rfloordiv__()`](./rfloordiv__.md) | Supports the `//` operator between producers and other values. | [`Expression`](../Expression.md) |
| [`__pow__()`](./pow__.md), [`__rpow__()`](./rpow__.md) | Supports the `**` operator between producers and other values. | [`Expression`](../Expression.md) |
| [`__mod__()`](./mod__.md), [`__rmod__()`](./rmod__.md) | Supports the `%` operator between producers and other values. | [`Expression`](../Expression.md) |

The following methods support comparison operations on producers:

| Name | Description | Returns |
| :------ | :------------ | :------ |
| [`__eq__()`](./eq__.md) | Supports `==` comparison between producers and other values. | [`Expression`](../Expression.md) |
| [`__ne__()`](./ne__.md) | Supports `!=` comparison between producers and other values. | [`Expression`](../Expression.md) |
| [`__ge__()`](./ge__.md) | Supports `>=` comparison between producers and other values. | [`Expression`](../Expression.md) |
| [`__gt__()`](./gt__.md) | Supports `>` comparison between producers and other values. | [`Expression`](../Expression.md) |
| [`__le__()`](./le__.md) | Supports `<=` comparison between producers and other values. | [`Expression`](../Expression.md) |
| [`__lt__()`](./lt__.md) | Supports `<` comparison between producers and other values. | [`Expression`](../Expression.md) |

Instances of `Producer` support arbitrary attribute access
and can be used as a [context manager](https://docs.python.org/3/reference/datamodel.html#context-managers)
in a [`with` statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement):

| Name | Description | Returns |
| :------ | :------------ | :------ |
| [`__getattribute__()`](./getattribute__.md) | Get a property of an object. | [`InstanceProperty`](../InstanceProperty/README.md) |
| [`__enter__()`](./enter__.md) | Enter the producer's context. | `None` |
| [`__exit__()`](./exit__.md) | Exit the producer's context. | `None` |

## Example

The key idea behind the `Producer` class is that it is used to represent a variable
in a [rule](../Model/rule.md) or [query](../Model/query.md) context:

```python
import relationalai as rai

# Create a model named 'people' with Person and Adult types.
model = rai.Model("people")
Person = model.Type("Person")
Adult = model.Type("Adult")

# Add some people to the model.
with model.rule():
    # Type.add() returns an Instance, which is a producer.
    alice = Person.add(name="Alice", age=8)
    bob = Person.add(name="Bob", age=36)
    # Instance producers have a .set() method for setting properties and
    # additional types on objects.
    bob.set(parent_of=alice)


# Create a rule that sets the Adult type on each person whose age is at least 18.
with model.rule():
    # Calling a type returns an Instance producer.
    person = Person()  # person produces Person objects.
    # person.age returns an InstanceProperty, which is also a producer.
    # Comparing the age to 18 returns an Expression, yet another producer.
    person.age >= 18  # Filter to people who are 18 or older.
    person.set(Adult)  # Set the adult type on the people who pass the filter.
```

You can think of the rule as executing once for each `Person` object in the model.
Each line in the rule describes a step in a pipeline that the objects produced by `person` pass through:

1. `person` Produces a `Person` object.
2. `person.age >= 18` only lets through objects with an age of 18 or more.
3. `person.set(Adult)` sets the `Adult` type on the objects that pass through.

The object for Alice never reaches the last step because her age is less than 18.
But the object for Bob _does_ reach the last step, and the `Adult` type is set on it.

Multiple producers may be mixed in the same rule or query:

```python
# Get pairs of people where the first person is younger than the second.
with model.query() as select:
    person1, person2 = Person(), Person()
    person1.age < person2.age
    response = select(person1.name, person2.name)

print(response.results)
# Output:
#    name1  name2
# 0  Alice    Bob
```

Both `person1` and `person2` produce `Person` objects.
The query is evaluated for each pair of possible values for `person1` and `person2`, of which there are four:

- Alice and Alice
- Alice and Bob
- Bob and Alice
- Bob and Bob

Only the pair (Alice, Bob) passes through the comparison and into `select()` since Alice is 8 and Bob is 36.

Producers can be used as context managers.
This is especially useful for `Expression` producers, which can be used to create a subcontext that applies to a subset of objects:

```python
Minor = model.Type("Minor")

with model.rule():
    person = Person()
    # If the person's age is less than 18, set the Minor type.
    with person.age < 18:
        person.set(Minor)
    # If the person's age is at least 18, set the Adult type.
    with person.age >= 18
        person.set(Adult)
```

Thinking of the rule as a pipeline, the `with` statement creates a subcontext
whose contents only apply to objects for which the `Expression` is true,
but doesn't block objects from passing through to the rest of the rule.

For example, the Alice object passes through the first `with` statement and gets the `Minor` type set on it since she is 8.
Her object still passes through to the second `with` statement, but the `Adult` type is not set on her because the expression is false.
Bob, on the other hand, passes through the first `with` statement without setting the `Minor` type, but the `Adult` type is set on him in the second `with` statement.

## See Also

[`Instance`](../Instance/README.md),
[`InstanceProperty`](../InstanceProperty/README.md),
and [`Expression`](../Expression.md).
